from flask import *

from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

import os
from . import db
from flask_login import login_user



auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')


    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('please check your login details and try again')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.landing'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    password = request.form.get('password')
    store = request.form.get('store')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    tel = request.form.get('tel')



    user = User.query.filter_by(email=email).first()

    if user:
           flash('Email adress exists')
           return redirect(url_for('auth.signup'))

    new_user = User(email=email, password=generate_password_hash(password, method='sha256'), store=store, fname=fname, lname=lname, tel=tel)

    db.session.add(new_user)
    db.session.commit()
    os.mkdir(f"{store}")


    return redirect(url_for('auth.login'))





