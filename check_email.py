#! /usr/bin/env python

import smtplib
from validate_email import validate_email
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from config import BaseConfig


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = BaseConfig.SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = BaseConfig.SECURITY_PASSWORD_SALT
db = SQLAlchemy(app)


class User(db.Model):
	""" Create user table"""

	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
	#email = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, nullable=False)
	activate = db.Column(db.Boolean, nullable=False, default=False)
	
	def __init__(self, username, password, email, activate):
		self.username = username
		self.password = password
		self.email = email
		self.activate = activate


def initial_db():
	''' 
		create default user
	'''
	# create default user : (username=a, passwd=a)
	data = User.query.filter_by(username='a').first()
	if data is None:
		usr_passwd = generate_password_hash('a')
		default_user = User(username='a', password=usr_passwd)
		db.session.add(default_user)
		db.session.commit()


def generate_confirmation_token(email, username):
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	print('serializer', serializer)
	
	return serializer.dumps({'email':email, 'username':username}, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	try:
		result = serializer.loads(token, 
								 salt=app.config['SECURITY_PASSWORD_SALT'],
								 max_age=expiration)
	except:
		return False
	
	return result


def check_email_validation(email):

	print('email', email)

	# valid = validate_email(email, verify=True)
	# verify option is for checking if that email exists
	# default is False
	# default just examine wether the input email format is correct

	valid = validate_email(email)
	print('valid', valid)
	return valid


def send_mail(email, template):

	f1 = open("email.txt","r")
	f2 = open("key.txt","r")

	username = f1.readline()
	password = f2.readline()

	_from = f1.readline()
	_to  = email

	msg = "\r\n".join([
	  "From: " + _from,
	  "To: " + email,
	  "Subject: confirm email",
	  "",
	  "send for activate account",
	  template
	  ])
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(_from, _to, msg)
	server.quit()
	return


def send_confirmation_mail(email, username):

	token = generate_confirmation_token(email, username)
	confirm_url = url_for('confirm_email', token=token, _external=True)
	html = render_template('activate.html', confirm_url=confirm_url)
	send_mail(email, html)
	return 


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
	#initial_db()
	app.run(host='127.0.0.1')





