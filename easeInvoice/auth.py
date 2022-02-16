from flask import *
from . import *
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeSerializer, SignatureExpired
from flask_mail import Message
from random import randint
from werkzeug.utils import secure_filename
from .s3 import  upload_file
from flask_login import login_required, current_user

import os
from . import db
from flask_login import login_user


auth = Blueprint('auth', __name__)
s = URLSafeSerializer('thisisasecretkey')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not password:
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login'))


    return redirect(url_for('main.landing'))


@auth.route('/forgotPass', methods=['GET', 'POST'])
def fg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        user = User.query.filter_by(email=email).first()

        if user:
         user.password = password
         db.session.commit()
         flash('password reset succesful')
         return redirect(url_for('auth.login'))
        flash('Email does not exist')

    return render_template('resetPass.html')

#remember to hash password











@auth.route('/signup')
def signup():

    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    name = request.form.get('name')
    email = request.form.get('email')
    tel = request.form.get('tel')
    password = request.form.get('password')
    files = request.files['file']
    code = randint(0000, 9999)

    print(files)


    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address Exists')
        return redirect(url_for('auth.signup'))

    new_user = User(name = name, email = email, tel=tel,  password=password, code=code)


    db.session.add(new_user)
    db.session.commit()
    os.makedirs(f"{name}", exist_ok=True)





    token = s.dumps(email, salt='email-confirm')
    msg = Message('Confirm Email', sender='ndichumwangi7@gmail.com', recipients=[email])
    link = url_for('auth.confirm_email', token=token, _external=True)
    msg.body = 'Your link is {}'.format(link)
    mail.send(msg)

    Bucket = "ease-invoice"

    user = request.form['name']
    UPLOAD_FOLDER = f"{user}"
    if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
      upload_file(f"{user}/{f.filename}", Bucket)
    return render_template('confirm.html')

@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=20)
    except SignatureExpired:
        return 'token expired'
    return redirect(url_for('auth.login'))

