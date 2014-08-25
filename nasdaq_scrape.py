import dompy
import mechanize
import cookielib
import ystockquote



class Crawler:

	def __init__(self):
		self.br = self._init_mechanize_browser()

	def _init_mechanize_browser(self):
		"""
		create a mechanize browser instance that will spoof most websites.
		copy/pasted from http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/
		"""
		br = mechanize.Browser()
		cj = cookielib.LWPCookieJar()
		br.set_cookiejar(cj)

		# Browser options
		br.set_handle_equiv(True)
		br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)

		# Follows refresh 0 but not hangs on refresh > 0
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		br.addheaders = [('User-agent',
			'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		return br

	def parseRow(self, tr):
		return [col.innerText for col in tr.children]

	def get(self, url):
		try:
			response = self.br.open(url)
		except:
			print "couldnt open url"
			return ""
		return response.read()

	def crawl(self, symbol):
		url = "http://www.nasdaq.com/symbol/{}/financials?".format(symbol.lower())
		url += "query=income-statement"

		response = self.get(url)
		if len(response) < 1:
			return

		document = dompy.Document(response)
		data = {}
		tbls = document.getElementById("financials-iframe-wrap").getElementsByClassName('genTable')
		balance = tbls[0].children[2].children
		headers = self.parseRow(balance[0])

		for row in balance:
			self.parseRow(row)

		print headers




class CNBC_Statement:

	def __init__(self, symbol):
		self.symbol = symbol
		self.setup()
		
	def setup(self):
		"""read the page from the file system, return as string"""
		try:
			html = open('earnings/{}.html'.format(self.symbol), 'r').read()
		except:
			raise IOError

		self.document = dompy.Document(html)

	def parseTR(self, tr):
		label = tr.children[0].innerText.upper()
		values = []
		for valForYear in tr.children[1:]:
			val = valForYear.innerText.replace(",","")
			if "(" in val: #negative
				val = float(val.strip("(").strip(")"))*-1.0
			else:
				val = float(val)
			values.append(val)
		return label, values

	def parseYearlyIncome(self):
		ret = dict()
		yrTbl = self.document.getElementById('financialReportYr')
		header = yrTbl.children[1].getElementsByTagName('tr')[0].getElementsByTagName('th')
		rowContainer = yrTbl.getElementsByTagName('tbody')[0]
		rowHeads = [] #an array to hold the row head value for each index
		for field in header[1:]:
			year = field.children[0].innerText #span holding the year
			rowHeads.append(year)

		#get the total values on the income statement
		#we'll worry about specifics (amoritizaiton ect) later
		totalTds = rowContainer.getElementsByClassName('total')

		for td in totalTds:
			key, vals = self.parseTR(td)
			ret[key] = vals

		return ret


class CNBC_Balance_Sheet():

	def __init__(self, symbol, type='yr'):
		self.raw = open('earnings/{} - {}.txt', 'r').read()

if __name__ == '__main__':
	cr = CNBC_Statement('GLW')
	print cr.parseYearlyIncome()