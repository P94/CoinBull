from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from modules import Currency, User
from forms import LoginForm
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager(app)
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/sorry')
def page_not_here_yet():
	return 'Sorry I have not made this page yet!'

@app.route('/about')
def about():
    return render_template('about.html')