Equation numbers follow aubinet2012, as does everything unless otherwise cited.

## The eddy flux method
Eddy covariance measurements are generally made in the surface boundary layer where turbulent flux is the largest driver of vertical transport and there tends to be relatively little variation of flux with height \cite{aubinet2012, foken2008}.

### Reynolds Decomposition
(follows \cite{aubinet2012}) Reynolds decomposition allows for the partitioning of the time series of each variable $\zeta$ into it mean with repect to time, $\overline{\zeta}$, and a fluctuating part $\zeta^{\prime}$:

$$ \zeta = \overline{\zeta} + \zeta^{\prime} $$ (1.1a)

where:

$$ \zeta^{\prime} = \frac{1}{T} \int_{T}^{t+T}\zeta(t)\,dt $$ (1.1b)

The following rules , known as the Reynolds postulates, for averaging are required to calculate the turbulent value, $\zeta^{\prime}$:

$$  
\mathrm{i} \:\:\:\:\:\:\:\: \overline{\zeta^{\prime}} = 0 \\
\mathrm{ii} \:\:\:\:\:\:\:\: \overline{\zeta\xi} = \bar{\zeta} \, \bar{\xi} + \overline{\zeta^{\prime}\xi^{\prime}} \\
\mathrm{iii} \:\:\:\:\:\:\:\: \overline{\bar{\zeta} \, \xi} = \bar{\zeta} \, \bar{\xi} \\
\mathrm{iv} \:\:\:\:\:\:\:\: \overline{a\zeta} = a \, \bar{\zeta} \\
\mathrm{v} \:\:\:\:\:\:\:\: \overline{\zeta+ \xi} = \bar{\zeta} + \bar{\xi}
$$ (1.2)

Where $a$ is a constant and $\xi$ is a second variable.

The rules can be described as: 
(i) the mean turbulent fluctuation is zero;
(ii) the mean product of two variables is the product of the means plus the mean of the product of the fluxes;
(iii) the mean of  one variable's mean times a second variable, is just the product of the means of both variables;
(iv) the product of a constant and a variable is the constant times the mean of the variable;
(v) the mean of the sum of two variables is the sum of their means.

The application of the Reynolds postulates relies on the assumption of ergodicity,i.e. that the time average is related to the spacial average. This requires that the fluctuations are statistically stationary over the averaging time. (TODO: should I explain this more?)

### Section in the book called Scalar Definition
Variables commonly used in literature to describe an atmospheric constituent $s$:
+ density ( $\rho_{s}, \mathrm{kg \; m^{-3}}$ ) 
+ molar concentration ($c_{s}, \mathrm{mol \; m^{-3}}$)
+ mole fraction ($\mathrm{mol \; mol^{-1}}$) is the number of moles of $s$ per total number of moles in the mixture or equivalently partial pressure of $s$ divided by total pressure.
+ molar mixing ratio ( $\Chi_{s,m} \, , \mathrm{mol \; mol^{-1}}$ ) is the ratio of moles $s$ to moles dry air.
+ mass mixing ratio ( $\Chi_{s} \, , \mathrm{kg \; kg^{-1}}$ )

Of the above quantities, changes in temperature, pressure and water vapor content change all but molar mass and the mass mixing ratios.  This is of importance to note because inthe field density and molar concentration which do change  with temperature, pressure and water vapor content \cite{kowalski2007}.  Correction is needed to discern fluctuations in these quantities  caused by changes in temperature, pressure, and water vapor content from those caused by production, absorption and transport of the constituent.

__Table 1.2 in this book has conversions between these quantitites__


### One point conservation equations
The following equation describes the conservation of a scalar or vector quantity, $\zeta$ in the atmosphere at a given instant and point:

$$
\frac{\partial \rho_{d} \; \zeta}{\partial t} +
\vec{\nabla} (\vec{u} \, \rho_{d} 0\; \zeta) +
K_{\zeta} \, \Delta(\rho_{d} \; \zeta) =
S_{\zeta} 
$$ (1.3)

