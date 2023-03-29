#!/bin/bash

# Script to download the Netherlands IENC charts list and convert it to the XML catalog format 
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

CATALOGNAME='NL_IENC_Catalog.xml'

WORKDIR='/tmp'
rm -f ${WORKDIR}/nl_ienc_feed.json
if wget -q -P ${WORKDIR} https://vaarweginformatie.nl/frp/api/webcontent/downloads?pageId=infra/enc -O ${WORKDIR}/nl_ienc_feed.json; then
  ./nl_ienc.py ${WORKDIR}/nl_ienc_feed.json > ${WORKDIR}/${CATALOGNAME}
  if xmllint --noout ${WORKDIR}/${CATALOGNAME} 2>&1 >/dev/null; then
    cat ${WORKDIR}/${CATALOGNAME} | xmllint --format - >  ${TARGETDIR}/${CATALOGNAME}
    rm ${WORKDIR}/${CATALOGNAME}
  fi
fi

