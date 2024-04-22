# app/routes.py
from flask import render_template, request, redirect, url_for, flash

def init_routes(app):
    from .models import User  # Import here to avoid circular imports

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

    
