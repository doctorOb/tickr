"""An interface to the sqlite3 database(s) used in the project"""
import numpy as np
import ystockquote as ys
from helpers import Utils
import pandas as pd
import pandas.io.sql as pdsql

import MySQLdb as mysql
import sys


#from the command line 'mysql -h 192.168.1.14 -u remote --password=whitey11'
class DBA(object):

	_instance = None

	#Ensure singleton behavior
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(DBA, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.con = None
		self._cache = dict()

	def connect(self):
		"""initiate a connection with the DB. This must be called manually"""
		if self.con is None:
			try:
				self.con = mysql.connect(host="192.168.1.14",
										 user="remote",
										 passwd="whitey11",
										 db="tickr")
			except:
				print "Failed to connect to db '{}'".format(self.dbname)
	def close(self):
		"""close the db conneciton, perform any other cleanup"""
		self.con.close()

	def write(self, table, dframe, if_exists='append'):
		"""Write a dataframe to the specified table. It's up to the caller
		to be smart about this and not write misformed frames"""
		dframe.to_sql(name=table, con=self.con, if_exists=if_exists, flavor='mysql')

	def fetch(self, table, cache=False):
		"""read a table into a pandas dataframe."""
		if table in self._cache.keys() and not fresh:
			return self._cache[table]
		else:
			try:
				return pdsql.read_sql("SELECT * FROM {}".format(table), self.con)
			except:
				return None


## result = df.sort(['A', 'B'], ascending=[1, 0])


def init_db():
	"""Instantiate the database, replacing existing tables. We should only need to call this once

	A table, called 'company_index', of all ticker symbols (from the CSVs) will be created.
	For each symbol, a table (named after the symbol) of historical data will also be made
	"""

	confirm = raw_input("this will erase most tables in the database, do you wish to proceede? [y/n]: ")

	if confirm != 'y':
		return

	ut = Utils()
	dba = DBA()

	NYSE = ut.parse_sector_csv('data/company_lists/NYSE.csv')
	NASDAQ = ut.parse_sector_csv('data/company_lists/NASDAQ.csv')
	AMEX = ut.parse_sector_csv('data/company_lists/AMEX.csv')
	all_companies = NYSE.values() + NASDAQ.values() + AMEX.values()

	#prepare the dataframe for SQL. This involves reindexing the frame to use
	#the ticker symbol as it's index. We have to remove the symbol field afterwards,
	#otherwise it will try to create a table with two Symbol fields, and MySQL will
	#throw an error.
	df = pd.DataFrame(all_companies)
	df.index = df['Symbol'] #make the symbols the index
	df = df.drop('Symbol', 1) #remove the symbol field as its already stored as the index

	
	dba.connect()
	dba.write('company_index', df[:-1], if_exists='replace')

	#pull historical information (since 2009, or the ipo year) for all stocks, and 
	#write them to a table (named after their ticker symbol)
	failures = []
	for company in all_companies:
		symbol = company['Symbol']
		ipo = company['IPOyear']

		try:
			if 'n/a' not in ipo:
				prices = ut.get_historical_summary(symbol, start="{}-01-01".format(ipo))
			else:
				prices = ut.get_historical_summary(symbol)

			dba.write(symbol, prices, if_exists='replace')
			print "wrote {}".format(symbol)
		except:
			print "failed on {}".format(symbol)
			failures.append(symbol)

	dba.close()
	
	with open('failures.csv', 'w') as f:
		f.write('Symbol,')
		for sym in failures:
			f.write(",{}".format(sym))




	