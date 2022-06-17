import re
from datetime import datetime, timedelta
from pprint import pprint
from urllib.parse import urlparse

from flask import (Blueprint, Flask, jsonify, make_response, redirect,
                   render_template, request, send_file, url_for,)
from flask_api import status
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

from project import create_app
import jwt
from . import database, db
from .models import User


api = Blueprint('api', __name__, url_prefix="/api")

conf = create_app().config['CONFIG']

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if auth_headers[0] != "RAF":
            return jsonify(invalid_msg), 401
        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, create_app().config['SECRET_KEY'], algorithms="HS256")
            user = User.query.filter_by(name=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

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
        usernm = request.get_json()['name']
        password = request.get_json()['password']
        user = User.query.filter_by(name=usernm).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'FAIL', 'text': 'Username and password do notmatch'}, 401
        token = jwt.encode({
            'sub': user.name,
            'iat':datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)},
            create_app().config['SECRET_KEY'])
        return jsonify({ 'token': token })

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
@token_required
def get_entries(current_user):
    entries = None
    try:
        print(current_user)
    except:
        print('Could not get entries')
        return {'message': 'FAIL'}


    return {'message': 'OK', 'data': entries}
