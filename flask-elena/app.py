# app.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from app import db
        db.create_all()  # Create database tables
    app.run(debug=True)