where:
+ $\vec{u}$ is the wind velocity vector,
+ $\vec{\nabla}$ is the divergence operator 
 
 $$ \vec{\nabla} = (\frac{\partial}{\partial x},
\frac{\partial}{\partial y},
\frac{\partial}{\partial z} ) $$

+ $\Delta$ is the Laplacian operator
+ 
$$ \Delta = (\frac{\partial^{2}}{\partial x^{2}} +
\frac{\partial^{2}}{\partial y^{2}} +
\frac{\partial^{2}}{\partial z^{2}} ) $$

+ $\rho_{d}$ is the dry air density,
+ $K_{\zeta}$ is the molecular diffusivity of $\zeta$,
+ and $S_{\zeta}$ is the magnitude of the source or sink of $\zeta$

equation  2a can be described as: 

rate of change of ${\zeta}$ + diffusion + transport = production or consumption

If:
+ $\zeta = 1$, equation 2a becomes the continuity equation (dry air mass)(eq1.4 and by applying the time averaging operator eq 1.5),

$$
\frac{\partial \rho_{d}}{\partial t} + 
\vec{\nabla} (\vec{u} \, \rho_{d}) = 0
$$ (1.4)

$$
\frac{\overline{\partial \rho_{d}}}{\partial t} + 
\vec{\nabla} (\overline{\vec{u} \, \rho_{d}}) = 0
$$ (1.5)


+ $\zeta =$ air enthalpy,  equation 2a becomes the enthalpy conservation equation,

+ $\zeta =$ mixing ratio of a component, equation 2a becomes the scalar conservation equation,

+ $\zeta =$ a component of the wind velocity vector in a given direction, $u_{i}$, equation 2a becomes the conservation of that momentum component. In this case $S_{i}$ refers to  forces, such as drag, Coriolis forces, pressure gradients, etc... as those are the sources or sinks of momentum. 
$$
\frac{\partial \rho_{d} \, u_{i}}{\partial t} + 
\vec{\nabla} (\vec{u} \, \rho_{d} \, u_{i}) = S_{i}
$$ (1.6)

+ "The three equations describing the momentum conservation in the three directions constitute the Navier Stokes equations"

# NEON.DOC.004571

Variables found in `'SITE/dp04/data/foot/stat/` for a given site \cite{NEON_DOC_004571}.

+ `timeBgn` - Observation start time.

+ `timeEnd` -  Observation end time.

+ `angZaxsErth` -  Wind direction.

+ `distReso` - Footprint matrix cell size.
  - Set equal to relative measurement height above displacement, and rounded to 10 m.

+ `veloYaxsHorSd` - Standard deviation of the cross-wind velocity.

+ `veloZaxsHorSd` - Standard deviation of the vertical velocity.

+ `veloFric` - Friction Velocity (often denoted $u*$)

+ `distZaxsMeasDisp` - Relative measurement height above displacement.

+ `distZaxsRgh` - Roughness length.
  - Calculated via call to eddy4R.turb::def.dist.rgh() )

+ `distZaxsAbl` - Boundary layer height.
  - Set to 1000 m by default.

+ `distXaxs90` - Along-wind distance of the 90 percent crosswind-integrated cumulative footprint.

+ `distXaxsMax` - Along-wind distance of contribution peak.

+ `distYaxs90` - One-sided cross-wind distance of the 90 percent along-wind integrated cumulative footprint.

## Calculations of fluxes


# Methods (as in my methods)

## Sample selection

Samples were selected following the basic procedure used by Gianccico et al. \cite{giannico2018}, but with some modification.  Half-hourly observations of CO$_{2}$ NSAE with no missing values and no bad quality control flags were first selected from the bundled eddy covariance data \cite{NEON_DP4_00200_001}.  The observations were then labeled by wind direction sector and assigned to a cluster based on input variables of the footprint model. __The number of sectors varied from site to site based on the distribution of wind direction and how many observations were available for a given sector__.

Clustering of observations was done with an unsupervised Gaussian Mixture Model using `sklearn.mixture.GaussianMixture` \cite{scikit2011}.  The number of clusters was selected automatically by maximizing the Silhouette Coefficient \cite{rousseeuw1987},

