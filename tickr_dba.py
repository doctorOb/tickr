"""An interface to the sqlite3 database(s) used in the project"""
import numpy as np
import ystockquote as ys
import pandas as pd
import pandas.io.sql as pdsql

import sqlite3 as sl3
import sys


class Tickr_DBA():

	def __init__(self, dbname="db/tickers.db"):
		self.con = None
		self.dbname = dbname

	def connect(self):
		"""initiate a connection with the DB. This must be called manually"""
		if self.con is None:
			try:
				self.con = sl3.connect(self.dbname)
			except:
				print "Failed to connect to db '{}'".format(self.dbname)


	def fetch(self, symbol):
		"""read a table into a pandas dataframe. It will probably be a string, so
		remember to convert relavent values to float or something"""
		return pdsql.read_sql("SELECT * FROM {}".format(symbol), self.con)


## result = df.sort(['A', 'B'], ascending=[1, 0])


class Utils():

	def __init__(self):
		pass

	def as_float(self, dataframe):
		"""convert a raw string dataframe to a float. Assumes the first column is to be ignored"""
		cols = dataframe.columns.get_values()
		return dataframe[cols[1:]].astype(float)

if __name__ == '__main__':
	tdb = Tickr_DBA()
	tdb.connect()

	