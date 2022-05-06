
# %%
from matplotlib.pyplot import thetagrids
import h5py
import os
import pandas as pd
import numpy as np



# %%
site = 'TEAK'
file_path = f'/media/data/NEON/{site}/filesToStack00200'
files = [os.path.join(file_path, f) for f in os.listdir(file_path) if '.h5' in f]


# %%
'''
# get the units from meta (seems like there should be columns names, but no)
for f in files[:1]:
    with h5py.File(f, 'r') as h:
        # get stat table
        stat = h[site]['dp04']['data']['foot']['stat']
        units = [u.decode(encoding='utf-8') for u in stat.attrs['unit'][:]]

# make cols (TODO: double check, this is based on email from Dave Durden)
cols = ['timeBgn', 'timeEnd', 'AngZaxsErth', 'distReso', 'VeloYaxsHorSd', 'VeloZaxsHorSd', 'veloFric', 'distZaxsMeasDisp']

# make list for dfs
dfs = []
'''
# %%

def find_valid_observations(f):
    '''
    Reads footprint statistics from f,
    drops bad observations,
    then returns dataframe.
    '''
    # open the hdf
    hdf = pd.HDFStore(f)

    # get the flux quality flags
    qfqm_CO2 = hdf.get(f'{site}/dp04/qfqm/fluxCo2/nsae')

    # Select observations with no bad flags
    qfqm_CO2 = qfqm_CO2.loc[
        (qfqm_CO2.qfFinlStor == 0) &
        (qfqm_CO2.qfFinlTurb ==  0) &
        (qfqm_CO2.qfFinl == 0)
        ]
    # get the footprint input stats
    stat = hdf.get(f'{site}/dp04/data/foot/stat/')

    # only keep the ones for valid observations
    istat = stat.set_index('timeBgn').index
    iqfqm = qfqm_CO2.set_index('timeBgn').index
    good = stat[istat.isin(iqfqm)]

    hdf.close()

    return good


def find_sectors(stat, theta=10):
    '''
    Returns a df of timestamps and sectors of the mean wind direction
    '''

    # make sure theta goes into 360 an even number of times
    if 360 % theta != 0:
        while 360 % theta != 0:
            theta= theta + 1
        print(f'theta has been forced to {theta} for even division of 360')

    # set start angle, and empy list
    stat['sector'] = theta * (stat.angZaxsErth // theta)

    return stat[['timeBgn', 'sector']]


def get_sample_size(sectors):
    '''Returns sample size, based on smallest sector counts'''
    # check to see if all sectors are represented
    if len(sectors.sector.unique()) != 360 // θ:
        dif = ((360 // θ - len(sectors.sector.unique()))
                + sectors.sector.unique()[sectors.sector.unique() == 0.0].shape[0])
        print(f'Warning: There are no observations for {dif} sectors.')

    # find the 4 smallest sector counts
    four_small = np.sort(np.partition(sectors.sector.unique(), 4)[:5])

    # take the first bin count >= 20
    for i in range(5):
        if four_small[i] >= 20:
            sample_size = four_small[i]
            if i > 0:
                print(f'Warning: There are {i} underrepresented sectors.')
            break

    return sample_size


# %%
# degrees per sector
θ = 18
bins = int(360 / θ)

# make empty df
sectors = pd.DataFrame(columns=['timeBgn', 'sector'])

# fill df with timestamps and sectors of valid observations
for f in files:
    # find footprint stats of the valid observations
    stat = find_valid_observations(f)

    # find sectors in which observations lie
    sects = find_sectors(stat, theta=θ)

    # scrunch the latest observations onto the df
    sectors = pd.concat([sectors, sects], axis=0)

    # get the sample size
    sample_size = get_sample_size(sectors)






# %%
h = h5py.File(f, 'r')
# get stat table
#stat = h.get(f'{site}/dp04/data/foot/stat/')

# %%
h.close()
# %%
