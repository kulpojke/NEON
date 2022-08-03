from distutils.ccompiler import new_compiler
import os
import random
import glob
import numpy as np
import argparse

import h5py
from dask import delayed, compute
from dask.diagnostics import ProgressBar
from sklearn.preprocessing import  StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import rasterio as rio
import xarray as xr
import rioxarray

from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)



def parse_arguments():
    '''parses the arguments, returns args'''

    # init parser
    parser = argparse.ArgumentParser()

    # add args

    parser.add_argument(
        '--site',
        type=str,
        required=True,
        help='NEON site abreviation, e.g. "TEAK"',
    )

    parser.add_argument(
        '--n_components',
        type=int,
        required=True,
        help='Number of PCA components to use',
    )

    parser.add_argument(
        '--n_clusters',
        type=int,
        required=True,
        help='Number of kmeans clusters to use.',
    )

    parser.add_argument(
        '--out_dir',
        type=str,
        required=True,
        help='''Directory into which site/mosaic subdir will be placed.
        For example if --site=TEAK and --out_dir=NEON,

        NEON
        |
        |__TEAK
           |
           |__mosaic

        will be created. The site dir may already exist, but does not have to.

        ''',
    )

    parser.add_argument(
        '--data_dir',
        type=str,
        required=False,
        help='''Directory where hyperspectral data is stored. Hyperspectral data
        should be stored in a subdirectory site/hyperspectral.  If --data_dir
        is ommited it will be assumed that data_dir is the same as out_dir.
        As an example of the directory structure required, if
        --site=TEAK and --data_dir=NEON,

        NEON
        |
        |__TEAK
           |
           |__hyperspectral

        '''
    )

    # parse the args
    args = parser.parse_args()

    # make data_dir if not specified
    if not args.data_dir:
        args.data_dir = args.out_dir

    # make source path
    args.src = os.path.join(args.data_dir,
                            args.site,
                            'hyperspectral',
                            'DP3.30006.001')

    # adjust source path in case there is an issue-log changing path
    if os.path.isdir(os.path.join(args.src, 'neon-aop-products')):
        args.src = os.path.join(args.src, 'neon-aop-products')

    # make destination path
    args.mosaic = os.path.join(args.out_dir,
                            args.site,
                            'mosaic')

    # make a path to hold pca output
    args.pca = os.path.join(args.out_dir, args.site, 'pca')

    return args


def band_list():
    '''excludes bands with H2O or CO2 absorption'''
    good_bands = np.hstack([
        np.arange(0, 188 + 1),
        np.arange(211, 269 + 1),
        np.arange(316, 425 + 1)
    ])

    return good_bands


@delayed
def sample_from_file(fname, size):
    '''samples from file'''

    # open the file
    f = h5py.File(fname, 'r')

    # get the within reflectance as np array
    refl_array = np.array(np.rot90(f[args.site]['Reflectance']['Reflectance_Data']))

    # drop bad bands from refl_array
    refl_array = refl_array[:, :, band_list()]

    # get shape of wavelenght dimension
    wl = refl_array.shape[2]

    # reshape
    flat_refl = refl_array.reshape(-1, wl)

    # drop nulls
    flat_refl = flat_refl[
    (~np.any(flat_refl == -9999, axis=1)) &
    (~np.any(np.isnan(flat_refl), axis=1))]

    # get random sample indices
    random.seed(3)
    sample_idx = random.sample(range(flat_refl.shape[0]), int(flat_refl.shape[0] * size))

    # return sample
    return flat_refl[sample_idx, :]


def sample_from_all(files, size):
    '''
    Returns a np array of samples of shape (N, wl) where N is
    the number of samples and wl is the length of the wavelength
    dimension.

    args:
        files    - list of full paths to netcdf4 files to be used.
        size     - fraction of data to be used.
    '''
    # empty list for samples
    samples = []

    for fname in files:
        samples.append(sample_from_file(fname, size))

    with ProgressBar():
        sample = np.vstack(compute(*samples))

    return sample


