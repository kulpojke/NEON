+ select sample of half hour observations based on 
    - valid footprint
    - flux data exists
    - stratification
        + cluster observations based on
            - u*
            - Obukhov length
            - stdev of cross and horizontal wind speed


# --------------

1. **Downloaded bundled eddy flux data** - Downloaded bundled eddy flux data (DP4.00200.001) and the hyperspectral data (DP3.30006.001) for the years 2018-2021 for selected sites (using `get_flux.R`, which is based on `neonUtilities`, and `download.sh` which was generated in `site_download_and_qfqm_check.ipynb`)
```
NEON
|__SITE
   |__footprints
      |__20180510T233000Z.tiff
      |__ ...
      |__20180731T233000Z.tiff
      |__summary.tiff
```

2. **Make file of valid flux observations for each site** - For each site, counted the number of half-hour observations in which footprint calculations and NSAE for CO$_{2}$, H$_{2}$O, and temperature all passed the final QAQC tests.  Dates and sites with valid observations are listed in table \ref{make_table_from_df} along with the number of valid observations of each metric. 17,662 observations, across 27 sites fit these criteria. Selecting only for sites with more than 100 observations we end up with 17,643 observations across 24 sites.  For each site with more than 100 valid observations a file was created (`flux_data.csv`) with the metrics used in footprint calculations and NSAE for CO$_{2}$, H$_{2}$O and T. (this step happens in `site_download_and_qfqm_check.ipynb`).

```
NEON
|__SITE
   |__flux_data.csv
   |
   |__footprints
      |__20180510T233000Z.tiff
      |__ ...
      |__20180731T233000Z.tiff
      |__summary.tiff
```

3. **Built hyperspectral mosaic** - (this happens for each site in `hyperspectral_mosaic_SITE.ipynb`)

```
NEON
|__TALL
   |__flux_data.csv
   |
   |__footprints
   |  |__20180510T233000Z.tiff
   |  |__ ...
   |  |__20180731T233000Z.tiff
   |  |__summary.tiff
   |
   |__mosaic
   |   |__2018
   |   |  |__TALL_2018_kmeans_mosaic.tiff
   |   |  |__TALL_2018_pca_mosaic.tiff
   |   |  |__TALL_2018_mosaic.nc
   |   |
   |   |__...
   |   |  |__ ...
   |   |
   |   |__2021
   |      |  |__TALL_2018_kmeans_mosaic.tiff
   |      |  |__TALL_2018_pca_mosaic.tiff
   |      |  |__TALL_2018_mosaic.nc
   |
   |__pca
      |__2018
      |  |__TALL_460000_3642000_pca.tiff
      |  |__ ...
      |  |__TALL_466000_3648000_pca.tiff
      |
      |__...
      |  |__ ...
      |
      |__2021
         |  |__TALL_460000_3642000_pca.tiff
         |  |__ ...
         |  |__TALL_466000_3648000_pca.tiff
```
4. **Quantize the footprints** - (`Quantize footprint.py`)

5. Revisit giannico method ipynbs