#!/bin/sh

SITE=$1
STARTDATE=$2
ENDDATE=$3
APITOKEN=$4
SAVEPATH=$5


docker run --rm -it -u $(id -u):$(id -g)  -v $SAVEPATH:/home/work/out -w /home/work quay.io/kulpojke/neon:flux-latest $SITE $STARTDATE $ENDDATE $APITOKEN $SAVEPATH

# ./start_get_flux.sh TEAK 2021-06 2021-07 $TOKEN /media/data/NEON/TEAK

# ./start_get_flux.sh TALL 2018-04 2018-05 $TOKEN /media/data/NEON/TALL
# ./start_get_flux.sh TALL 2019-04 2019-05 $TOKEN /media/data/NEON/TALL
# ./start_get_flux.sh TALL 2020-04 2020-05 $TOKEN /media/data/NEON/TALL
# ./start_get_flux.sh TALL 2021-04 2021-05 $TOKEN /media/data/NEON/TALL

# ./start_get_flux.sh SJER 2019-03 2019-04 $TOKEN /media/data/NEON/SJER
# ./start_get_flux.sh SJER 2020-03 2020-04 $TOKEN /media/data/NEON/SJER
# ./start_get_flux.sh SJER 2021-03 2021-04 $TOKEN /media/data/NEON/SJER