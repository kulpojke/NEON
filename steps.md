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

3. **Determine needed Principal components and clusters** - (`hyperspectral_n_k_determination.ipynb`)

For each year, for each site:

+ 0.2% of pixels were randomly sampled from each hyperspectral reflectance file from the first year with available data.

+ Bands with H2O or CO2 absorption issues were dropped (need way more info about this)

+ Data was scaled using sklearn.preprocessing.StandardScaler \cite_{sklearn}.

+ PCA was performed on the sample.

Then:

+ Cumulative explained variance ratio for all site-years was plotted.

+ The number of principal components ,_n_=3,  to use was selected by inspecting the plot. _n_ was selected such that greater than 95% of the variance was explained for all site-years, and if reasonable, the slope of the  cumulative explained variance ratio was beginning to level off for all site-years.

+ In notebooks (`hyperspectral_mosaic_notebooks`) for several different sites Within-Cluster Sum of Square (WCSS) was plotted for various numbers of clusters using _n_ components.  The elbow method was used to determine the number of clusters, _k_=3. (__Maybe go back and plot them all like you did for *n*__)

+ this step failed for DCSF and HARV, so they were omitted from this step of the analysis.


3. **Built hyperspectral mosaic** - (this happens for each site in `build_hyper_mosaic.py`)  Performs pca and kmeans clustering then assembles the mosaic tiles into large tiffs and a netCDF. For each site:

+ 0.2% of pixels were randomly sampled from each hyperspectral reflectance file from the first year with available data.

+ Bands with H2O or CO2 absorption issues were dropped (need way more info about this)

+ Data was scaled using sklearn.preprocessing.StandardScaler \cite_{sklearn}.

+ the sampled pixels were then used to train the PCA model (sklearn.decomposition.PCA) using $n=3$ components.

+ Kmeans clustering was then performed using the three pca components.

+ 

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


 # Bib #

@article{sklearn,
 title={Scikit-learn: Machine Learning in {P}ython},
 author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V.
         and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P.
         and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and
         Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
 journal={Journal of Machine Learning Research},
 volume={12},
 pages={2825--2830},
 year={2011}
}


# NOTES # 

+ Though the Konza Prairie site is abbreviated KONA, the abbreviation used in the files is KONZ.  Thus I changed the name of the Directory to match.