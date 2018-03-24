import gdax
from flask_login import UserMixin
#from app import login

public_client = gdax.PublicClient()

class Currency(object):
	"""
	This class holds all crypto currency information
	"""
	def __init__(self, name, ticker, picture_url):
		self.name = name
		self.ticker = ticker
		self.usd_product = "{}-USD".format(self.ticker)
		self.picture_url = picture_url

	## Function to pull current price of a specified crypto currency ##
	def get_price(self):
		price_info = public_client.get_product_ticker(product_id=self.usd_product)
		price_only = price_info.get('price')
		price_two_decimal = price_only[:-6]
		self.price = price_two_decimal

	## Function to pull 24 hour statistics for a crypto currency ##
	def get_42hr_stats(self):
		stats_24_hour = public_client.get_product_24hr_stats(self.usd_product)
		self.volume_24hr = stats_24_hour.get("volume")[:-6]
		self.high_24hr = stats_24_hour.get("high")[:-6]
		self.low_24hr = stats_24_hour.get("low")[:-6]

	## Function to get the URL to GDAX for the current crypto currency object ##
	def get_url(self):
		url = "https://www.gdax.com/trade/{0}".format(self.usd_product)
		self.url = url

class User(UserMixin):
	pass