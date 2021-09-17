from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
# creating the database
db = SQLAlchemy()
DB_NAME  = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('secret_key')
    # for databse
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
    # initialize the database
    db.init_app(app)

    # register the blueprint here
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,Note
    create_database(app)

    # for login 
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access any page'
    login_manager.login_message_category = "error"


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # it will check if database exists
    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created database')