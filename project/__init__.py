from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse
import os
from . import database

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

url = urlparse(os.environ.get('DATABASE_URL'))

class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG')
    DATABASE_HOST = url.hostname
    DATABASE_PORT = url.port
    DATABASE_USER = url.username
    DATABASE_PASS = url.password
    DATABASE_SCHEMA = url.path[1:]

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'JDKLj3sddkadsa'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['CONFIG'] = Config

    db.init_app(app)
    
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

    