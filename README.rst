# flask-email-validation
Email validation template, based on Flask and SQLAlchemy

  TODO: requirements.txt


Usage
========

1. create and save your gmail inside ``email.txt``
2. create and save your password inside ``key.txt``
3. Go to your gmail, agree to "Access for low secure apps"
4. ``pip install -r requirements.txt``
5. execute command : ``python3 main.py``


Details
=========
``main.py`` is the main part, entry point of this code

``config.py`` for configuraiotn

``db.py`` for SQLAlchemy ORM, DB schema

``utils.py`` for utility functions 


Note that it is not save to store your password on the server, for further information, check `this <https://security.stackexchange.com/questions/61627/how-to-store-passwords-securely-in-my-server>`_

In this repo, I don't use `Flask extensions <http://flask.pocoo.org/extensions/>`_ for simplifying my code (and my life OTZ)



Reference
===========

`How to send an email with Gmail as provider using Python? <https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python/10147497#10147497>`_

`Handling Email Confirmation During Registration in Flask <https://realpython.com/handling-email-confirmation-in-flask/>`_





