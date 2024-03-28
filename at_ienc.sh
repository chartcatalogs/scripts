#!/bin/bash

# Script to download German IENC charts list and convert it to the XML catalog format 
#
# Part of the ChartCatalogs project
# Copyright (c) 2024 Pavel Kalian
# Licensed under GPLv2 or, at your will later version
#

if [ -z "${CHARTCATALOGS_TARGETDIR}" ]; then
  TARGETDIR='.'
else
  TARGETDIR="${CHARTCATALOGS_TARGETDIR}"
fi

CATALOGNAME='AT_IENC_Catalog.xml'

WORKDIR='/tmp'
rm -f ${WORKDIR}/ienc_feed.xml
if wget -q -P ${WORKDIR} https://www.doris.bmk.gv.at/inland-encs/downloads/inland-encs-inland-ecdis-standard-24/rss.xml; then
  ./at_ienc.py ${WORKDIR}/rss.xml > ${WORKDIR}/${CATALOGNAME}
  if xmllint --noout ${WORKDIR}/${CATALOGNAME} 2>&1 >/dev/null; then
    cat ${WORKDIR}/${CATALOGNAME} | xmllint --format - >  ${TARGETDIR}/${CATALOGNAME}
    rm ${WORKDIR}/${CATALOGNAME}
  fi
fi

