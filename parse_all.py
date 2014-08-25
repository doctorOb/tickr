import csv


"""
format is:
	symbol, name, lastSale, MarketCap, ADR TSO, IPOyear
	,sector, industry, summary

We're concerned with symbol (0), sector (6), and industry (7)
"""

fp_base = "data/company_lists/"

nasdaqf = open(fp_base + 'NASDAQ.csv', 'r')
reader = csv.reader(nasdaqf, delimiter=',')
data={}
reader.next() #skip the first line (row info)
for l in reader:
	data[l[0]] = {
		'sector' : l[6],
		'industry' : l[7]
	}


f = open('test.csv', 'w')
for d in data:
	key = d
	d = data[d]
	f.write("{},{},{}".format(key, d['sector'], d['industry']))