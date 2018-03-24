from flask import Flask, render_template

from flask.ext.sqlalchemy import SQLAlchemy

#import gdax

from modules import Currency

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

## Configuration for what crypto currencies to track ##
cryptos = {
	'Bitcoin': {
		'ticker': 'BTC',
		'picture_url': 'bitcoin.png'
		},
	'Litecoin': {
		'ticker': 'LTC',
		'picture_url': 'litecoin.png'
		},
	'Ethereum': {
		'ticker': 'ETH',
		'picture_url': 'ether.png'
		},
	'Bitcoin Cash': {
		'ticker': 'BCH',
		'picture_url': 'bitcoin_cash.png'
		},
	}

## public client to handle connections to GDAX ##
#public_client = gdax.PublicClient()

'''
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
'''

## Home page that displays basic price information ##
@app.route('/')
def index():
	crypto_objects = []
	for name, attributes in cryptos.items():
		ticker = attributes.get('ticker')
		picture_url = attributes.get('picture_url')
		crypto_object = Currency(name, ticker, picture_url)
		crypto_object.get_price()
		crypto_object.get_42hr_stats()
		crypto_object.get_url()
		crypto_objects.append(crypto_object)
	return render_template('index.html', crypto_objects=crypto_objects)

@app.route('/sorry')
def page_not_here_yet():
	return 'Sorry I have not made this page yet!'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<username>')
def get_username(username):
	return "User: {}".format(username)

if __name__ == "__main__":
	app.run(debug=True)