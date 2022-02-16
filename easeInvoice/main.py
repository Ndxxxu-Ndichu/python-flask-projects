from flask import *
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'this is first page'

@main.route('/landing')
def landing():
    return 'Succesfully loggedin!'

@main.route('/invoices')
def invoices():
    return render_template('invoices.html')