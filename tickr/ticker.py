import ystockquote as y
import ticker as ticker
import datetime
import dateutil
import dba



class Ticker:
	"""For information of function output, run as main"""
	def __init__(self,symbol):
		self.symbol=symbol.upper()
		self.today=datetime.date.today().toordinal()
		if dba.DBA()==True:
			d=dba.DBA()
			d.connect()
			self.frame=d.fetch(self.symbol).sort(columns="index")
			print("connected")
			self.frame.iloc[-1]
		else:
			print("Can't connect.")
	def Manual_connect():
		print("Choose algorithm to run.")
		#implement way to decide algorithm. Default implementation is simple moving average
		#alg=raw_input()
		print("Choose length of history in days")
		days=int(raw_input())
		initial_date=datetime.date.fromordinal(735549-days).isoformat()
		final_date=datetime.date.fromordinal(735549).isoformat()
		symbol="AAPL"
		if True==True:
			prices=y.get_historical_prices(symbol,initial_date,final_date)
			sum=0
			tradingdays=0
			print(prices.keys())
			for key in prices.iterkeys():
				sum+=float(prices[key]["Adj Close"])
				tradingdays+=1
				#for debugging
				print(prices[key]["Adj Close"])
			print(sum,days)	
			sum=sum/(tradingdays)		
			print ("%s to %s is %s trading days with a moving day average is %s:" % (initial_date,final_date,tradingdays,sum))
		else:
			print("it's not true")
	Manual_connect()
	#self.frame.iloc[-2] and equivalent
	#self.frame[-2:-1]


	def simple_moving_average(days=50):
		print "%s day moving average is:" % (str(days))
		sma=[value for value in self.frame[-days:]["Close"]]
		ave=0
		for value in sma:
			ave+=value
		print ave
	def weighted_moving_average(days=50):
		print "%s day weighted moving average is:" % (str(days))

	def exponentional_moving_average(days=50):
		print "%s day exponential moving average is:" % (str(days))


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
