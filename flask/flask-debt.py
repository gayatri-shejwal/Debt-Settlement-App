from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict

app = Flask(__name__)

# Simplified data structures
expenses = []
participants = {}  # Maps participant names to their PayPal emails


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    real_name = request.form['name']
    # Adjusted to collect PayPal username
    paypal_username = request.form['paypalUsername']
    participants[real_name] = {
        'real_name': real_name, 'paypal_username': paypal_username}
    return redirect(url_for('enter_costs'))


@app.route('/enter_costs')
def enter_costs():
    return render_template('enter_costs.html', participants=list(participants.keys()))


@app.route('/submit_cost', methods=['POST'])
def submit_cost():
    name = request.form['name']
    description = request.form['description']
    amount = float(request.form['amount'])
    expenses.append(
        {'name': name, 'description': description, 'amount': amount})
    return redirect(url_for('summary'))


def calculate_balances(expenses, participants):
    total_expense = sum(expense['amount'] for expense in expenses)
    split_amount = total_expense / len(participants) if participants else 0
    # Start with what each owes
    balances = {participant: -split_amount for participant in participants}
    for expense in expenses:
        balances[expense['name']] += expense['amount']  # Add what they've paid
    return balances


def settle_debts(balances):
    # Separate into debtors (owe money) and creditors (owed money)
    debtors = sorted([(name, amount) for name, amount in balances.items(
    ) if amount < 0], key=lambda x: x[1])
    creditors = sorted([(name, -amount) for name, amount in balances.items() if amount > 0], key=lambda x: x[1],
                       reverse=True)

    transactions = []
    while debtors and creditors:
        debtor, debt_amount = debtors.pop(0)
        creditor, credit_amount = creditors.pop(0)

        # Determine the transaction amount (the lesser of debt or credit amounts)
        transaction_amount = min(-debt_amount, credit_amount)

        transactions.append((debtor, creditor, transaction_amount))

        # Update the remaining amounts
        new_debt_amount = debt_amount + transaction_amount
        new_credit_amount = credit_amount - transaction_amount

        # If there's remaining debt, add the debtor back with the updated amount
        if new_debt_amount < 0:
            debtors.insert(0, (debtor, new_debt_amount))

        # If there's remaining credit, add the creditor back with the updated amount
        if new_credit_amount > 0:
            creditors.insert(0, (creditor, -new_credit_amount))

    return transactions


def calculate_and_link_settlements(transactions):
    transactions_with_links = []
    for debtor, creditor, amount in transactions:
        creditor_info = participants.get(creditor, {})
        paypal_username = creditor_info.get('paypal_username', '')
        if paypal_username:
            paypal_link = f"https://www.paypal.com/paypalme/{paypal_username}"
            transactions_with_links.append(
                (debtor, creditor, amount, paypal_link))
        else:
            # Handle case where PayPal username is missing
            paypal_link = None
            transactions_with_links.append(
                (debtor, creditor, amount, paypal_link))
    return transactions_with_links


@app.route('/summary')
def summary():
    total = sum(expense['amount']
                for expense in expenses)  # Calculate total expenses
    # Calculate split amount
    split_amount = total / len(participants) if participants else 0

    # Calculate the balances based on the current expenses and participants
    balances = calculate_balances(expenses, participants)

    # Determine the transactions needed to settle debts
    transactions = settle_debts(balances)

    # Generate PayPal links for these transactions (if applicable)
    transactions_with_links = calculate_and_link_settlements(transactions)

    # Pass the balances to the template, along with any other data needed for rendering
    return render_template('summary.html', total=total, split_amount=split_amount,
                           expenses=expenses, balances=balances, transactions_with_links=transactions_with_links)


if __name__ == '__main__':
    app.run(debug=True)
