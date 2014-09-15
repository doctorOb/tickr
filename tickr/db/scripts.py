import ystockquote as ys
from helpers import Utils
import sys
from accessor import Accessor


"""
Scripts to automate batch database interactions (long running ones), should be defined here.

A callback function, which operates on a stock DataFrame, can be provided, and will be 
called on each frame before it is saved to the DB.
"""

def init_db(callback):
	"""Instantiate the database, replacing existing tables. We should only need to call this once

	A table, called 'company_index', of all ticker symbols (from the CSVs) will be created.
	For each symbol, a table (named after the symbol) of historical data will also be made
	"""

	confirm = raw_input("this will erase most tables in the database, do you wish to proceede? [y/n]: ")

	if confirm != 'y':
		return

	ut = Utils()
	dba = Accessor()
	all_companies = ut.get_company_list()

	dba.connect()

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

			prices['Raw_Change'] = prices['Close'] - prices['Open']
			prices['Percent_Change'] = (prices['Close'] - prices['Open']) / prices['Open']
			dba.write(symbol, prices, if_exists='replace')
			print "wrote {}".format(symbol)
		except:
			print "failed on {}".format(symbol)
			failures.append(symbol)

	all_companies = filter(lambda x: x not in failures, all_companies)
	#prepare the dataframe for SQL. This involves reindexing the frame to use
	#the ticker symbol as it's index. We have to remove the symbol field afterwards,
	#otherwise it will try to create a table with two Symbol fields, and MySQL will
	#throw an error.
	df = pd.DataFrame(all_companies)
	df.index = df['Symbol'] #make the symbols the index
	df = df.drop('Symbol', 1) #remove the symbol field as its already stored as the index
	dba.write('company_index', df[:-1], if_exists='replace')

	dba.close()
	
	with open('failures.csv', 'w') as f:
		f.write('Symbol,')
		for sym in failures:
			f.write(",{}".format(sym))

def update_db(callback=None, start=None):
	"""db script to iterate over all operating companies in our database, and update them with 
	the day's historical data."""
	ut = Utils()
	dba = Accessor()
	all_companies = ut.get_company_list()
	start = start if start else ut.yesterday()

	dba.connect()

	for symbol in all_companies:
		try:
			new_row = ut.get_historical_summary(symbol, start=start, end=ut.today())
			if callback:
				new_row = callback(new_row)
			dba.write(symbol, new_row)
			print "updated {}".format(symbol)
		except:
			print "failed on {}".format(symbol)


	dba.close()


if __name__ == '__main__':
	
	ut = Utils()

	update_db(callback=ut.calculate_change, start="2014-09-05")

