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


if __name__ == '__main__':

	f = open('test.csv', 'w')
	for d in data:
		key = d
		d = data[d]
		f.write("{},{},{}".format(key, d['sector'], d['industry']))


