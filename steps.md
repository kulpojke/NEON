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
