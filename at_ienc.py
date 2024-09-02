#!/usr/bin/python
"""Script to process the Atom feed of the Austrian IENC charts list and convert it to the XML catalog format
Part of the ChartCatalogs project
Copyright (c) 2024 Pavel Kalian
Licensed under GPLv2 or, at yoir will later version
"""


import sys
from ChartCatalogs.RncChartCatalog import RncChartCatalog
from ChartCatalogs.Chart import Chart
from datetime import datetime
import xml.etree.ElementTree as ET
import dateutil.parser

catalog = RncChartCatalog()
catalog.title = "AT IENC Charts"

xmldoc = ET.parse(sys.argv[1])

feed = xmldoc.getroot()

for entry in feed.find('channel').findall('item'):
    chart = Chart()
    chart.chart_format = 'Sailing Chart, International Chart'
    chart.url = entry.find('link').text
    chart.number = entry.find('guid').text
    chart.title = entry.find('title').text
    chart.zipfile_ts = dateutil.parser.parse(entry.find('pubDate').text)
    catalog.add_chart(chart)

catalog.print_xml(True)