Once observations had been assigned a sector and a cluster a two level stratified sample was selected first by sector, then by cluster. For each site a number of samples was selected in order to have a somewhat balanced representation of observations from the different sectors and cluster while maintaining as large a sample size as possible. 

*__How about instead we just__*
+ calculate the metrics for each 95 percent footprint and see how they corelate with flux
+ post hoc look at the clusters to see what effect they have

Once we have an idea about the effects of these things
+ pick a subsample for which to calculate soil flux
+ look at T and soil moisture effects

# Refs

@book{aubinet2012,
  title={Eddy covariance: a practical guide to measurement and data analysis},
  author={Aubinet, Marc and Vesala, Timo and Papale, Dario},
  year={2012},
  publisher={Springer Science \& Business Media}
}

@book{foken2008,
  title={Micrometeorology},
  author={Foken, Thomas and Napo, Carmen J},
  volume={308},
  year={2008},
  publisher={Springer}
}

@article{giannico2018,
  title={Contributions of landscape heterogeneity within the footprint of eddy-covariance towers to flux measurements},
  author={Giannico, Vincenzo and Chen, Jiquan and Shao, Changliang and Ouyang, Zutao and John, Ranjeet and Lafortezza, Raffaele},
  journal={Agricultural and Forest Meteorology},
  volume={260},
  pages={144--153},
  year={2018},
  publisher={Elsevier}
}

@article{kowalski2007,
  title={On the relationship between the eddy covariance, the turbulent flux, and surface exchange for a trace gas such as CO2},
  author={Kowalski, Andrew S and Serrano-Ortiz, Pen{\'e}lope},
  journal={Boundary-layer meteorology},
  volume={124},
  number={2},
  pages={129--141},
  year={2007},
  publisher={Springer}
}

@misc{NEON_DP4_00200_001,
  doi = {10.48443/7CQP-3J73},
  url = {https://data.neonscience.org/data-products/DP4.00200.001/RELEASE-2022},
  author = {{National Ecological Observatory Network (NEON)}},
  keywords = {attitude, carbon dioxide (CO2), carbon-13 (13C), CO2 mixing ratio, CO2 molar fraction, eddy covariance (EC), energy balance, evapotranspiration (ET), flux, footprint, hydrogen-2 (2H), isotopes, latent heat, momentum, motion, net ecosystem exchange (NEE), net surface atmosphere exchange (NSAE), oxygen-18 (18O), profile, sensible heat, stable isotopes, storage, turbulence, water (H2O) mixing ratio, water (H2O) molar fraction, water (H2O) vapor, wind direction, wind speed},
  language = {en},
  title = {Bundled data products - eddy covariance (DP4.00200.001)},
  publisher = {National Ecological Observatory Network (NEON)},
  year = {2022}
}

@techreport{NEON_DOC_004571,
  author={Metzger, S., Durden, D., Florian, C., Luo, H., Pingintha-Durden, N., and Xu, K.},
  title={Algorithm theoretical basis document: eddy-covariance data products bundle},
  institution={National Ecological Observatory Network},
  year={2018},
  number={Revision A (2018-04-30)},
  address={Boulder, U.S.A.},
  month={04},
  note={http://data.neonscience.org/documents}
}

@article{rousseeuw1987,
  title={Silhouettes: a graphical aid to the interpretation and validation of cluster analysis},
  author={Rousseeuw, Peter J},
  journal={Journal of computational and applied mathematics},
  volume={20},
  pages={53--65},
  year={1987},
  publisher={Elsevier}
}

@article{scikit2011,
  title={Scikit-learn: Machine learning in Python},
  author={Pedregosa, Fabian and Varoquaux, Ga{\"e}l and Gramfort, Alexandre and Michel, Vincent and Thirion, Bertrand and Grisel, Olivier and Blondel, Mathieu and Prettenhofer, Peter and Weiss, Ron and Dubourg, Vincent and others},
  journal={Journal of machine learning research},
  volume={12},
  number={Oct},
  pages={2825--2830},
  year={2011}
}