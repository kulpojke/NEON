## The eddy flux method
Eddy covariance methods are generally made in the surface boundary layer where turbulent flux is the largest driver of vertical transport and there tends to be relatively little variation of flux with height \cite{aubinet2012, foken2008}.

### Reynolds Decomposition
(follows \cite{aubinet2012}) Reynolds decomposition allows for the partitioning of the time series of each variable $\zeta$ into it mean with repect to time, $\overline{\zeta}$, and a fluctuating part $\zeta^{\prime}$:

$$ \zeta = \overline{\zeta} + \zeta^{\prime} $$ (1a)

where:

$$ \zeta^{\prime} = \frac{1}{T} \int_{T}^{t+T}\zeta(t)\,dt $$ (1b)

The following rules , known as the Reynolds postulates, for averaging are required to calculate the turbulent value, $\zeta^{\prime}$:

$$  
\mathrm{i} \:\:\:\:\:\:\:\: \overline{\zeta^{\prime}} = 0 \\
\mathrm{ii} \:\:\:\:\:\:\:\: \overline{\zeta\xi} = \bar{\zeta} \, \bar{\xi} + \overline{\zeta^{\prime}\xi^{\prime}} \\
\mathrm{iii} \:\:\:\:\:\:\:\: \overline{\bar{\zeta} \, \xi} = \bar{\zeta} \, \bar{\xi} \\
\mathrm{iv} \:\:\:\:\:\:\:\: \overline{a\zeta} = a \, \bar{\zeta} \\
\mathrm{v} \:\:\:\:\:\:\:\: \overline{\zeta+ \xi} = \bar{\zeta} + \bar{\xi}
$$ (1c)

Where $a$ is a constant and $\xi$ is a second variable.

The rules can be described as: 
(i) the mean turbulent fluctuation is zero;
(ii) the mean product of two variables is the product of the means plus the mean of the product of the fluxes;
(iii) the mean of  one variable's mean times a second variable, is just the product of the means of both variables;
(iv) the product of a constant and a variable is the constant times the mean of the variable;
(v) the mean of the sum of two variables is the sum of their means.

The application of the Reynolds postulates relies on the assumption of ergodicity,i.e. that the time average is related to the spacial average. This requires that the fluctuations are statistically stationary over the averaging time. (TODO: should I explaint this more?)

### Section in the book called Scalar Definition
Variables commonly used in literature to describe an atmospheric constituent $s$:
+ density ( $\rho_{s}, \mathrm{kg \; m^{-3}}$ ) 
+ molar concentration ($c_{s}, \mathrm{mol \; m^{-3}}$)
+ mole fraction ($\mathrm{mol \; mol^{-1}}$) is the number of moles of $s$ per total number of moles in the mixture or equivalently partial pressure of $s$ divided by total pressure.
+ molar mixing ratio ( $\Chi_{s,m} \, , \mathrm{mol \; mol^{-1}}$ ) is the ratio of moles $s$ to moles dry air.
+ mass mixing ratio ( $\Chi_{s} \, , \mathrm{kg \; kg^{-1}}$ )

Of the above quantities, changes in temperature, pressure and water vapor content change all but molar mass and the mass mixing ratios.  This is of importance to note because inthe field density and molar concentration which do change  with temperature, pressure and water vapor content \cite{kowalski2007}.  Correction is needed to discern fluctuations in these quantities  caused by changes in temperature, pressure, and water vapor content from those caused by production, absorption and transport of the constituent.

__Table 1.2 in this book has conversions between these quantitites__


### Onep point conservation equations
The following equation describes the conservation of a scalar or vector quantity, $\zeta$ in the atmosphere at a given instant and point:

$$
\frac{\partial \rho_{d} \; \zeta}{\partial t} +
\vec{\nabla} (\vec{u} \, \rho_{d} 0\; \zeta) +
K_{\zeta} \, \Delta(\rho_{d} \; \zeta) =
S_{\zeta} 
$$ (2a)

where:
+ $\vec{u}$ is the wind velocity vector,
+ $\vec{\nabla}$ is the divergence operator 
, $ (\frac{\partial}{\partial x},
\frac{\partial}{\partial y},
\frac{\partial}{\partial z} ) $,
+ $\Delta$ is the Laplacian operator
, $ (\frac{\partial^{2}}{\partial x^{2}} +
\frac{\partial^{2}}{\partial y^{2}} +
\frac{\partial^{2}}{\partial z^{2}} ) $,
+ $\rho_{d}$ is the dry air density,
+ $K_{\zeta}$ is the molecular diffusivity of $\zeta$,
+ and $S_{\zeta}$ is the magnitude of the source or sink of $\zeta$

equation  2a can be described as: 

rate of change of ${\zeta}$ + diffusion + transport = production or consumption

If:
+ $\zeta = 1$, equation 2a becomes the continutiy equation,

$$
\frac{\partial \rho_{d}}{\partial t} + 
\vec{\nabla} (\vec{u} \, \rho_{d} 0) = 0
$$ (2b)

+ $\zeta =$ air enthalpy,  equation 2a becomes the enthalpy conservation equation,

+ $\zeta =$ mixing ratio of a component, equation 2a becomes the scalar conservation equation,

+ $\zeta =$ a component of the wind velocity vector in a given direction equation 2a becomes the conservation of that momentum component.

$$

$$

+ "The three equations describing the momentum conservation in the three directions constitute the Navier Stokes equations"

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
