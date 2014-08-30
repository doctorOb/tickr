"""An interface to the sqlite3 database(s) used in the project"""
import numpy as np
import ystockquote as ys
import pandas as pd
import pandas.io.sql as pdsql

import MySQLdb as mysql
import sys


#from the command line 'mysql -h 192.168.1.14 -u remote --password=whitey11'
class Tickr_DBA():

	def __init__(self):
		self.con = None

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

	def write(self, table, dframe, if_exists='append'):
		"""Write a dataframe to the specified table. It's up to the caller
		to be smart about this and not write misformed frames"""
		dframe.to_sql(name=table, con=self.con, if_exists=if_exists, flavor='mysql')

	def fetch(self, table):
		"""read a table into a pandas dataframe. It will probably be a string, so
		remember to convert relavent values to float or something"""
		return pdsql.read_sql("SELECT * FROM {}".format(table), self.con)


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

	