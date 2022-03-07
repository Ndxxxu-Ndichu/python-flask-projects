import imgkit
from flask import *
from flask_login import login_required, current_user
import random
from . import *
from .models import User, Logo
from datetime import date
import os
from itsdangerous import URLSafeSerializer





main = Blueprint('main', __name__, static_folder='static')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/landing')
@login_required
def landing():
    return render_template('landing.html', name=current_user.name)

@main.route('/invoices')
@login_required
def invoices():
    today = date.today()
    d = today.strftime("%m/%d/%y")
    invo = random.randint(100,99999)
    return render_template('invoices.html', name=current_user.name, invo=invo, d=d)

@main.route('/invoices', methods=['POST'])
@login_required
def invoices_post():
    invo = request.form.get('invo')
    user = request.form.get('user')
    date = request.form.get('date')
    due_date = request.form.get('due_date')

    client_name = request.form.get('client_name')
    client_email = request.form.get('client_email')
    client_phone = request.form.get('client_phone')


    payment_bank = request.form.get('payment_bank')
    payment_acc = request.form.get('payment_acc')

    payment_name = request.form.get('payment_name')
    payment_method = request.form.get('payment_method')

    mongo.db.invoice_details.insert_one({
        'invNo' : invo,
        'user' : user,
        'date' : date,
        'due_date' : due_date,

        'client' : {'client_name' : client_name,
                    'client_email' : client_email,
                    'client_phone' : client_phone
                    },


        'payment' : {'payment_bank' : payment_bank,
                     'payment_acc' : payment_acc,
                     'payment_name' : payment_name,
                     'payment_method' : payment_method
                     },



        'status' : {'paid' : False}
    })



    return redirect(url_for('main.items', invo=invo))


@main.route('/invoices/items/<invo>')
@login_required
def items(invo):
    return render_template('items.html', invo=invo)

@main.route('/invoices/items/<invo>', methods=['POST'])
@login_required
def items_post(invo):

    service_name = request.form.get('service_name')
    service_price = request.form.get('service_price')
    quantity = request.form.get('service_quantity')
    total = request.form.get('service_total')
    tot = int(total)


    mongo.db.item_details.insert_one({
        'services':{
            'user' : current_user.name,
            'invNo': invo,
            'description': service_name,
            'unit_cost': service_price,
            'quantity': quantity,
            'total':tot
        }

    })
    grandTotal = mongo.db.item_details.aggregate([{"$match":{'services.invNo':invo}},{"$group": {'_id': "$services.invNo",'ss': {"$sum": "$services.total"}}}])
    x = (list(grandTotal))
    y=x[-1]


    mongo.db.invoice_details.update_one({'invNo':invo}, {'$set':{'grand_total':y}})

    flash('Item Added,fill in the Form to add another item')





    return redirect(url_for('main.items', invo=invo))

@main.route('/invoices/items/<invo>/preview')
@login_required
def preview(invo):

    owners = User.query.filter_by(name=current_user.name).all()

    images = mongo.db.users.find({'name':current_user.name})

    invoices = mongo.db.invoice_details.find({'invNo' : invo})
    items = mongo.db.item_details.find({'services.invNo':invo})






    return render_template('pdf.html', owners=owners, invoices=invoices, items=items,images=images)

@main.route('/allInvoices')
@login_required
def allInvoices():
    name = current_user.name
    items = mongo.db.item_details.find({'services.user':name})
    invoices = mongo.db.invoice_details.find({'user': name})
    return render_template('all_Invoices.html', invoices=invoices, items=items)


@main.route('/quotations')
@login_required
def quotations():
    quo = random.randint(100, 99999)
    return render_template('quotations.html', quo=quo, name=current_user.name)

@main.route('/quotations',methods=['POST'])
@login_required
def quotations_post():
    quo = request.form.get('quo')
    user = request.form.get('user')
    date = request.form.get('date')


    client_name = request.form.get('client_name')
    client_email = request.form.get('client_email')
    client_phone = request.form.get('client_phone')



    mongo.db.quotation_details.insert({
        'quoNo': quo,
        'user': user,
        'date': date,


        'client': {'client_name': client_name,
                   'client_email': client_email,
                   'client_phone': client_phone
                   },


    })
    return redirect(url_for('main.quoItems', quo=quo))

@main.route('/quotations/quoItems/<quo>')
@login_required
def quoItems(quo):
    return render_template('quoItems.html', quo=quo)

@main.route('/quotations/quoItems/<quo>', methods=['POST'])
@login_required
def quoItems_post(quo):

    service_name = request.form.get('service_name')
    service_price = request.form.get('service_price')
    quantity = request.form.get('service_quantity')
    total = request.form.get('service_total')



    mongo.db.quotation_item_details.insert({
        'services': {
            'quoNo': quo,
            'description': service_name,
            'unit_cost': service_price,
            'quantity': quantity,
            'total': int(total)
        }

    })

    grandTotal = mongo.db.quotation_item_details.aggregate([{"$match": {'services.quoNo': quo}}, {
        "$group": {'_id': "$services.quoNo", 'ss': {"$sum": "$services.total"}}}])

    x = (list(grandTotal))
    y = x[-1]



    mongo.db.quotation_details.update({'quoNo': quo}, {'$set': {'grand_total': y}})




    return redirect(url_for('main.quoItems', quo=quo))

@main.route('/quotations/quoItems/<quo>/preview')
@login_required
def qpreview(quo):
    owners = User.query.all()
    quotations = mongo.db.quotation_details.find({'quoNo' : quo})
    items = mongo.db.quotation_item_details.find({'services.quoNo':quo})
    return render_template('quo.html', owners=owners, quotations=quotations, items=items)

@main.route('/allQuotations')
@login_required
def allQuotations():
    name = current_user.name
    items = mongo.db.quotation_item_details.find({'services.user':name})
    quotations = mongo.db.quotation_details.find({'user': name})
    return render_template('all_Quotations.html', quotations=quotations, items=items)



