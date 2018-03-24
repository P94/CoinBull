from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from modules import Currency, User
from forms import LoginForm
from flask_login import LoginManager
from config import *
from flask_migrate import Migrate

app = Flask(__name__)
login = LoginManager(app)
app.config.from_object('config')
db = SQLAlchemy(app)

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
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html')