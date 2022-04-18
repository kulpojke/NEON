# %%
import numpy as np
import xarray as xr
import rioxarray
from xrspatial.classify import equal_interval
import os
from tqdm import tqdm
import argparse
from argparse import RawTextHelpFormatter
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# %%
def parse_arguments():
    '''parses the arguments, returns args'''

    # init parser
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    # add args

    parser.add_argument(
        '--site',
        type=str,
        required=True,
        help='NEON site abreviation, e.g. "TEAK"',
    )

    parser.add_argument(
        '--year',
        type=str,
        required=True,
        help='Year for which foorprints will be converted'
    )

    parser.add_argument(
        '--data_dir',
        type=str,
        required=True,
        help='''Base data directory of project. Must contain\na directory named for the site, which must in turn\ncontain directories footprints, which contains\nthe footprint rasters generated by the R function\nneonUtilities::footRaster, and mosaic, containing the mosaic from ___.  This function will create\n(if not existent) a directory within the site\ndirectory called quantile_footprints where the\noutputs will be stored.\n\ne.g. If data_dir=NEON, site=TEAK, and year=2019:

        NEON
        |__TEAK
           |
           |__footprints
           |  |
           |  |__20190601T000000Z.tiff
           |  |__ ...
           |  |__20191031T230000Z.tiff
           |
           |__quantile_footprints
           |  |
           |  |__20190601T000000Z.nc
           |  |__ ...
           |  |__20191031T230000Z.nc
           |
           |__mosaic
              |
              |__TEAK_2019_mosaic.nc
        ''',
    )

    # parse the args
    args = parser.parse_args()

    # add paths to args
    args.basepath = os.path.join(args.data_dir, args.site)
    args.ncdf = os.path.join(args.basepath, 'mosaic', f'{args.site}_{args.year}_mosaic.nc')
    args.foot_path = os.path.join(args.basepath, 'footprints')

    return(args)


def interp_foot_2_data(footprint, data):

    # footprints are different resolution so we must upscale, first get dims
    old_x = footprint.shape[1]
    old_y = footprint.shape[0]

    # then upscale
    footprint = footprint.interp_like(data.kmeans_label)

    # fill nulls
    footprint = footprint.fillna(0)

    # renormalize , interp messes up the sum
    footprint = footprint / np.nansum(footprint)

    return(footprint)


def square_crop(q):
    '''returns 1km square datarray cropped around the extent of non-zero entries'''
    # find the extent of the q95 mask
    xmin = q.x.values[np.argwhere(q.data > 0)[:,1].min()]
    xmax = q.x.values[np.argwhere(q.data > 0)[:,1].max()]

    ymin = q.y.values[np.argwhere(q.data > 0)[:,0].min()]
    ymax = q.y.values[np.argwhere(q.data > 0)[:,0].max()]

    # buffer it out to km^2
    xbuf = (1000 - (xmax - xmin)) / 2
    xmin = xmin - xbuf
    xmax = xmax + xbuf

    ybuf = (1000 - (ymax - ymin)) / 2
    ymin = ymin - ybuf
    ymax = ymax + ybuf


    mask_x = (q.x >= xmin) & (q.x <= xmax)
    mask_y = (q.y >= ymin) & (q.y <= ymax)

    crop = q.where(mask_x & mask_y, drop=True)
    return crop


def initiate_footstack(foot, data):
    '''
    uses the first footprint to create a new dataset
    '''
    # get timestamp
    t = os.path.basename(foot).split('.')[0]

    # open footprint
    footprint = rioxarray.open_rasterio(foot)

    # footprint.shape is(1, y, x) so bust it out 3rd dim
    footprint = footprint[0]

    # upscale and align footprint
    footprint = interp_foot_2_data(footprint, data)

    # create equal interval contour classifcations
    footprint = equal_interval(footprint, k=20)

    # get the q95 footprint
    vals = set(footprint.data[footprint.data > 0].flatten())
    val_max = max(vals)
    q95 = np.zeros_like(footprint.data, dtype=np.int8)
    q95[footprint.data == val_max] = 1
    q95 = xr.DataArray(q95, dims=['y', 'x'], coords=[footprint.y, footprint.x])

    # crop q95 footprint to 1km square
    q95 = square_crop(q95)

    # align footprint to q95
    global CROP_TEMPLATE
    CROP_TEMPLATE, footprint = xr.align(q95, footprint)

    # create the dataset
    footstack = footprint.to_dataset()
    footstack = footstack.drop('equal_interval')

    # ad a new dimension, t, fot timeseries of footrasters
    footstack = footstack.expand_dims(dim='t')

    # make all 0.5 t0 0.95 quantile rasters
    qs = []
    names = []

    for val in vals:
        q = np.zeros_like(footprint.data, dtype=np.int8)
        q[footprint.data == val] =  1
        q = xr.DataArray(q, dims=['y', 'x'], coords=[footprint.y, footprint.x])
        names.append(f'q{int(val * 5)}')
        qs.append(q)

    foot_series = xr.concat(qs, dim='quantile')

    return footstack, foot_series, t


def make_foot_series(foot):

    # get timestamp
    t = os.path.basename(foot).split('.')[0]

    # open footprint
    footprint = rioxarray.open_rasterio(foot)

    # footprint.shape is(1, y, x) so bust it out 3rd dim
    footprint = footprint[0]

    # upscale and align footprint
    footprint = interp_foot_2_data(footprint, data)

    # create equal interval contour classifcations
    footprint = equal_interval(footprint, k=20)

    # make all 0.5 t0 0.95 quantile rasters
    qs = []
    names = []

    vals = set(footprint.data[footprint.data > 0].flatten())
    for val in vals:
        q = np.zeros_like(footprint.data, dtype=np.int8)
        q[footprint.data == val] =  1
        q = xr.DataArray(q, dims=['y', 'x'], coords=[footprint.y, footprint.x])
        _ , q = xr.align(CROP_TEMPLATE, q)
        names.append(f'q{int(val * 5)}')
        qs.append(q)

    foot_series = xr.concat(qs, dim='quantile')

    return foot_series, t





# %%
if __name__ == '__main__':

    # parse the args
    args = parse_arguments()

    # get names of footprints
    footprints = [
                    os.path.join(args.foot_path, f)
                    for f
                    in os.listdir(args.foot_path)
                    if 'summary'
                    not in f
                    and '.xml' not in f]

    # open netcdf mosaic
    data = xr.open_dataset(args.ncdf)

    # set epsg from attrs
    data = data.rio.write_crs(data.attrs['epsg'])

    # clip the hyperspectral derived data to footprint extent
    footprint = rioxarray.open_rasterio(footprints[0])
    data = data.rio.clip_box(minx=footprint.x.values.min(),
                             miny=footprint.y.values.min(),
                             maxx=footprint.x.values.max(),
                             maxy=footprint.y.values.max())

    # ensure directory exists for results to live in
    footmask_home = os.path.join(args.basepath, 'quantile_footprints')
    os.makedirs(footmask_home, exist_ok=True)

    first = True

    for foot in tqdm(footprints):
        if first:
            footstack, foot_series, t = initiate_footstack(foot, data)
            first = False
        else:
            foot_series, t = make_foot_series(foot)

        foot_series = foot_series.rename('footprint')
        foot_series.to_netcdf(os.path.join(footmask_home, f'{t}.nc'))


    print(f'Finished writing files to {footmask_home}')