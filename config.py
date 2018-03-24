# Enabling development environmentr
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'CoinBull.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

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