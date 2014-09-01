import pandas as pd
import numpy as np


class AbstractAlgorithm():

	def __init__(self):
		self.result = dict()
		pass

	def process(self, ticker):
		pass



class GRatio(AbstractAlgorithm):

	def __init__(self, ticker):
		AbstractAlgorithm.__init__(self)
		self.ticker = ticker

	def process(self):
		df = ticker.drange(-30)


