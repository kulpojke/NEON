import os
import random
import numpy as np
import h5py
import matplotlib.pyplot as plt

from numba import cuda, jit

from dask import delayed, compute
from dask.diagnostics import ProgressBar

from sklearn.preprocessing import  StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA as IPCA
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

import rasterio as rio

import xarray as xr
import rioxarray

import glob


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
    args.dst = os.path.join(args.out_dir,
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


def plot_pca_var(pca):
    '''plots explained variance by PCA component'''

    # make fig
    plt.figure(figsize=(10,4));

    # plot
    plt.plot(range(1, 359),
             pca.explained_variance_ratio_.cumsum(),
             marker='o',
             linestyle='--');

    # details
    plt.title('Explained Variance by Number of Components');
    plt.xlabel('Components');
    plt.ylabel('Cumulative explained Var');
    plt.xlim(0, 20);
    plt.show()


def kmeans_wcss(n_components, scaled_refl, max_n_clusters=20):
    '''
    Returns a list of wcss values for different n_clusters values
    after performing PCA using n_components.
    args:
        n_components   - number of components to be kept in PCA.
        scaled_refl    - scaled values on which to perform PCA and
                         clustering.
        max_n_clusters - max number of clusters to try default 20.
    '''
    # use n components for pca
    pca = PCA(n_components=n_components)

    # fit
    pca.fit(scaled_refl)

    # get component scores
    scores_pca = pca.transform(scaled_refl)

    # empty list for witih cluster sum of squares
    wcss = []

    # now try out some differnt cluster numbers
    print(f'Out of {max_n_clusters} trials working on:')

    for n in range(1, max_n_clusters + 1):

        print(f'\b\b{n}', end="")

        kmeans =  KMeans(n_clusters=n, init='k-means++', random_state=42)
        kmeans.fit(scores_pca)
        wcss.append(kmeans.inertia_)

    print('\ndone!')

    return wcss, pca



if __name__ == '__main__':

    # parse the args
    args = parse_arguments()

    # find the years with htperspectral data
    years = [y
             for y
             in os.listdir(args.src)
             if os.path.isdir(os.path.join(args.dst, y))]

    # make a dict with paths to all files for each year
    data_dict = {}
    for year in years:

        globstring = os.path.join(
            args.src,
            year,
            'Fullsite',
            'D??',
            f'{year}_{args.site}_*',
            'L3',
            'Spectrometer',
            'Reflectance',
            '*.h5'
            )

        data_dict[year] =  glob.glob(globstring)

    # ensure directory for pca tiffs exists and make path
    os.makedirs(args.pca, exist_ok=True)

    # begin to make a the path to the hyperspectral data
    hyper_path = os.path.join(args.data_dir,
                              args.site,
                              'hyperspectral',
                              'DP3.30006.001',
                              'neon-aop-products')

    # check to make sure there is hyperspectral for the site
    if not os.path.isdir(hyper_path):
        a = f'There appears to be no hyperspectral data for {args.site} '
        b = f'{hyper_path} is not a directory.'
        msg = a + b
        raise Exception(msg)

    # get the years (they are directories in hyper_path)
    years = os.listdir(hyper_path)

    for year in years:

        # get the rest of the path
        globstring = os.path.join(hyper_path,
        year,
        'FullSite',
        'D08',
        f'{year}_{args.site}_[0-9]',
        'L3',
        'Spectrometer',
        'Reflectance',
        f'NEON_D08_{args.site}_DP3_*.h5')

        # find the names of the hyperspectral cubes
        files = glob.glob(globstring)
