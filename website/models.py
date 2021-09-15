from datetime import timezone
from enum import unique

from sqlalchemy.sql.expression import true
from . import db    # it will import it from init.py
from flask_login import UserMixin
from sqlalchemy.sql import func # to store the datezone information automatically


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000000000000000000000000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # will create a relationship between Note and user class with the primary key name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20000000000000000), unique=True)
    name = db.Column(db.String(2000000000000000))
    password= db.Column(db.String(20000000000000))
    notes = db.relationship('Note')
