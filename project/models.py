from sqlalchemy import ForeignKey, Integer, String, Boolean, Date, Sequence
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, Sequence('users_id_seq'), unique=True, primary_key=True, nullable=False) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), unique=True, nullable=False)
    makers = db.relationship("Maker", backref="user")
    entries = db.relationship("Entry", backref="user")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.password = generate_password_hash(kwargs.get('password'), method='sha256')
    
    @classmethod
    def authenticate(cls, **kwargs):
        name = kwargs.get('name')
        password = kwargs.get('password')
        
        if not name or not password:
            return None

        user = cls.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    @classmethod
    def validate(cls, **kwargs):
        name = kwargs.get('name')
        
        if not name:
            return None

        user = cls.query.filter_by(name=name).first()

        if not user:
            return None

        return user
    def to_dict(self):
        return dict(id=self.id, name=self.name)

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
    maker_name = db.relationship("Maker", primaryjoin=("and_(Entry.maker_id==Maker.id)"), backref="makers")

    def to_dict(self):
        return dict(id=self.id, user_id=self.user_id, maker_id=self.maker_id, maker_name=self.maker_name.name, epoch=self.epoch, raffle_link=self.raffle_link, notes=self.notes, result=self.result, date=self.date)