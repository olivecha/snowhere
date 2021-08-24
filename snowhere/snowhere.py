import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv


class StationData(object):
    """
    A class to import data from environment Canada
    """
    # Read the station data
    STATIONS_QC = pd.read_csv('meta-data/stations_QC.csv')

    def __init__(self, ID):
        self.ID = ID
        self.data = {}
        self.get_station_info(self.ID)

    def get_station_info(self):
        self.info = self.STATIONS_QC[self.STATIONS_QC['Identification Station'] == self.ID]

    def get_winter_data(self, year):
        """
        adds the year winter data to the current station class
        """
        years = [str(year - 1)] + [str(year)]
        months = ['01']

        part1_1 = 'https://climat.meteo.gc.ca/climate_data/bulk_data_f.html?format=csv&stationID='
        part1_2 = '&Year='
        part1 = part1_1 + str(self.ID) + part1_2
        part2 = '&Month='
        part3 = '&Day=1&time=&timeframe=2&submit=T%C3%A9l%C3%A9charger+des+donn%C3%A9es'

        urls = []
        for year, month in zip(years, months):
            urls.append(part1 + year + part2 + month + part3)

        dataframes = []
        for url, year in zip(urls, years):
            with requests.Session() as s:
                download = s.get(url)

                decoded_content = download.content.decode('utf-8')

                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                my_list = list(cr)

            dataframe = pd.DataFrame(my_list[1:], columns=my_list[0])
            dataframes.append(dataframe)

        self.data[str(year)] = pd.concat(dataframes, ignore_index=True)


