from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_pymongo import PyMongo


db = SQLAlchemy()
mail = Mail()
mongo = PyMongo()



def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile('config.cfg')

    ENV = 'dev'
    if ENV == 'dev':
     app.debug = True
     app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
     app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/flask_auth"
     app.config['MONGO_URI'] = "mongodb+srv://easeInvoice-Ndxxxu:22319989657@easeinvoice-cluster.i4ipk.mongodb.net/easeInvoice?retryWrites=true&w=majority"
    else:
        app.debug = False
        app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ejdoennkprcjzb:eb37b87addf02d0f530740d23ea400edad8a8731f533e2c9662ec3dcfb8bcc59@ec2-54-229-47-120.eu-west-1.compute.amazonaws.com:5432/db7pmpbi2q4cuv"
        app.config['MONGO_URI'] = "mongodb+srv://easeInvoice-Ndxxxu:22319989657@easeinvoice-cluster.i4ipk.mongodb.net/easeInvoice?retryWrites=true&w=majority"

    db.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)



    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app