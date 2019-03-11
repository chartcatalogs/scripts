#!/usr/bin/python
"""Script to process the NOAA JSON MBtiles catalog and convert it to the XML catalog format
Part of the ChartCatalogs project
Copyright (c) 2019 Pavel Kalian
Licensed under GPLv2 or, at yoir will later version
"""


import sys
from ChartCatalogs import Chart, RncChartCatalog
from datetime import datetime
import dateutil.parser
import json

catalog = RncChartCatalog()
catalog.title = 'NOAA Raster Charts MBTiles'

with open(sys.argv[1]) as f:
    data = json.load(f)
    for tileset in data['quilted_tilesets']:
        chart = Chart()
        chart.chart_format = 'Sailing Chart, International Chart'
        chart.url = "https:%s" % data['quilted_tilesets'][tileset]['url']
        chart.number = data['quilted_tilesets'][tileset]['name'][-2:]
        chart.title = "%s [%i MB]" % (data['quilted_tilesets'][tileset]['description'], data['quilted_tilesets'][tileset]['size'])
        chart.zipfile_ts = dateutil.parser.parse(data['quilted_tilesets'][tileset]['updated'])
        catalog.add_chart(chart)

catalog.print_xml(True)

