#!/usr/bin/python
"""Script to process the JSON feed of the Dutch IENC charts list and convert it to the XML catalog format
Part of the ChartCatalogs project
Copyright (c) 2019-2023 Marcel Verpaalen
Licensed under GPLv2 or, at your will later version
"""

import sys
from ChartCatalogs.RncChartCatalog import RncChartCatalog
from ChartCatalogs.Chart import Chart
from datetime import datetime
import json
from urllib.request import urlopen
import re

catalog = RncChartCatalog()
catalog.title = "Netherlands Inland ENC Charts"

with open(sys.argv[1]) as f:
    data = json.load(f)
    cnt = 0
    for tileset in data:
        chart = Chart()
        chart.chart_format = 'Sailing Chart, International Chart'
        chart.url = "https://vaarweginformatie.nl/fdd/main/wicket/resource/org.apache.wicket.Application/downloadfileResource?fileId=%s" % tileset['fileId']
        chart.number = "%s" % cnt
        chart.title = "%s" % tileset['name']
        chart.zipfile_ts = datetime.fromtimestamp(tileset['date']/1000)
        chart.target_filename = "%s.zip" % tileset['name']
        try:
            response = urlopen(chart.url)
            d = response.headers['content-disposition']
            filename = re.findall("filename=\"(.+)\"", d)[0]
            if filename is not None:
                chart.target_filename = filename
        except Exception:
            pass
        catalog.add_chart(chart)
        cnt = cnt + 1

catalog.print_xml(True)
