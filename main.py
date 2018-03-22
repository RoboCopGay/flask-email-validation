#! /usr/bin/env python

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from config import BaseConfig
from utils import *
from db import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = BaseConfig.DB_PATH
app.config['SECRET_KEY'] = BaseConfig.SECRET_KEY
db = SQLAlchemy(app)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/mainpage')
def mainpage():
	return render_template('mainpage.html')


@app.route('/logout', methods=['GET','POST'])
def logout():
	del session['username']
	del session['email']

	return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	username = request.form['username']
	passwd = request.form['password']

	user = User.query.filter_by(username=username).first()
	if user is None:
		return 'User does not exist!'
	
	true_user = check_password_hash(user.password, passwd)
	if not true_user:
		return 'wrong password'
	
	session['username'] = user.username
	session['email'] = user.email

	if user.activate is False:
		return render_template('unconfirmed.html')

	return redirect(url_for('mainpage'))


@app.route('/register', methods=['GET', 'POST'])
def register():

	if request.method == 'POST':

		username = request.form['username']
		print('username', username)
		user = User.query.filter_by(username=username).first()
		if user is not None:
			return 'User exists!'

		email = request.form['email']
		if check_email_validation(email):
			password = generate_password_hash(request.form['password'])
			new_user = User(username=username, 
							password=password,
							email=email,
							activate=False)

			db.session.add(new_user)
			db.session.commit()

			send_confirmation_mail(email, username)
		else:
			return 'email is not valid.'

	return redirect(url_for('index'))


@app.route('/confirm/<token>')
def confirm_email(token):
	try:
		data = confirm_token(token)
	except:
		return 'token expired'

	user = User.query.filter_by(username=data['username']).first()
	if user:
		user.activate=True
		db.session.add(user)
		db.session.commit()

	return 'ok'


@app.route('/resend')
def resend_confirmation():

	send_confirmation_mail(session['email'], session['username'])
	return 'ok'


@app.after_request
def add_header(r):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	# clear browser cache
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r


if __name__ == '__main__':
	app.debug = True
	db.create_all()
	app.run(host='127.0.0.1')





