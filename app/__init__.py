from flask import Flask, render_template

from flask.ext.sqlalchemy import SQLAlchemy

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