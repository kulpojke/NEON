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
echo "$SAVEPATH is mounted as /home/work/out and ..."

Rscript /home/work/get_flux.R $SITE $STARTDATE $ENDDATE $APITOKEN /home/work/out
