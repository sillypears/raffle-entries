from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from urllib.parse import urlparse
import os
from flask_login import LoginManager

from . import database

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

url = urlparse(os.environ.get('DATABASE_URL'))

class Config(object):
    DEBUG = True if os.environ.get('FLASK_ENV') == "development" else False
    DATABASE_HOST = url.hostname
    DATABASE_PORT = url.port
    DATABASE_USER = url.username
    DATABASE_PASS = url.password
    DATABASE_SCHEMA = url.path[1:]

def create_app():
    # Dumb work around because heroku forces "postgres" and sqlalchemy only knows "postgresql"
    # So we replace the first instance of it if we find it
    db_url = os.environ.get('DATABASE_URL')
    if os.environ.get('DATABASE_URL').split(':')[0] == "postgres": 
        db_url = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql', 1)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['CONFIG'] = Config   
    app.config['majorVersion'] = 1
    app.config['minorVersion'] = 0.1
    with open('project/id_rsa', 'r') as f:
        app.config['priv_key'] = f.read()
    with open('project/id_rsa.pub', 'r') as f:
        app.config['pub_key'] = f.read()
    CORS(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    @app.before_request
    def before_request():
        if 'DYNO' in os.environ:
            if request.url.startswith('http://'):
                url = request.url.replace('http://', 'https://', 1)
                code = 301
                return redirect(url, code=code)
                                    
    @app.after_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
        return response
        
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .utils import utils as utils_blueprint
    app.register_blueprint(utils_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

    