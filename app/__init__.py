from flask import Flask, render_template, flash, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_migrate import Migrate
from werkzeug.urls import url_parse
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app.errors import not_found_error, internal_error
from app.modules import Currency, User
from app.forms import LoginForm, RegistrationForm, SettingsForm

## Home page that displays basic price information ##
@app.route('/index')
@app.route('/')
def index():
    crypto_objects = []
    for name, attributes in cryptos.items():
        ticker = attributes.get('ticker')
        picture_url = attributes.get('picture_url')
        crypto_object = Currency(name, ticker, picture_url)
        crypto_object.get_price()
        crypto_object.get_24hr_stats()
        crypto_object.get_url()
        crypto_objects.append(crypto_object)
    return render_template('index.html', crypto_objects=crypto_objects)

@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    if current_user.username != username:
        abort(401)
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('dashboard.html', user=user)

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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
        	next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('settings.html', title='Edit Profile',
                           form=form)

@app.route('/about')
def about():
    return render_template('about.html')