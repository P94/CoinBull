from flask import Flask, render_template
import gdax
app = Flask(__name__)

cryptos = {
	'Bitcoin': {
		'ticker': 'BTC',
		'picture_url': 'bitcoin.png'
		},
	'LiteCoin': {
		'ticker': 'LTC',
		'picture_url': 'litecoin.png'
		},
	'Ether': {
		'ticker': 'ETH',
		'picture_url': 'ether.png'
		},
	}

public_client = gdax.PublicClient()

class Currency(object):
	def __init__(self, name, ticker, picture_url):
		self.name = name
		self.ticker = ticker
		self.usd_product = "{}-USD".format(self.ticker)
		self.picture_url = picture_url

	def get_price(self):
		price_info = public_client.get_product_ticker(product_id=self.usd_product)
		price_only = price_info.get('price')
		price_two_decimal = price_only[:-6]
		self.price = price_two_decimal
		return self.price

@app.route('/')
def index():
	crypto_objects = []
	for name, attributes in cryptos.items():
		ticker = attributes.get('ticker')
		picture_url = attributes.get('picture_url')
		crypto_object = Currency(name, ticker, picture_url)
		crypto_object.get_price()
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
