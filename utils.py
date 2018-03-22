'''
	function tools for email validation
'''
import smtplib
from validate_email import validate_email
from itsdangerous import URLSafeTimedSerializer
from flask import Flask, url_for, render_template
from config import BaseConfig


SECRET_KEY = BaseConfig.SECRET_KEY
SALT = BaseConfig.SECURITY_PASSWORD_SALT
MAIL_SERVER = BaseConfig.MAIL_SERVER


def generate_confirmation_token(email, username):
	serializer = URLSafeTimedSerializer( SECRET_KEY )
	print('serializer', serializer)
	return serializer.dumps({'email':email, 'username':username}, salt=SALT)


def confirm_token(token, expiration=3600):
	serializer = URLSafeTimedSerializer( SECRET_KEY )
	try:
		result = serializer.loads(token, salt=SALT, max_age=expiration)
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

	with open('email.txt', 'r') as f1:
		with open('key.txt', 'r') as f2:
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
	server = smtplib.SMTP( MAIL_SERVER )
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

