import ystockquote as stock
import ticker as ticker

class Ticker:
	def __init__(self,symbol):
		self.symbol=symbol
		self.info={}
		a=ticker.stock.get_all(str(symbol))
		for key in a:
			new_key=key.replace("_"," ")
			self.info[new_key]=a[key]
			
	def print_info(self):
		a=[key for key in self.info]
		a.sort()
		for key in a:
			print key.ljust(30),self.info[key]


if __name__=="__main__":
	AAPL=Ticker("AAPL")
	AAPL.print_info()
