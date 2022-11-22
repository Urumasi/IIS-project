from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.model):
    xlogin = db.Column(db.String(length=30), nullable=False, unique=True, primary_key=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=30))


class Course(db.model):
    abbreviation = db.Column(db.String(length=30), nullable=False, unique=True, primary_key=True)
    description = db.Column(db.String())
    type = db.Column(db.String())
    price = db.Column(db.Integer())


class Course_news(db.model):
    abbreviation = db.Column(db.String(length=30), nullable=False, unique=True, primary_key=True)
    da_newz = db.Column(db.String())
