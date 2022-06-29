#!/bin/sh

SITE=$1
STARTDATE=$2
ENDDATE=$3
APITOKEN=$4
SAVEPATH=$5


docker run --rm -it -u $(id -u):$(id -g)  -v $SAVEPATH:/home/work/out -w /home/work quay.io/kulpojke/neon:flux-latest $SITE $STARTDATE $ENDDATE $APITOKEN $SAVEPATH

# e.g.
# ./start_get_flux.sh TEAK 2021-06 2021-07 $TOKEN /media/data/NEON/TEAK

