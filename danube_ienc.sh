#!/bin/bash

# Script to download Brasilian RNC charts list and convert it to the XML catalog format 
#
# Part of the ChartCatalogs project
# Copyright (c) 2021 Pavel Kalian
# Licensed under GPLv2 or, at yoir will later version
#

#set -x

if [ -z "${CHARTCATALOGS_TARGETDIR}" ]; then
  TARGETDIR='.'
else
  TARGETDIR="${CHARTCATALOGS_TARGETDIR}"
fi

CATALOGNAME='BR_RNC_Catalog.xml'

function process_country() {
  CATALOGNAME="$1"
  URL="$2"
  TITLE="$3"

  WORKDIR='/tmp'
  if curl -f -o "${WORKDIR}/danube_ienc.html" "$URL"; then
    ./danube_ienc.py ${WORKDIR}/danube_ienc.html "${TITLE}" > ${WORKDIR}/${CATALOGNAME}
    if xmllint --noout ${WORKDIR}/${CATALOGNAME} 2>&1 >/dev/null; then
      cat ${WORKDIR}/${CATALOGNAME} | xmllint --format - >  ${TARGETDIR}/${CATALOGNAME}
      rm ${WORKDIR}/${CATALOGNAME}
    fi
  fi

  if [ -f ${WORKDIR}/danube_ienc.html ]; then
    rm ${WORKDIR}/danube_ienc.html
  fi
}

#process_country "AT_IENC_Catalog.xml" "https://www.danubeportal.com/charts/electronicChart/AT" "Austria IENC Charts"
process_country "SK_IENC_Catalog.xml" "https://www.danubeportal.com/charts/electronicChart/SK" "Slovakia IENC Charts"
process_country "HU_IENC_Catalog.xml" "https://www.danubeportal.com/charts/electronicChart/HU" "Hungary IENC Charts"
process_country "HR_IENC_Catalog.xml" "https://www.danubeportal.com/charts/electronicChart/HR" "Croatia IENC Charts"
process_country "RS_IENC_Catalog.xml" "https://www.danubeportal.com/charts/electronicChart/RS" "Serbia IENC Charts"
process_country "BG_IENC_Catalog.xml" "https://www.danubeportal.com/charts/electronicChart/BG" "Bulgaria IENC Charts"
process_country "RO_IENC_Catalog.xml" "https://www.danubeportal.com/charts/electronicChart/RO" "Romania IENC Charts"
