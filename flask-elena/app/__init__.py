# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import Config

db = SQLAlchemy()  # Initialize SQLAlchemy here

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .routes import init_routes
    init_routes(app)  # Initialize routes

    return app
