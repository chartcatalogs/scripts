"""ChartCatalog
Part of the ChartCatalogs project
Copyright (c) 2015 Pavel Kalian
Licensed under GPLv2 or, at yoir will later version
"""


from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

class RncChartCatalog:
    def __init__(self):
        self.charts = []
        self.title = ''
        self.created_ts = datetime.utcnow()
        self.valid_ts = datetime.utcnow()
        self.ref_spec = 'Subset of NOAA Rnc Product Catalog Technical Specifications'
        self.ref_spec_vers = '1.0'
        self.s62AgencyCode = '0';
        self.xml = None

    def xml_add_header(self):
        header = SubElement(self.xml, 'Header')
        t = SubElement(header, 'title')
        t.text = self.title.decode('UTF-8')
        t = SubElement(header, 'date_created')
        t.text = self.created_ts.strftime('%Y-%m-%d')
        t = SubElement(header, 'time_created')
        t.text = self.created_ts.strftime('%H:%M:%S')
        t = SubElement(header, 'date_valid')
        t.text = self.valid_ts.strftime('%Y-%m-%d')
        t = SubElement(header, 'time_valid')
        t.text = self.valid_ts.strftime('%H:%M:%S')
        t = SubElement(header, 'dt_valid')
        t.text = self.valid_ts.strftime('%Y-%m-%dT%H:%M:%SZ')
        t = SubElement(header, 'ref_spec')
        t.text = self.ref_spec
        t = SubElement(header, 'ref_spec_vers')
        t.text = self.ref_spec_vers
        t = SubElement(header, 's62AgencyCode')
        t.text = self.s62AgencyCode

    def xml_add_charts(self, chart_name_include_number):
        for chart in self.charts:
            chart.append_xml_element(self.xml, chart_name_include_number)

    def print_xml(self, chart_name_include_number = False):
        self.xml = Element('RncProductCatalogChartCatalogs')
        self.xml_add_header()
        self.xml_add_charts(chart_name_include_number)
        print tostring(self.xml)

    def add_chart(self, chart):
        self.charts.append(chart)
