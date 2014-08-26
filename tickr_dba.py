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
		if self.con is None:
			try:
				self.con = sl3.connect(self.dbname)
			except:
				print "Failed to connect to db '{}'".format(self.dbname)

		return self.con

	def fetch(self, symbol):
		return pdsql.read_sql("SELECT * FROM {}".format(symbol), self.con)


if __name__ == '__main__':
	tdb = Tickr_DBA()
	tdb.connect()

	print tdb.fetch('ANY')