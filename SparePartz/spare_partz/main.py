from flask import *

from .models import *

from . import db

import os

from .s3_funtions import  upload_file

from werkzeug.utils import secure_filename

from flask_login import login_required, current_user


main = Blueprint('main', __name__)


@main.route ('/')
def index():
    return render_template('index.html')

@main.route ('/home')
def landing():
    return render_template('landing.html')

@main.route('/sell')
@login_required
def sell():
    name = current_user.store
    return render_template('sell.html', name=name)

@main.route('/sell', methods=['POST'])
def sell_post():

    title = request.form.get('title')
    type = request.form.get('type')
    subtype1 = request.form.get('subtype1')
    subtype2 = request.form.get('subtype2')
    subtype3 = request.form.get('subtype3')
    subtype4 = request.form.get('subtype4')
    subtype5 = request.form.get('subtype5')
    subtype6 = request.form.get('subtype6')
    subtype7 = request.form.get('subtype7')
    subtype8 = request.form.get('subtype8')
    subtype9 = request.form.get('subtype9')
    location = request.form.get('location')
    condition = request.form.get('condition')
    description = request.form.get('description')
    price = request.form.get('price')
    status = request.form.get('status')



    if type == "audio":

     audio = Audio(title=title,
                    type=type,
                    subtype1=subtype1,
                    location=location,
                    condition=condition,
                    description=description,
                    price=price,
                   status=status)


     db.session.add(audio)
     db.session.commit()

     name = current_user.store
     os.makedirs(f"{name}/{type}", exist_ok=True)


    elif type == "brakes":

        brakes = Brakes(title=title,
                    type=type,
                    subtype2=subtype2,
                    location=location,
                    condition=condition,
                    description=description,
                    price=price)

        db.session.add(brakes)
        db.session.commit()
        name = current_user.store
        os.makedirs(f"{name}/{type}", exist_ok=True)


    elif type == "engine":

        engine = Engine (title=title,
                         type=type,
                         subtype3=subtype3,
                         location=location,
                         condition=condition,
                         description=description,
                         price=price)

        db.session.add(engine)
        db.session.commit()
        os.mkdir(f"{type}")

    elif type == "exterior":

        exterior = Exterior (title=title,
                             type=type,
                             subtype4=subtype4,
                             location=location,
                             condition=condition,
                             description=description,
                             price=price)
        db.session.add(exterior)
        db.session.commit()



    elif type == "headlights":

        headlights = Headlights(title=title,
                                type=type,
                                subtype5=subtype5,
                                location=location,
                                condition=condition,
                                description=description,
                                price=price)

        db.session.add(headlights)
        db.session.commit()




    elif type == "interior":

        interior = Interior(title=title,
                            type=type,
                            subtype6=subtype6,
                            location=location,
                            condition=condition,
                            description=description,
                            price=price)

        db.session.add(interior)
        db.session.commit()


    elif type == "motorcycle":

        motorcycle = Motorcycle(title=title,
                                type=type,
                                subtype7=subtype7,
                                location=location,
                                condition=condition,
                                description=description,
                                price=price)

        db.session.add(motorcycle)
        db.session.commit()


    elif type == "safety":

        safety = Safety(title=title,
                        type=type,
                        subtype8=subtype8,
                        location=location,
                        condition=condition,
                        description=description,
                        price=price)

        db.session.add(safety)
        db.session.commit()


    else:

        wheels = Wheels(title=title,
                        type=type,
                        subtype9=subtype9,
                        location=location,
                        condition=condition,
                        description=description,
                        price=price)

        db.session.add(wheels)
        db.session.commit()



    BUCKET = "spare-partz"



    type = request.form['type']
    name = current_user.store

    UPLOAD_FOLDER = f"{name}/{type}"
    if request.method == 'POST':
        f = request.files['file']
        type = request.form['type']
        f.save (os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"{name}/{type}/{f.filename}", BUCKET)
        return redirect(url_for('main.landing'))


    return redirect(url_for('main.landing'))