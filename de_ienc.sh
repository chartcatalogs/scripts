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

CATALOGNAME='DE_IENC_Catalog.xml'

WORKDIR='/tmp'
if wget -q -P ${WORKDIR} https://www.elwis.de/DE/dynamisch/IENC/enc-dateien/ienc_feed.xml; then
  ./de_ienc.py ${WORKDIR}/ienc_feed.xml > ${WORKDIR}/${CATALOGNAME}
  if xmllint --noout ${WORKDIR}/${CATALOGNAME} 2>&1 >/dev/null; then
    cat ${WORKDIR}/${CATALOGNAME} | xmllint --format - >  ${TARGETDIR}/${CATALOGNAME}
    rm ${WORKDIR}/${CATALOGNAME}
  fi
fi

