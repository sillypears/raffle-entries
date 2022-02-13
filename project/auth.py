from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(name=name).first()
        print(generate_password_hash(password, method='sha256'))
        if not user or not check_password_hash(user.password, password):
            print('nope')
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        print('loggers')
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))
    else:
        return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
