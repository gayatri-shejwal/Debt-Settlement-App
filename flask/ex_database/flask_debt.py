from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from debt import calculate_total_debt
import networkx as nx

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
app.app_context().push()


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debtor_id = db.Column(db.Integer, db.ForeignKey(
        'person.id'), nullable=False)
    creditor_id = db.Column(
        db.Integer, db.ForeignKey('person.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    debtor = db.relationship('Person', foreign_keys=[debtor_id])
    creditor = db.relationship('Person', foreign_keys=[creditor_id])


# @app.route('/add_debt', methods=['POST'])
# def add_debt():
#     data = request.json
#     debtor_name = data.get('debtor')
#     creditor_name = data.get('creditor')
#     amount = data.get('amount')

#     # Query persons from the database
#     debtor = Person.query.filter_by(name=debtor_name).first()
#     creditor = Person.query.filter_by(name=creditor_name).first()

#     if not debtor or not creditor:
#         return jsonify({'message': 'Debtor or creditor does not exist.'}), 400

#     # Create a new debt record
#     new_debt = Debt(debtor=debtor, creditor=creditor, amount=amount)
#     db.session.add(new_debt)
#     db.session.commit()

#     return jsonify({'message': 'Debt added successfully.'}), 201

@app.route('/')
@app.route('/home')
def total_debt():
    # Fetch debts from the database
    debts = Debt.query.all()

    # Create a directed graph representing debts
    G = nx.DiGraph()

    # Add edges with debt amounts
    for debt in debts:
        G.add_edge(debt.debtor.name, debt.creditor.name, debt=debt.amount)

    # Calculate total debts using the imported function
    total_debt_result = calculate_total_debt(G)

    # Return the result as JSON
    return total_debt_result
