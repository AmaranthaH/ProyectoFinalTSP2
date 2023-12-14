from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#pip install SQLAlchemy
#pip install flask-sqlalchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Datos.db'
    app.config['SECRET_KEY'] = '22'  # Cambia esto a una cadena única y segura

    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    from .routes import main
    app.register_blueprint(main)
    return app
