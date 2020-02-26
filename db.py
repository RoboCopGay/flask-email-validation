from flask_sqlalchemy import SQLAlchemy
from main import db

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
