


+ select sample of half hour observations based on 
    - valid footprint
    - flux data exists
    - stratification
        + cluster observations based on
            - u*
            - Obukhov length
            - stdev of cross and horizontal wind speed


# --------------

1. Downloaded bundled eddy flux data (DP4.00200.001) and the hyperspectral data (DP3.30006.001) for the years 2018-2021 for selected sites (using `get_flux.R`, which is based on `neonUtilities`, and `download.sh` which was generated in `site_download_and_qfqm_check.ipynb`)
2. For each site, counted the number of half-hour observations in which footprint calculations and NSAE for CO$_{2}$, H$_{2}$O, and temperature all passed the final QAQC tests.  Dates and sites with valid observations are listed in table \ref{make_table_from_df} along with the number of valid observations of each metric. 17,662 observations, across 27 sites fit these criteria. Selecting only for sites with more than 100 observations we end up with 17,643 observations across 24 sites.  For each site with more than 100 valid observations a file was created with the metrics used in footprint calculations and NSAE for CO$_{2}$, H$_{2}$O and T.


