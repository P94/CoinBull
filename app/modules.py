import gdax
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

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

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))