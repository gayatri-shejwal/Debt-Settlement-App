# flaskapp/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '020720000'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
