from flask import *
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer, SignatureExpired


app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'c94ecc2e1adc02'
app.config['MAIL_PASSWORD'] = '1be8a6a4addad3'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

s = URLSafeSerializer('Thisisasecret')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return "<form action='/' method='POST'><input name='email'><input type='submit'></form>"

    email = request.form['email']
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confrm Email', sender='ndichumwangi7@gmail.com', recipients=[email])

    link = url_for('confirm_email', token=token, _external=True)

    msg.body = 'Your link is {}'.format(link)

    mail.send(msg)

    return 'the email you entered is {}. the token is {}'.format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
     email = s.loads(token, salt='email-confirm', max_age=20)
    except SignatureExpired:
        return 'The token expired'
    return 'The token works'


if __name__ == '__main__':
    app.run(debug=True)