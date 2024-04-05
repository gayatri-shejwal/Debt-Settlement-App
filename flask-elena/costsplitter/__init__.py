# flaskapp/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Creating your flaskapp instance
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Creating a SQLAlchemy database instance
db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db)