def read_h5_do_pca(fname, scaler, pca):
    '''reads'''

    # open the file
    f = h5py.File(fname, 'r')

    # seperate out reflectance
    refl = f[args.site]['Reflectance']

    # get no data value
    no_data_value = refl['Reflectance_Data'].attrs['Data_Ignore_Value']

    # get the actual data within reflectance as array
    refl_array = np.array(np.rot90(refl['Reflectance_Data'], k=3), dtype=np.float16)

    # drop bad bands from refl_array
    refl_array = refl_array[:, :, band_list()]

    # get wavelength info
    wavelengths = np.array(refl['Metadata']['Spectral_Data']['Wavelength'])

    # drop bad bands from wavelength
    wavelengths = wavelengths[band_list()]

    # get  dimensions of array
    x  = refl_array.shape[0]
    y  = refl_array.shape[1]
    wl = refl_array.shape[2]

    # reshape
    flat_refl = refl_array.reshape(-1, wl)

    # make sure there are no nans
    flat_refl[np.isnan(flat_refl)] = no_data_value

    # before we drop no-datas get their indices
    null_idx = np.argwhere(np.any(flat_refl == no_data_value, axis=1)).flatten()

    # pick arbitray valid index
    good_idx = np.argwhere(~np.any(flat_refl == no_data_value, axis=1)).flatten()[25]

    # fill no-datas with a vaule within normal range if need be (they will be returned to na data val in output)
    if null_idx.any():
        #flat_refl = flat_refl[np.argwhere(~np.any(flat_refl == no_data_value, axis=1)).flatten()]
        flat_refl[null_idx] = flat_refl[good_idx]

    # scale with previously fit scaler
    scaled = scaler.transform(flat_refl)

    # get component scores
    scores_pca = pca.transform(scaled)

    # put no-data values back in if need be
    if null_idx.any():
        #scores_pca = np.insert(scores_pca, null_idx, [no_data_value] * scores_pca.shape[1], axis=0)
        scores_pca[null_idx, :] = [no_data_value] * scores_pca.shape[1]

    # reshape to original tile x, y
    scores_pca = scores_pca.reshape(x, y, args.n_components)

    # close hdf
    #f.close()

    return scores_pca, refl


def tiffize_and_xarray(arr, refl, out_file):
    '''
    Writes tiff from array.

    args:
        arr      - array to be written as tiff
        refl     - reflectance metadata from h5
        out_file - filename of tiff to write
    '''
    # bag crs as epsg
    epsg = refl['Metadata']['Coordinate_System']['EPSG Code'][()].decode("utf-8")
    epsg = f'EPSG:{epsg}'

    # bag other crs info
    crs_info = refl['Metadata']['Coordinate_System']['Map_Info'][()].decode("utf-8").split(',')

    # get corners and x, y resolution
    xmin = float(crs_info[3])
    ymax = float(crs_info[4])
    xres = float(crs_info[5])
    yres = float(crs_info[6])
    xmax = xmin + (arr.shape[1] * xres)
    ymin = ymax - (arr.shape[0] * yres)

    # create array of x center pixel locations in utm coords
    x = np.linspace(xmin, xmax, arr.shape[1], endpoint=False)
    x = x + xres * 0.5

    # create array of y center pixel locations in utm coords
    y = np.linspace(ymin, ymax, arr.shape[0], endpoint=False)
    y = y + yres * 0.5

    # make dataset
    d_all = xr.DataArray(arr, dims=['x', 'y', 'components'], coords={'x':x, 'y':y, 'components': range(arr.shape[2])})
    d_all.name = 'pca'
    d_all = d_all.to_dataset()

    # assign crs and spatial dims
    d_all.rio.write_crs(epsg, inplace=True)

    # attributes
    no_data_value = refl['Reflectance_Data'].attrs['Data_Ignore_Value']
    d_all.attrs = {
                    'no_data_value': no_data_value,
                    'epsg': epsg,
                    'crs' : crs_info
                  }

    # write the labels to geotiff
    d_all.pca.transpose('components', 'y', 'x').rio.to_raster(out_file)

    return d_all


