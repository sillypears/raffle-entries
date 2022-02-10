from sqlalchemy import ForeignKey, Integer, String, Boolean, Date, Sequence
from sqlalchemy.sql import expression
from . import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, Sequence('user_id_seq'), unique=True, primary_key=True, nullable=False) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), unique=True, nullable=False)

class Maker(db.Model):
    __tablename__ = "maker"

    id = db.Column(db.Integer, Sequence('maker_id_seq'), unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    display = db.Column(db.String(100), nullable=False)
    instagram = db.Column(db.String(100))
    
class Entry(db.Model):
    __tablename__ = "entry"

    id = db.Column(db.Integer, Sequence('entry_id_seq'), unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'), nullable=False)
    epoch = db.Column(db.Integer, nullable=False)
    raffle_link = db.Column(db.String(500), nullable=False)
    notes = db.Column(db.String(500))
    result = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    date = db.Column(db.Date, nullable=False)
    