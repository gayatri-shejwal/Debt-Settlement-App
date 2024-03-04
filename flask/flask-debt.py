from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict

app = Flask(__name__)


# Placeholder for storing expenses and names
expenses = []
participants = set()
paypal_emails = set()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    paypal_email = request.form['paypalEmail']
    participants.add(name)
    paypal_emails.add(paypal_email)
    return redirect(url_for('enter_costs'))

@app.route('/enter_costs')
def enter_costs():
    return render_template('enter_costs.html', participants=list(participants))

@app.route('/submit_cost', methods=['POST'])
def submit_cost():
    name = request.form['name']
    description = request.form['description']
    amount = float(request.form['amount'])
    expenses.append({'name': name, 'description': description, 'amount': amount})
    return redirect(url_for('summary'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    payer = request.form.get('payer')
    amount = float(request.form.get('amount'))
    description = request.form.get('description')
    # Assume 'participants' is a global variable or stored in a session/database
    if payer in participants:
        transactions.append({'name': payer, 'amount': amount, 'description': description})
    else:
        # Handle case where payer is not in participants list
        pass
    return redirect(url_for('summary'))

@app.route('/summary')
def summary():
    total = sum(expense['amount'] for expense in expenses)
    split_amount = total / len(participants) if participants else 0
    # Calculate how much each participant has paid
    paid_by_each = {participant: 0 for participant in participants}
    for expense in expenses:
        paid_by_each[expense['name']] += expense['amount']
    # Calculate balances (how much each person owes or is owed)
    balances = {participant: paid_by_each[participant] - split_amount for participant in participants}
    transactions = settle_debts(balances)
    return render_template('summary.html', expenses=expenses, total=total, split_amount=split_amount,
                           participants=list(participants), balances=balances, transactions=transactions)



def settle_debts(balances):
    # Create a sorted list of people who owe money (negative balance)
    debtors = [(person, balance) for person, balance in balances.items() if balance < 0]
    # Create a sorted list of people who are owed money (positive balance)
    creditors = [(person, balance) for person, balance in balances.items() if balance > 0]

    transactions = []

    # While there are still debtors and creditors
    while debtors and creditors:
        debtor, debt_amount = debtors[0]
        creditor, credit_amount = creditors[0]

        # Calculate the transaction amount
        transaction_amount = min(-debt_amount, credit_amount)

        # Append the transaction
        transactions.append((debtor, creditor, transaction_amount))

        # Adjust the balances
        debt_amount += transaction_amount
        credit_amount -= transaction_amount

        # Update lists
        if debt_amount == 0:
            debtors.pop(0)  # Remove the debtor if their debt is settled
        else:
            debtors[0] = (debtor, debt_amount)  # Update the remaining debt

        if credit_amount == 0:
            creditors.pop(0)  # Remove the creditor if their credit is settled
        else:
            creditors[0] = (creditor, credit_amount)  # Update the remaining credit

    return transactions


def generate_paypal_link(email):
    return f"https://www.paypal.com/paypalme/{email}"


@app.route('/calculate_settlements')
def calculate_settlements():
    balances = calculate_balances(transactions)
    transactions = settle_debts(balances)
    transactions_with_links = []
    for debtor, creditor, amount in transactions:
        # Assuming you have a way to get the creditor's PayPal email, perhaps stored in a database or session
        ownee_email = participants_paypal.get(creditor, '')  # Replace with your method of retrieving emails
        if ownee_email:
            paypal_link = generate_paypal_link(ownee_email, amount)
            transactions_with_links.append((debtor, creditor, amount, paypal_link))

    # Now, transactions_with_links contains all the info you need to display settlements with PayPal links
    return render_template('settlements.html', transactions_with_links=transactions_with_links)


if __name__ == '__main__':
    app.run(debug=True)
