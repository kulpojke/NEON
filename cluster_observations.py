
# %%
from turtle import st
import h5py
import os
import pandas as pd
import numpy as np


# %%
site = 'TEAK'
file_path = f'/media/data/NEON/{site}/filesToStack00200'
files = [os.path.join(file_path, f) for f in os.listdir(file_path) if '.h5' in f]


# %%
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

# %%

# open the files
for f in files[:1]:
    with h5py.File(f, 'r') as h:
        # get stat table
        stat = h[site]['dp04']['data']['foot']['stat']

        vals = []

        for row in stat:
            vals.append(
                [item.decode(encoding='utf-8')
                if isinstance(b, np.bytes_)
                else item
                for item in row]
            )

        d = pd.DataFrame(vals, columns=cols)

    dfs.append(d)

# %%
