# %%
import xarray as xr
import rioxarray
import numpy as np
import pandas as pd
from pandas import to_datetime
from tqdm import tqdm

import argparse
import os
import  glob


def parse_args():
    '''
    This is a temporary version of parse args for development
    '''

    args = {'site' : 'TALL',
            'year' : 2021,
            'path' : '/media/data/NEON/'}

    args = argparse.Namespace(**args)

    return args


def find_nearest_file(footprint,site, mosaic_path):
    '''
    Returns the file path to the netcdf containing kmeans classification
    for which the year is closest to that of footprint.
    '''

    # get directory
    path = os.path.dirname(footprint)

    # get year of footprint
    foot_year = int(os.path.basename(footprint).split('T')[0][:4])

    # get names of netcdf files
    globstring = os.path.join(mosaic_path, f'{site}_????_mosaic.nc')
    nc_files = glob.glob(globstring)

    # get years of existing nc files
    nc_years =[int(os.path.basename(f).split('_')[1]) for f in nc_files]

    # find closet year to foot_year (if 2 are the same take past file)
    diffs = [abs(y - foot_year) for y in nc_years]
    close_file = nc_files[np.argmin(diffs)]

    return close_file


def get_timestep(foot):

    # empty list
    t = []

    # get timestamp
    t.append(to_datetime(os.path.basename(foot).split('.')[0]))

    # find filepath to netcdf mosaic
    ncdf = find_nearest_file(foot, args.site, mosaic_path)

    # open netcdf
    data = xr.open_dataset(ncdf)

    # open footprint
    footprint = rioxarray.open_rasterio(foot)

    # footprints are 20m resolution so we must upscale, first get dims
    old_dim = footprint.shape[1]

    # then upscale
    footprint = footprint.interp_like(data.kmeans_label)

    # renormalize , interp messes up the sum
    footprint = footprint / (footprint.shape[1]**2 / old_dim**2)

    # set epsg from attrs
    data = data.rio.write_crs(data.attrs['epsg'])

    # clip the hyperspectral derived data to fpptprint extent
    data = data.rio.clip_box(minx=np.atleast_1d(footprint.x.min())[0],
                            miny=np.atleast_1d(footprint.y.min())[0],
                            maxx=np.atleast_1d(footprint.x.max())[0],
                            maxy=np.atleast_1d(footprint.y.max())[0])

     # calculate weighted class sums
    for label in labels:
        mask = data.kmeans_label.data == label
        t.append(np.atleast_1d((mask * footprint).sum())[0])

    return(t)


# get the args
args = parse_args()

# TODO: change this to just footpints when fixed in R script
footdir = 'footprints'

# make paths
mosaic_path = os.path.join(args.path, args.site, 'mosaic')
foot_path   = os.path.join(args.path, args.site, footdir)

# get names of footprints
footprints = [os.path.join(foot_path, f) for f in os.listdir(foot_path) if 'summary' not in f and '.xml' not in f]

# get the unique classes
nc = [os.path.join(mosaic_path, f) for f in os.listdir(mosaic_path) if '.nc' in f][0]
data = xr.open_dataset(nc)
labels = list(set(data.kmeans_label.data.flatten()))
labels.sort()

# emptyl ist
timeseries = []

# fill list
for foot in tqdm(footprints):
    timeseries.append(get_timestep(foot))

# make column names
cols = ['t'] + [str(l) for l in labels]
cols

# make timeseries into df
timeseries = pd.DataFrame(timeseries, columns=cols)
timeseries = timeseries.set_index('t')

# NA for bad data timesteps
timeseries.loc[(timeseries.values < 0).any(axis=1), :] = 'NA'

# print the missing data percentage
missing = 100 *len(timeseries.loc[(timeseries.values == 'NA').any(axis=1)]) / len(timeseries)
print(f'{missing}\% of the footprint files are bunk.')


# %%
