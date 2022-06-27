+ Visit [NEON data explorer](https://data.neonscience.org/data-products/explore) and determine what months to use.
    - For each site we noted months where hyperspectral reflectance was gathered.
        + __TALL__ 
            - No hyperspectral was collected in 2020, but we will just use 2019's collection for that year.
            - `flux_dates` - [['2018-04', '2018-05'], ['2019-04', '2019-05'], ['2020-04', '2020-05'], ['2021-04', '2021-05']]
        
        + __TEAK__ 
            - No hyperspectral was collected in 2020, but we will just use 2019's collection for that year.
            - `flux_dates` - [['2018-06', '2018-07'], ['2019-06', '2019-07'], ['2020-06', '2020-07'], ['2021-06', '2021-07']]

+ Download AOP and hyperspectral using `get_flux.R`
    - `get_flux.R` was run for each two month pair for a given year of date where flux data was available.


+ select sample of half hour observations based on 
    - valid footprint
    - flux data exists
    - stratification
        + cluster observations based on
            - u*
            - Obukhov length
            - stdev of cross and horizontal wind speed


# --------------

1. Downloaded bundled eddy flux data (DP4.00200.001) for the years 2018-2021 for selected sites (using `get_flux.R`, which is based on `neonUtilities`, and `download.sh` which was generated in `site_download_and_qfqm_check.ipynb`)
2. For each site, counted the number of half-hour observations in which footprint calculations and NSAE for CO$_{2}$, H$_{2}$O, and temperature all passed the final QAQC tests.  Dates and sites with valid observations are listed in table \ref{make_table_from_df} along with the number of valid observations of each metric. 17,662 observations, across 27 sites fit these criteria. Selecting only for sites with more than 100 observations we end up with 17,643 observations across 24 sites.


