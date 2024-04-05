# flaskapp/models.py
from costsplitter import db


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(100), nullable=False)
    paypal_username = db.Column(db.String(100), unique=True, nullable=False)
    expenses = db.relationship('Expense', backref='payer', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.real_name}, PayPal: {self.paypal_username}>'

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Expense {self.description}, Amount: {self.amount}, Payer ID: {self.payer_id}>'

