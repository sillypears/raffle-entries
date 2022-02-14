from sqlalchemy import ForeignKey, Integer, String, Boolean, Date, Sequence
from sqlalchemy.sql import expression
from flask_login import UserMixin

from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, Sequence('users_id_seq'), unique=True, primary_key=True, nullable=False) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), unique=True, nullable=False)

class Maker(db.Model):
    __tablename__ = "makers"

    id = db.Column(db.Integer, Sequence('makers_id_seq'), unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    display = db.Column(db.String(100), nullable=False)
    instagram = db.Column(db.String(100))
    
class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, Sequence('entries_id_seq'), unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    maker_id = db.Column(db.Integer, db.ForeignKey('makers.id'), nullable=False)
    epoch = db.Column(db.Integer, nullable=False)
    raffle_link = db.Column(db.String(500), nullable=False)
    notes = db.Column(db.String(500))
    result = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    date = db.Column(db.Date, nullable=False)
    