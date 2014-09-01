import ystockquote as stock
import ticker as ticker
import datetime

class Ticker:
	"""For information of function output, run as main"""
	def __init__(self,symbol):
		self.symbol=symbol
		self.info={}
		a=ticker.stock.get_all(str(symbol))
		for key in a:
			new_key=key.replace("_"," ")
			self.info[new_key]=a[key]
		self.history(years_ago=0,months_ago=1,days_ago=0)
	def history(self,years_ago=0,months_ago=0,days_ago=0,date="yyyy-mm-dd"):
		if date!="yyyy-mm-dd":
			start=date
		else:
			if years_ago==months_ago==days_ago==0:
				months_ago=1
			month=str(int(str(datetime.datetime.now())[5:7])-months_ago)
			if len(month)==1:
				month="0"+month
			year=str(int(str(datetime.datetime.now())[0:4])-years_ago)
			day=str(int(str(datetime.datetime.now())[8:10])-days_ago)
			start=year+"-"+month+"-"+day
			#print year, month, day, start
		end=str(datetime.datetime.now())[0:11]
		self.hist=stock.get_historical_prices(self.symbol,start,end)
	def print_info(self):
		a=[key for key in self.info]
		a.sort()
		for key in a:
			print key.ljust(30),self.info[key]

def format_historical_data(dict_of_dict):
	b=dict_of_dict
	a=b.keys()
	e=[]
	for key in range(len(a)):
		e.append(a[key])
		c=[value for value in b[a[key]]]
		header=c[:]
		header.insert(0,'date')
		#print c, "\n", header
		print a[key]
		for k in range(len(c)):
			d=c[k]
			print d,":",b[a[key]][d].rjust(5)
		print "\n"
	#sorted(e,int(e[8])) """trying to sort dates"""
	print e


if __name__=="__main__":
	AAPL=Ticker("AAPL")
	#AAPL.print_info()
	AAPL.history(date="2014-07-25")
	print ticker.format_historical_data(AAPL.hist)
