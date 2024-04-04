# flaskapp/splitting.py

from costsplitter import db

def calculate_balances():
    from costsplitter.models import Expense,User  # Import here to avoid circular imports

    total_expense = Expense.query.with_entities(db.func.sum(Expense.amount)).scalar()
    participant_count = User.query.count()
    split_amount = total_expense / participant_count if participant_count else 0

    balances = {}
    for participant in User.query.all():
        paid_amount = Expense.query.with_entities(db.func.sum(Expense.amount)).filter_by(
            payer_id=participant.id).scalar()
        balances[participant.name] = paid_amount - split_amount if paid_amount else -split_amount

    return balances

def settle_debts(balances):
    # Separate into debtors (owe money) and creditors (owed money)
    debtors = sorted([(name, amount) for name, amount in balances.items() if amount < 0], key=lambda x: x[1])
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
    from costsplitter.models import User  # Import here to avoid circular imports

    transactions_with_links = []
    for debtor_name, creditor_name, amount in transactions:
        creditor = User.query.filter_by(name=creditor_name).first()
        paypal_username = creditor.paypal_username if creditor else None

        if paypal_username:
            paypal_link = f"https://www.paypal.com/paypalme/{paypal_username}"
            transactions_with_links.append((debtor_name, creditor_name, amount, paypal_link))
        else:
            paypal_link = None
            transactions_with_links.append((debtor_name, creditor_name, amount, paypal_link))

    return transactions_with_links

