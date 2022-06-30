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

        will be created. Tee site dir may already exist, but does not have to. 
        
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
        if os.path.isdir(os.path.join(args.src, 'neon-aop-products'):
            args.src = os.path.join(args.src, 'neon-aop-products')

        # make destination path
        args.dst = os.path.join(args.out_dir,
                                args.site,
                                'mosaic')

        # make a path to hold pca output
        args.pca = os.path.join(args.out_dir, args.site, 'pca')

        return args


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
            Fullsite,
            'D??',
            f'{year}_{site}_*',
            'L3',
            'Spectrometer',
            'Reflectance',
            '*.h5'
            )

        data_dict[year] =  glob.glob(globstring)

    # ensure directory for pca tiffs exists and make path
    os.makedirs(args.pca, exist_ok=True)
    
