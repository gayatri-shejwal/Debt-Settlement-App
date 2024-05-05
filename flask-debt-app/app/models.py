from . import db  # Import db from the local package init
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    paypal_username = db.Column(db.String(80), unique=True, nullable=False)
    groups = db.relationship('Group', secondary='user_group', backref='members')
    expenses_paid = db.relationship('Expense', backref='payer', foreign_keys='Expense.payer_id')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expenses = db.relationship('Expense', backref='group')

class UserGroup(db.Model):
    __tablename__ = 'user_group'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    debtors = db.relationship('User', secondary='expense_debtors', backref=db.backref('debts'))
    settled = db.Column(db.Boolean, default=False, nullable=False)

class ExpenseDebtor(db.Model):
    __tablename__ = 'expense_debtors'
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), primary_key=True)
    debtor_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

