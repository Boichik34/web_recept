from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'routes.authorization'


def create_app(config_class=Config):
    global app
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)

    from app import routes

    with app.app_context():
        db.create_all()

    return app


app = create_app()