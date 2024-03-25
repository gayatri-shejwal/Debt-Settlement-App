# This is the code calculating how much each creditor will get from the debtor's property
# based on the ratio of over total 
def allocate_debt(debt_amount, creditor_dict):
    total_credit = sum(creditor_dict.values())
    allocation = {}
    for creditor, credit_amount in creditor_dict.items():
        allocation[creditor] = debt_amount * (credit_amount / total_credit)
    return allocation

def main():
    debt_amount = float(input("Enter the amount of property: ")) # the debtor's current property, not the amount of debt
    creditor_count = int(input("Enter the number of creditors: ")) # how many creditors the debtor owed 
    creditor_dict = {}
    for i in range(creditor_count):
        creditor = input(f"Enter creditor {i+1}: ") # input creditor's name (e.g A, B, C)
        credit_amount = float(input(f"Enter the amount credited by {creditor}: ")) # how much debt the debtor owed to each creditor
        creditor_dict[creditor] = credit_amount

    allocation = allocate_debt(debt_amount, creditor_dict)
    print("\nAllocation to Creditors:")
    for creditor, amount in allocation.items():
        print(f"{creditor}: {amount}")

if __name__ == "__main__":
    main()
