# app/algorithm.py

def calculate_debts(group_id):
    from .models import Group  # Import here to avoid circular imports
    group = Group.query.get(group_id)
    if not group:
        return []
    expenses = group.expenses
    balances = {}

    for expense in expenses:
        if len(expense.debtors) > 0:
            amount_per_debtor = expense.amount / len(expense.debtors)
            for debtor in expense.debtors:
                if debtor.id != expense.payer_id:
                    balances[debtor.id] = balances.get(debtor.id, 0) - amount_per_debtor
                    balances[expense.payer_id] = balances.get(expense.payer_id, 0) + amount_per_debtor

    transactions = simplify_debts(balances)
    return transactions

def simplify_debts(balances):
    creditors = {k: v for k, v in balances.items() if v > 0}
    debtors = {k: -v for k, v in balances.items() if v < 0}
    transactions = []

    while debtors and creditors:
        debtor, debt_amount = debtors.popitem()
        creditor, credit_amount = creditors.popitem()

        transaction_amount = min(debt_amount, credit_amount)
        transactions.append({'debtor': debtor, 'creditor': creditor, 'amount': transaction_amount})

        if debt_amount > credit_amount:
            debtors[debtor] = debt_amount - credit_amount
        elif credit_amount > debt_amount:
            creditors[creditor] = credit_amount - debt_amount

    return transactions