FROM r-base:4.1.3

# install apt packages
RUN apt-get update \
    && apt install -y \
    parallel \
    software-properties-common \
    apt-utils \
    libgdal-dev \
    libgeos++-dev \
    libudunits2-dev \
    libproj-dev \
    libx11-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libfreetype6-dev \
    libnode-dev \
    libxt-dev \
    libfftw3-dev

# install R packages
RUN R -e "install.packages('BiocManager'); \
    install.packages('devtools'); \
    install.packages('neonUtilities'); \
    install.packages('parallel'); \
    install.packages('raster'); \
    install.packages('rgdal'); \
    BiocManager::install('rhdf5')"

# make working and output directories
WORKDIR /home/work/out

# create a non-root user
RUN useradd -ms /bin/bash notroot

# change ownership
RUN chown -R notroot /home/work

# switch user
USER notroot

# change workdir
WORKDIR /home/work

# copy files
COPY get_flux.sh .
COPY get_flux.R .

# change permisions
USER root
RUN chmod -R 777 /home/work/get_flux.sh && \
    chmod 777 /home/work/get_flux.R && \
    chmod -R 777 /home/work/out
USER notroot

ENTRYPOINT ["/home/work/get_flux.sh"]






