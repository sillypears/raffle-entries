from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for, send_file, make_response
from flask_api import status
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import math
from pprint import pprint
from datetime import datetime
import os
from urllib.parse import urlparse
import json
import csv
import re
from project import create_app
from . import database
from . import db
from .models import User

api = Blueprint('api', __name__, url_prefix="/api")

conf = create_app().config['CONFIG']

@api.route('/', methods=['GET'])
def main():
    return {'message': 'OK', 'version': f"{create_app().config['majorVersion']}.{create_app().config['minorVersion']}"}

@api.route('/check_user', methods=['GET'])
@login_required
def check_user():
    return {
        'message': 'OK',
        'user_id': current_user.id,
        'user_name': current_user.name
    }

@api.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "GET":
        return redirect(url_for('api.main'))
    elif request.method == "POST":
        usernm = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(name=usernm).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'FAIL', 'text': 'Username and password do notmatch'}, 401
        return {'message': 'OK', 'text': f"User ({usernm}) logged in successfully"}

    else:
        return redirect(url_for('auth.login'))

@api.route('/register', methods=['POST'])
def register():
    usernm = request.form.get('username')
    passwd = generate_password_hash(request.form.get('password'), method='sha256')
    if re.fullmatch('[a-zA-Z0-9_-]+', usernm):
        user = User.query.filter_by(name=usernm).first()
        if user:
            return {'message': 'FAIL', 'error': "Username already exists"}, 409
        n_user = User(name=usernm, password=passwd)
        db.session.add(n_user)
        db.session.commit()
        return {'message': 'OK', 'text': f"User {usernm} signed up"}, 201
    else:
        return {'message': 'FAIL', 'error': "Username contains non-supported characters"}, 400

@api.route('/entries', methods=['GET'])
def get_entries():
    entries = None
    try:
        cur = database.get_db(conf)
        e = database.get_entries(cur, current_user.id, conf)
        entries = e.fetchall()
        cur.close()
    except:
        print('Could not get entries')

    return {'message': 'OK', 'data': entries}
