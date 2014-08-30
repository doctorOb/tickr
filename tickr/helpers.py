import numpy as np
import ystockquote as ys
import pandas as pd

import sys
import csv


"""
format is:
	symbol, name, lastSale, MarketCap, ADR TSO, IPOyear
	,sector, industry, summary

We're concerned with symbol (0), sector (6), and industry (7)
"""
fp_base = "data/company_lists/"

def parse_sector_csv(sector):
	with open(fp_base + '{}.csv'.format(sector), 'r') as f:
		reader = csv.reader(f, delimiter=',')
		reader.next()
		data={}
		reader.next() #skip the first line (row info)
		for l in reader:
			data[l[0]] = {
				'Name': l[1],
				'Sector' : l[6],
				'Industry' : l[7]
			}
		return data

def get5yr_summary(symbol):
    start = "2009-01-01"
    end = "2014-08-20"
    raw = ys.get_historical_prices(symbol, start, end)
    df = pd.DataFrame(raw.values(), index=raw.keys())
    df.index = pd.to_datetime(df.index) #convert the index to date types
    cols = df.columns.get_values()
    return df[cols[1:]].astype(float) #convert the reset to floats







if __name__ == '__main__':
	fails = []
	for ticker in parse_sector_csv('NASDAQ').keys():
		try:
			serialize_5yr_summary(ticker)
			print "succeeded in creating 5yr summary table for {}".format(ticker)
		except:
			print "failed to serialize_5yr_summary for {}".format(ticker)
			fails.append(ticker)
