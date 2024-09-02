#!/usr/bin/python
"""Script to process the HTML Danube IENC charts list and convert it to the XML catalog format
Part of the ChartCatalogs project
Copyright (c) 2021 Pavel Kalian
Licensed under GPLv2 or, at yoir will later version
"""


import sys
from html.parser import HTMLParser
from ChartCatalogs.RncChartCatalog import RncChartCatalog
from ChartCatalogs.Chart import Chart
from datetime import datetime
import codecs
from pprint import pprint

class DanubeIENCHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inColumn = False
        self.chart = None
        self.column = 0
        self.row = 0
        self.base_url = ''
        self.catalog = RncChartCatalog()
        self.catalog.title = "Danube IENC Charts"
        self.inLink = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.chart = Chart()
            self.chart.chart_format = 'Sailing Chart, International Chart'
        elif tag == 'td':
            self.inColumn = True
            self.column += 1
        elif tag == 'a' and self.inColumn and self.column == 7:
            for attr in attrs:
                if attr[0] == 'href':
                    self.chart.url = self.base_url + attr[1]
        elif tag == 'a' and self.inColumn and self.column == 2:
              for attr in attrs:
                  if attr[0] == 'href':
                      self.inLink = True;

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.chart.number = "Base" + str(self.row)
            if self.row > 0 and self.chart.is_valid():
                self.catalog.add_chart(self.chart)
            else:
                if self.row > 0:
                    print("<!-- unavailable/invalid?")
                    pprint(vars(self.chart))
                    print("-->")
            self.column = 0
            self.row += 1
        elif tag == 'td':
            self.inColumn = False

    def handle_data(self, data):
        if self.inColumn:
            if self.inColumn:
                if self.column == 2:
                    self.chart.title = data.strip()
                if self.column == 3:
                    self.chart.title += " " + data.strip()
                if self.column == 7:
                    if self.inLink and data.strip() != '':
                        self.chart.title = data.strip()
                        self.inLink = False
                if self.column == 6:
                    try:
                        self.chart.zipfile_ts = datetime.strptime(data.strip(), '%Y-%m-%d')
                    except:
                        self.chart.zipfile_ts = datetime.strptime("1900-01-01", '%Y-%m-%d')
                        pass
                if self.column == 5:
                    self.chart.ntm_edition_last_correction = "0"

    def print_xml(self):
        self.catalog.print_xml(True)

if len(sys.argv) < 2:
    print('ERROR: Filename parameter missing')
if len(sys.argv) < 3:
    print('ERROR: Base URL parameter is missing')
    print('Usage danube_ienc.py <filename> <title>')
    exit(1)


# instantiate the parser and fed it some HTML
f = codecs.open(sys.argv[1], 'r', 'utf-8')
parser = DanubeIENCHTMLParser()
#parser.base_url = sys.argv[2]
parser.catalog.title = sys.argv[2]
parser.feed(f.read())
parser.print_xml()
