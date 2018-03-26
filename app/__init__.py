from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
from flask_login import LoginManager
from config import *
from flask_login import current_user, login_user, logout_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from modules import Currency, User

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html')