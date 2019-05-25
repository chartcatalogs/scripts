#!/bin/bash

# Script to download German IENC charts list and convert it to the XML catalog format 
#
# Part of the ChartCatalogs project
# Copyright (c) 2019 Pavel Kalian
# Licensed under GPLv2 or, at your will later version
#

if [ -z "${CHARTCATALOGS_TARGETDIR}" ]; then
  TARGETDIR='.'
else
  TARGETDIR="${CHARTCATALOGS_TARGETDIR}"
fi

CATALOGNAME='NOAA_MBTiles_Catalog.xml'

WORKDIR='/tmp'
rm -f ${WORKDIR}/mbtiles_catalog.json
if wget -q -P ${WORKDIR} https://tileservice.charts.noaa.gov/mbtiles/mbtiles_catalog.json; then
  ./noaa_mbtiles.py ${WORKDIR}/mbtiles_catalog.json > ${WORKDIR}/${CATALOGNAME}
  if xmllint --noout ${WORKDIR}/${CATALOGNAME} 2>&1 >/dev/null; then
    cat ${WORKDIR}/${CATALOGNAME} | xmllint --format - >  ${TARGETDIR}/${CATALOGNAME}
    rm ${WORKDIR}/${CATALOGNAME}
  fi
fi

