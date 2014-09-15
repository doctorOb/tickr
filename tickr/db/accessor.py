"""An interface to the sqlite3 database(s) used in the project"""
import numpy as np
import pandas as pd
import pandas.io.sql as pdsql
import MySQLdb as mysql


#from the command line 'mysql -h 192.168.1.14 -u remote --password=whitey11'
class Accessor(object):

	_instance = None

	#Ensure singleton behavior
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Accessor, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.con = None
		self._cache = dict()

	"""
	handlers for with statement use. Basically a cleaner way to open/close the db connection
	"""
	def __enter__(self):
		self.connect()
		return self

	def __exit__(self):
		self.close()

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
		try:
			return pdsql.read_sql("SELECT * FROM {}".format(table), self.con)
		except:
			return "fail"

	def query(self, qstring):
		"""allow raw query strings to be sent to the DB manually"""
		pass









	