#!/bin/bash

# Script to download Brasilian RNC charts list and convert it to the XML catalog format 
#
# Part of the ChartCatalogs project
# Copyright (c) 2015 Pavel Kalian
# Licensed under GPLv2 or, at yoir will later version
#
if [ -z "${CHARTCATALOGS_TARGETDIR}" ]; then
  TARGETDIR='.'
else
  TARGETDIR="${CHARTCATALOGS_TARGETDIR}"
fi

CATALOGNAME='BR_RNC_Catalog.xml'

WORKDIR='/tmp'
if wget -q -P ${WORKDIR} http://www.mar.mil.br/dhn/chm/box-cartas-raster/raster_disponiveis.html; then
  ./brasil_rnc.py ${WORKDIR}/raster_disponiveis.html http://www.mar.mil.br/dhn/chm/box-cartas-raster/ > ${WORKDIR}/${CATALOGNAME}
  if xmllint --noout ${WORKDIR}/${CATALOGNAME} 2>&1 >/dev/null; then
    mv ${WORKDIR}/${CATALOGNAME}  ${TARGETDIR}/${CATALOGNAME}
  fi
fi

if [ -f ${WORKDIR}/raster_disponiveis.html ]; then
  rm ${WORKDIR}/raster_disponiveis.html
fi
