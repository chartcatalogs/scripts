#!/usr/bin/python
"""Script to process the HTML Brasilian RNC charts list and convert it to the XML catalog format
Part of the ChartCatalogs project
Copyright (c) 2015 Pavel Kalian
Licensed under GPLv2 or, at yoir will later version
"""


import sys
from ChartCatalogs.RncChartCatalog import RncChartCatalog
from ChartCatalogs.Chart import Chart
from datetime import datetime
import codecs
from pprint import pprint
import requests
from bs4 import BeautifulSoup

def ProcessPage(catalog, page = 0):
    # URL of the webpage to parse
    url = "https://www.marinha.mil.br/chm/chm/dados-do-segnav/cartas-ienc?page={}".format(page)

    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the data
    table = soup.find('table')

    # Extract the data from the table
    table_data = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 2:
            chart = Chart()
            chart.chart_format = 'Sailing Chart, International Chart'
            chart.number = columns[0].get_text(strip=True)
            chart.title = columns[1].get_text(strip=True)
            chart.url = columns[2].find('a')['href']
            chart.zipfile_ts = datetime.strptime(columns[3].get_text(strip=True).strip(), '%d/%m/%Y')
            if len(chart.number) > 0:
                catalog.add_chart(chart)

catalog = RncChartCatalog()
catalog.title = "Brasil RNC Charts"
ProcessPage(catalog, 0)
ProcessPage(catalog, 1)
ProcessPage(catalog, 2)
catalog.print_xml(True)
