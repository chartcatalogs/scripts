#!/usr/bin/python
"""Script to process the EURIS IENC charts list and convert it to the XML catalog format
Copyright (c) 2024 Transporter
Licensed under GPLv2 or, at yoir will later version
"""

import xml.etree.ElementTree as ET
import requests
import datetime
import zlib
from dateutil import parser

def create_xml_node(node_name, node_content):
    new_node = ET.Element(node_name)
    new_node.text = node_content
    return new_node

root = ET.Element("RncProductCatalogChartCatalogs")
header = ET.SubElement(root, "Header")
header.append(create_xml_node('title', 'EURIS IENC Charts'))
header.append(create_xml_node('date_created', datetime.datetime.now().strftime('%Y-%m-%d')))
header.append(create_xml_node('time_created', datetime.datetime.now().strftime('%H:%M:%S')))
header.append(create_xml_node('date_valid', datetime.datetime.now().strftime('%Y-%m-%d')))
header.append(create_xml_node('time_valid', datetime.datetime.now().strftime('%H:%M:%S')))
header.append(create_xml_node('dt_valid', datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')))
header.append(create_xml_node('ref_spec', 'Subset of NOAA Rnc Product Catalog Technical Specifications'))
header.append(create_xml_node('ref_spec_vers', '1.0'))
header.append(create_xml_node('s62AgencyCode', '0'))

response = requests.get('https://www.eurisportal.eu/AWFIENC/api/IENC/GetIENCOverviewList', headers={'accept': 'application/json'})
api_data = response.json()

# Let's sort the charts by cell name, it will put them together by area due to the standard cell numbering schema
api_data.sort(key=lambda x: x['name'], reverse=False)

for item in api_data:
    dt = parser.parse(item['filesModifiedDate'])
    chart = ET.SubElement(root, "chart")
    chart.append(create_xml_node('number', str(zlib.crc32(item['mapID'].encode('utf-8')))))
    area_name = ''
    if(len(item['areas']) > 0):
        area_name = item['areas'][0]['areaName']
    cell_name = item['name']
    chart.append(create_xml_node('target_filename', cell_name + ".zip"))
    cell_description = item['description']
    if cell_description.startswith(area_name):
        cell_name += " - {cd}".format(cd = cell_description)
    else:
        cell_name += " - {an} - {cd}".format(an = area_name, cd = cell_description)
    chart.append(create_xml_node('title', cell_name))
    chart.append(create_xml_node('format', 'Sailing Chart, International Chart'))
    chart.append(create_xml_node('zipfile_location', f"https://www.eurisportal.eu/AWFIENC/api/IENC/DownloadIENCMap?mapID={item['mapID']}"))
    chart.append(create_xml_node('zipfile_datetime', dt.strftime('%Y%m%d_%H%M%S')))
    chart.append(create_xml_node('zipfile_datetime_iso8601', dt.strftime('%Y-%m-%dT%H:%M:%SZ')))

tree = ET.ElementTree(root)
tree.write("EURIS_IENC_Catalog.xml", encoding='utf-8', xml_declaration=True)
