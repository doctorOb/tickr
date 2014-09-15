import ystockquote as ys
import pandas as pd
import datetime as dt

import sys
import csv


class Utils(object):

	_instance = None

	#Ensure singleton behavior
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Utils, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		try:
			open("data/company_lists/NYSE.csv")
			self.dpath = "data/company_lists"
		except:
			self.dpath = "tickr/data/company_lists"

	def as_float(self, dataframe):
		"""convert a raw string dataframe to a float. Assumes the first column is to be ignored"""
		cols = dataframe.columns.get_values()
		return dataframe[cols[1:]].astype(float)

	def today(self, as_date=False):
		"""return the current day as a string, unless as_date is specified, in which 
		case it will be returned as a datetime date object"""
		return dt.date.today() if as_date else str(dt.date.today())

	def yesterday(self, as_date=False):
		yd = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
		return yd if as_date else str(yd)

	def parse_sector_csv(self, exchange_csv):
		"""
		format is:
			symbol, name, lastSale, MarketCap, ADR TSO, IPOyear
			,sector, industry, summary

		We're concerned with symbol (0), sector (6), and industry (7)
		"""
		sector = exchange_csv.split('/')[-1].strip('.csv')
		with open(exchange_csv, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			data={}
			reader.next() #skip the first line (row info)
			for l in reader:
				data[l[0]] = {
					'Symbol': l[0],
					'Name': l[1],
					'Market': sector,
					'MarketCap': l[3],
					'IPOyear': l[5],
					'Sector' : l[6],
					'Industry' : l[7]
				}
			return data

	def get_historical_summary(self, symbol, start="2000-01-01", end=None):
		"""get the past 5 years ticker data for symbol, and return it as a DataFrame
		indexed by date, with values as float"""

		raw = ys.get_historical_prices(symbol, start, end or self.today())
		return self.as_float(pd.DataFrame(raw.values(), index=pd.to_datetime(raw.keys())))

	def get_company_list(self):
		"""get the list of all "operating companies" from our CSV file. 
		Here, an 'Operating company' is any company that we successfully pulled
		historical ticker data for. Indexes and ETFs are examples of ticker symbols
		which would not be included in this list"""
		with open('{}/all_valids.csv'.format(self.dpath), 'r') as f:
			return [sym for sym in csv.reader(f, delimiter=',')][0]

	def get_yahoo_summary(self, symbol):
		raw = ys.get_all(symbol)
		

	def calculate_change(self, dframe):
		dframe['Raw_Change'] = dframe['Close'] - dframe['Open']
		dframe['Percent_Change'] = (dframe['Close'] - dframe['Open']) / dframe['Open']
		return dframe




