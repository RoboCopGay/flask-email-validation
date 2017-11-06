#! /usr/bin/env python

import smtplib
from itsdangerous import URLSafeTimedSerializer
from validate_email import validate_email
from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)

def check_email_validation(email):

	print('email', email)
	valid = validate_email(email)
	print('valid', valid)
	return valid


def send_mail(email):

	f1 = open("email.txt","r")
	f2 = open("key.txt","r")

	username = f1.readline()
	password = f2.readline()

	_from = f1.readline()
	_to  = email


	msg = "\r\n".join([
	  "From: " + _from,
	  "To: " + email,
	  "Subject: Just a message",
	  "",
	  "send for activate account"
	  ])
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(_from, _to, msg)
	server.quit()


@app.route('/')
def index():

	return render_template('index.html')


@app.route('/check_email', methods=['GET', 'POST'])
def check_email():

	if request.method == 'POST':
		email = request.form['email']
		#print('email', email)
		if check_email_validation(email):
			send_mail(email)
		else:
			print('email is not valid.')


	return redirect(url_for('index'))


if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1')
