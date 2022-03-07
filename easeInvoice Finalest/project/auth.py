from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Logo
from . import *
from flask_mail import Message
from itsdangerous import SignatureExpired, TimedSerializer
from werkzeug.utils import secure_filename
from .s3 import upload_file
import os



auth = Blueprint('auth', __name__,static_folder='static')
s = TimedSerializer('thisisasecretkey')



@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')


    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Please Check your password and try again.')
        return redirect(url_for('auth.login'))




    login_user(user)

    return redirect(url_for('main.landing'))

@auth.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        email = request.form['email']

        token = s.dumps(email, salt='pass-reset')
        msg = Message('Password Reset', sender='ndichumwangi7@gmail.com', recipients=[email])
        link = url_for('auth.passw_reset', token=token, _external=True)
        msg.body = 'Your password reset link is {}'.format(link)
        mail.send(msg)
        return render_template('message_pass_reset.html')
    return render_template('email.html')


@auth.route('/pass_reset/<token>')
def passw_reset(token):
    try:
        email = s.loads(token, salt='pass-reset', max_age=1800)
    except SignatureExpired:
        return 'token expired'

    return redirect(url_for('auth.fg'))


@auth.route('/forgotPass', methods=['GET', 'POST'])
def fg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
           user.password = generate_password_hash(password)
           db.session.commit()
           flash('Password reset succesful')
           return redirect(url_for('auth.login'))
        flash('Email does not exist')

    return render_template('reset.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    website = request.form.get('website')
    phone = request.form.get('phone')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), website=website, phone=phone)

    db.session.add(new_user)
    db.session.commit()



    token = s.dumps(email, salt='email-confirm')
    msg = Message('Confirm Email', sender='ndichumwangi7@gmail.com', recipients=[email])
    link = url_for('auth.confirm_email', token=token, _external=True)
    msg.body = 'Your link is {}'.format(link)
    mail.send(msg)


    return render_template('message_acc_created.html')

@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=1800)

    except SignatureExpired:
        return 'token expired'

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))