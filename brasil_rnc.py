#!/usr/bin/python
"""Script to process the HTML Brasilian RNC charts list and convert it to the XML catalog format
Part of the ChartCatalogs project
Copyright (c) 2015 Pavel Kalian
Licensed under GPLv2 or, at yoir will later version
"""


import sys
from HTMLParser import HTMLParser
from ChartCatalogs import Chart, RncChartCatalog
from datetime import datetime
import codecs

class BrasRNCHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inColumn = False
        self.chart = None
        self.column = 0
        self.base_url = ''
        self.catalog = RncChartCatalog()
        self.catalog.title = "Brasil RNC Charts"

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.chart = Chart()
            self.chart.chart_format = 'Sailing Chart, International Chart'
        elif tag == 'td':
            self.inColumn = True
            self.column += 1
        elif tag == 'a' and self.inColumn and self.column == 3:
            for attr in attrs:
                if attr[0] == 'href':
                    self.chart.url = self.base_url + attr[1]

    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.chart.is_valid():
                self.catalog.add_chart(self.chart)
            self.column = 0
        elif tag == 'td':
            self.inColumn = False

    def handle_data(self, data):
        if self.inColumn:
            if self.inColumn:
                if self.column == 1:
                    self.chart.number = data.strip()
                if self.column == 2:
                    self.chart.title = data.strip()
                if self.column == 4:
                    try:
                        self.chart.zipfile_ts = datetime.strptime(data.strip(), '%d/%m/%Y')
                    except:
                        pass
                if self.column == 5:
                    self.chart.ntm_edition_last_correction = data.strip()

    def print_xml(self):
        self.catalog.print_xml(True)

if len(sys.argv) < 2:
    print 'ERROR: Filename parameter missing'
if len(sys.argv) < 3:
    print 'ERROR: Base URL parameter is missing'
    print 'Usage brasil_rnc.py <filename> <base url>'
    exit(1)


# instantiate the parser and fed it some HTML
f = codecs.open(sys.argv[1], 'r', 'utf-8')
parser = BrasRNCHTMLParser()
parser.base_url = sys.argv[2]
parser.feed(f.read())
parser.print_xml()
