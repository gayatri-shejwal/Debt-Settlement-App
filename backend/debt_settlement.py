import pandas as pd

# This function calculates how much each debtor owes to the payer
# The input(expenses) accept one payer, multiple debtors, and debt amount


def calculate_debts_python_sorted(expenses):
    balances = {}

    # This part calculates each person's net balance.
    for expense in expenses:
        if expense.amount >= 0:
            # The amount owed per debtor is the total amount divided by the number of debtors
            amount_per_debtor = expense.amount / len(expense.debtors)
            for debtor in expense.debtors:
                if debtor != expense.payer:  # Payer should not owe money to themselves
                    # Update the debtor's balance
                    balances[debtor] = balances.get(
                        debtor, 0) - amount_per_debtor
                    # Update the payer's balance
                    balances[expense.payer] = balances.get(
                        expense.payer, 0) + amount_per_debtor
        else:
            raise ValueError("Expense has to be positive")

    balances_copy = balances.copy()
    # Sorting the net balance using Python Sorted function.
    sorted_balances = sorted(balances_copy.items(), key=lambda x: x[1])
    debtors = 0
    payers = len(sorted_balances) - 1
    transactions = []

    while any(x != 0 for x in [value for key, value in sorted_balances]) and debtors < payers:
        debtor, debtor_balance = sorted_balances[debtors]
        payer, payer_balance = sorted_balances[payers]

        if debtor_balance == 0:
            debtors += 1
            continue
        if payer_balance == 0:
            payers -= 1
            continue

        transfer_amount = min(-debtor_balance, payer_balance)
        debtor_balance += transfer_amount
        payer_balance -= transfer_amount

        transactions.append((debtor, payer, transfer_amount))

        sorted_balances[debtors] = (debtor, debtor_balance)
        sorted_balances[payers] = (payer, payer_balance)

        if debtor_balance == 0:
            debtors += 1
        if payer_balance == 0:
            payers -= 1

    return transactions


def calculate_debts_merge_sort(expenses):
    balances = {}

    # This part calculates each person's net balance.
    for expense in expenses:
        if expense.amount >= 0:
            # The amount owed per debtor is the total amount divided by the number of debtors
            amount_per_debtor = expense.amount / len(expense.debtors)
            for debtor in expense.debtors:
                if debtor != expense.payer:  # Payer should not owe money to themselves
                    # Update the debtor's balance
                    balances[debtor] = balances.get(
                        debtor, 0) - amount_per_debtor
                    # Update the payer's balance
                    balances[expense.payer] = balances.get(
                        expense.payer, 0) + amount_per_debtor
        else:
            raise ValueError("Expense has to be positive")

    balances_copy = balances.copy()
    # Sorting the net balance using Merge Sort function.
    sorted_balances = list(merge_sort_dict_by_value(balances_copy).items())
    debtors = 0
    payers = len(sorted_balances) - 1
    transactions = []

    while any(x != 0 for x in [value for key, value in sorted_balances]) and debtors < payers:
        debtor, debtor_balance = sorted_balances[debtors]
        payer, payer_balance = sorted_balances[payers]

        if debtor_balance == 0:
            debtors += 1
            continue
        if payer_balance == 0:
            payers -= 1
            continue

        transfer_amount = min(-debtor_balance, payer_balance)
        debtor_balance += transfer_amount
        payer_balance -= transfer_amount

        transactions.append((debtor, payer, transfer_amount))

        sorted_balances[debtors] = (debtor, debtor_balance)
        sorted_balances[payers] = (payer, payer_balance)

        if debtor_balance == 0:
            debtors += 1
        if payer_balance == 0:
            payers -= 1

    return transactions

# From this part is defining merge sort function.


def merge_sort(arr, compare_func=None):
    arr_temp = list(arr)
    n = len(arr_temp)

    if n > 1:
        mid = n // 2
        arr_temp_left = arr_temp[:mid]
        arr_temp_right = arr_temp[mid:]

        arr_temp_left = merge_sort(arr_temp_left, compare_func)
        arr_temp_right = merge_sort(arr_temp_right, compare_func)

        i = j = k = 0
        n_left, n_right = len(arr_temp_left), len(arr_temp_right)

        while i < n_left and j < n_right:
            if compare_func(arr_temp_left[i], arr_temp_right[j]):
                arr_temp[k] = arr_temp_left[i]
                i += 1
            else:
                arr_temp[k] = arr_temp_right[j]
                j += 1
            k += 1

        while i < n_left:
            arr_temp[k] = arr_temp_left[i]
            i += 1
            k += 1

        while j < n_right:
            arr_temp[k] = arr_temp_right[j]
            j += 1
            k += 1

    return arr_temp


def merge_sort_dict_by_value(dictionary):
    def compare_dict_items(item1, item2):
        return item1[1] < item2[1]

    items = list(dictionary.items())
    sorted_items = merge_sort(items, compare_func=compare_dict_items)
    return dict(sorted_items)