if __name__ == '__main__':

    # parse the args
    args = parse_arguments()

    # ensure directory for pca tiffs exists and make path
    os.makedirs(args.pca, exist_ok=True)

    # find the years with hyperspectral data
    years = [y
             for y
             in os.listdir(args.src)
             if os.path.isdir(os.path.join(args.src, y))]

    # check to make sure there is hyperspectral for the site
    if not os.path.isdir(args.src):
        a = f'There appears to be no hyperspectral data for {args.site} '
        b = f'{args.src} is not a directory.'
        msg = a + b
        raise Exception(msg)

    # get the years (they are directories in hyper_path)
    years = os.listdir(args.src)

    for year in years:

        # get the rest of the path
        globstring = os.path.join(args.src,
        year,
        'FullSite',
        'D[0-9][0-9]',
        f'{year}_{args.site}_[0-9]',
        'L3',
        'Spectrometer',
        'Reflectance',
        f'NEON_D[0-9][0-9]_{args.site}_DP3_*.h5')

        # find the names of the hyperspectral cubes
        files = glob.glob(globstring)

        # sample the files so we can train scalar
        size = 1 / 500
        sample = sample_from_all(files, size)

        # change dtype for memory
        sample = np.array(sample, dtype=np.float16)

        # fit and transform
        scaler = StandardScaler().fit(sample)
        scaled = scaler.transform(sample)

        # instantiate the PCA model
        pca = PCA(n_components=args.n_components)

        # fit the pca model
        pca.fit(scaled)

        # delete sample for memory
        del sample
        del scaled

        # list for xarrays to merge later
        xarrays = []

        print(f'Working om {len(files)} files for {args.site}-{year}')
        for i, f in tqdm(enumerate(files)):

            base = os.path.basename(f).split('.')[0].split('_')
            base = '_'.join([base[2], base[4], base[5]])

            scores_pca, refl = read_h5_do_pca(f, scaler, pca)

            # make fname
            os.makedirs(os.path.join(args.pca, year), exist_ok=True)
            tiff = os.path.join(args.pca, year, f'{base}_pca.tiff')

            # write tiffs and make xarrays
            xarrays.append(tiffize_and_xarray(scores_pca, refl, tiff))

        # combine the xarrays
        mosaic = xr.combine_by_coords(xarrays, combine_attrs='override')
        no_data_value = mosaic.attrs['no_data_value']

        # get the nice unified pca array
        pca_arr = mosaic.pca.data

        # determine number of pca compnents in use
        comps = mosaic.components.data.shape[0]

        # flatten the pca img
        flat_pca = pca_arr.reshape(-1, comps)

        # before we drop no-datas get their indices
        null_idx = np.argwhere(np.any(flat_pca == no_data_value, axis=1)).flatten()

        # pick arbitray valid index
        good_idx = np.argwhere(~np.any(flat_pca == no_data_value, axis=1)).flatten()[25]

        # drop no-datas
        if null_idx.any():
            flat_pca[null_idx] = flat_pca[good_idx]

        # cluster
        kmeans =  KMeans(n_clusters=args.n_clusters, init='k-means++', random_state=42)
        kmeans.fit(flat_pca)

        # get labels
        labels = kmeans.labels_

        # add the labels to the xarray
        mosaic['kmeans_label'] = xr.DataArray(labels.reshape(pca_arr.shape[0], pca_arr.shape[1]), dims=['x', 'y'])

        # ensure directory for mosaics exists
        os.makedirs(os.path.join(args.mosaic, year), exist_ok=True)

        # make fname
        tiff = os.path.join(args.mosaic, year, f'{args.site}_{year}_kmeans_mosaic.tiff')

        # write the labels to geotiff
        mosaic.kmeans_label.transpose('y', 'x').rio.to_raster(tiff, dtype=np.int8)

        # make fname
        tiff = os.path.join(args.mosaic, year, f'{args.site}_{year}_pca_mosaic.tiff')

        # write the labels to geotiff
        mosaic.pca.transpose('components', 'y', 'x').rio.to_raster(tiff)

        # write netCDF
        ncdf = os.path.join(args.mosaic, year, f'{args.site}_{year}_mosaic.nc')
        mosaic.to_netcdf(ncdf)