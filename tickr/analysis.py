import pandas as pd
import numpy as np
import sys


class AbstractAlgorithm():

	def __init__(self, ticker=None, frame=None, ticker_set=(), days=0):
		self.result = dict()
		self.ticker = ticker
		self.frame = frame
		self.ticker_set = ticker_set
		self.days = days

		

	#custom handlers for each input type. The subclass MUST implement each of these
	def _process_ticker(self):
		pass
	def _process_frame(self):
		pass
	def _process_set(self):
		pass

	#figures out which input handler to call. Doesn't need to be overriden by subclass
	def process(self):
		if self.ticker:
			self._process_ticker()
		elif self.frame:
			self._process_frame()
		elif len(self.ticker_set) > 0:
			self._process_set()



class GRatio(AbstractAlgorithm):

	def __init__(self, ticker=None, frame=None, ticker_set=(), days=0):
		AbstractAlgorithm.__init__(self, ticker, frame, ticker_set, days)
		

	def _process_ticker(self):
		pass

	def _process_frame(self):
		self.frame['Change'] = self.frame.Open - self.frame.Close
		red_days = self.frame[self.frame.Change < 0]
		green_days = self.frame[self.frame.Change >= 0]

	def _process_set(self):
		pass

	def process(self):
		#pre process

		super.process(self)

		#post process


def _GRatio(frame):
	gr = GRatio(frame=)
	sys.modules['pandas'].DataFrame.GRatio = GRatio()

