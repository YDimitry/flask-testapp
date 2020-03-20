from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import app_config
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap



db = SQLAlchemy()

login_manager = LoginManager()

def create_app(conf):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[conf])
    app.config.from_pyfile('config.py')

    Bootstrap(app)
    db.init_app(app)
    migrate = Migrate(app, db)


    from app import models

    # @app.route('/')
    # def index_page():
    #     return 'index page'

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    from .home import home as home_blue
    app.register_blueprint(home_blue)

    from .admin import admin as admin_blue
    app.register_blueprint(admin_blue, url_prefix='/admin')

    from .auth import auth as auth_blue
    app.register_blueprint(auth_blue)

    return app
