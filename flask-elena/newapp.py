from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from instance.config import Config
from app.models import User

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    @app.route('/')
    def home():
        return render_template('register.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']  # Hash this password before storage
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already taken. Please choose a different one.', 'error')
                return redirect(url_for('register'))
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            try:
                db.session.commit()
                flash('User registered successfully.', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash('Failed to register user. Error: {}'.format(e), 'error')
        return render_template('register.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create database tables for our data models
    app.run(debug=True)
