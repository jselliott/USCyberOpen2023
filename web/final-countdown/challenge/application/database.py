from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()

class Hacker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    specialization = db.Column(db.String(50))
    location = db.Column(db.String(50))
    price = db.Column(db.Float)

class Flag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(50))