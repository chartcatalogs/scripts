#!/usr/bin/python
"""Script to process the Atom feed of the German IENC charts list and convert it to the XML catalog format
Part of the ChartCatalogs project
Copyright (c) 2019 Pavel Kalian
Licensed under GPLv2 or, at yoir will later version
"""


import sys
from ChartCatalogs import Chart, RncChartCatalog
from datetime import datetime
import xml.etree.ElementTree as ET
import dateutil.parser

catalog = RncChartCatalog()
catalog.title = "DE IENC Charts"

xmldoc = ET.parse(sys.argv[1])

feed = xmldoc.getroot()

for entry in feed.findall('{http://www.w3.org/2005/Atom}entry'):
    chart = Chart()
    chart.chart_format = 'Sailing Chart, International Chart'
    chart.url = entry.find('{http://www.w3.org/2005/Atom}id').text
    chart.number = entry.find('{http://www.w3.org/2005/Atom}link').attrib['title'][2:4]
    chart.title = entry.find('{http://www.w3.org/2005/Atom}title').text
    chart.zipfile_ts = dateutil.parser.parse(entry.find('{http://www.w3.org/2005/Atom}updated').text)
    catalog.add_chart(chart)

catalog.print_xml(True)

