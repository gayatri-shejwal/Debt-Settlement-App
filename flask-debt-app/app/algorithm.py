# app/algorithm.py

def calculate_debts(group_id):
    '''
    Calculate debts within a group based on expenses.

    Args:
        group_id (int): The ID of the group.

    Returns:
        list: List of transactions indicating debts to be settled.
    '''
    from .models import Group  # Import here to avoid circular imports
    group = Group.query.get(group_id)
    if not group:
        return []
    expenses = group.expenses
    balances = {}

    # Calculate balances for each debtor and creditor
    for expense in expenses:
        if len(expense.debtors) > 0:
            amount_per_debtor = expense.amount / len(expense.debtors)
            for debtor in expense.debtors:
                if debtor.id != expense.payer_id:
                    balances[debtor.id] = balances.get(
                        debtor.id, 0) - amount_per_debtor
                    balances[expense.payer_id] = balances.get(
                        expense.payer_id, 0) + amount_per_debtor

    transactions = simplify_debts(balances)
    return transactions


def simplify_debts(balances):
    '''
    Simplify debts by minimizing transactions.

    Args:
        balances (dict): A dictionary containing balances for each participant.

    Returns:
        list: List of transactions indicating debts to be settled.
    '''
    balances_copy = balances.copy()
    sorted_balances = sorted(balances_copy.items(), key=lambda x: x[1])
    debtors = 0
    creditors = len(sorted_balances) - 1
    transactions = []

    # Simplify debts by transferring amounts between debtors and creditors
    while debtors <= creditors:
        debtor, debtor_balance = sorted_balances[debtors]
        creditor, creditor_balance = sorted_balances[creditors]

        # Ensure balances are not zero, and debtor and creditor are not the same person
        if debtor_balance == 0 or debtor == creditor:
            debtors += 1
            continue
        if creditor_balance == 0 or debtor == creditor:
            creditors -= 1
            continue

        transfer_amount = min(-debtor_balance, creditor_balance)
        debtor_balance += transfer_amount
        creditor_balance -= transfer_amount

        # Only add the transaction if it's between different people and the amount is not zero
        if debtor != creditor and transfer_amount != 0:
            transactions.append({'debtor': debtor, 'creditor': creditor, 'amount': transfer_amount})

        sorted_balances[debtors] = (debtor, debtor_balance)
        sorted_balances[creditors] = (creditor, creditor_balance)

        if debtor_balance == 0:
            debtors += 1
        if creditor_balance == 0:
            creditors -= 1

    return transactions