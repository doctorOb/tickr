import numpy as np
import ystockquote as ys
import pandas as pd

import sqlite3 as sl3
import sys
from parse_all import parse_sector_csv


def get5yr_summary(symbol):
    start = "2009-01-01"
    end = "2014-08-20"
    raw = ys.get_historical_prices(symbol, start, end)
    return pd.DataFrame(raw.values(), index=raw.keys())


def serialize_5yr_summary(symbol):
	"""create a table (named after the ticker) and fill it with
	   5 years worth of daily trade summaries of that stock. Assumes
	   that you have a 'tickers.db' file already"""

	with sl3.connect('db/tickers.db') as con:
		df = get5yr_summary(symbol)
		df.to_sql(name=symbol, con=con, if_exists='replace')


if __name__ == '__main__':
	
	for ticker in parse_sector_csv('NASDAQ').keys():
		try:
			serialize_5yr_summary(ticker)
			print "succeeded (hopefully) in creating 5yr summary table for {}".format(ticker)
		except:
			print "failed to serialize_5yr_summary for {}".format(ticker)
