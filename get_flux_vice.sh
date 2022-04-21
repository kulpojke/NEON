#!/bin/sh

SITE=$1
STARTDATE=$2
ENDDATE=$3
APITOKEN=$4
SAVEPATH=$5

# run the app
echo " "
echo " "
echo "---------------------------------------"
echo " "
echo "$SAVEPATH is mounted as /out and ..."

Rscript /work/get_flux.R $SITE $STARTDATE $ENDDATE $APITOKEN /out
