def calculate_percentage_of_individual_expenses(database_session):
    # An empty dictionary object contains the receivers and their expense information
    # as key-value pairs
    receivers_and_expenses = {}

    # Get the list of receivers
    list_of_receivers = database_session.get_receivers_of_expense_from_db()

    # With each receiver, collect total spending
    for receiver in list_of_receivers:
        # An empty list that contains total spending of specific <receiver>
        spending = []
        expenses = database_session.get_expenses_based_on_receiver(receiver)
        for expense in expenses:
            spending.append(expense.amount)
        # Update
        receivers_and_expenses.update({
            receiver : {
                "amount" : sum(spending)
        }})

    # Analyze <receiver_and_spending> dictionary to calculate the contributed
    # percentage of individual receiver
    # The percentage is rounded to 2 decimals
    total_amount_of_spending = sum([ x["amount"] for x in receivers_and_expenses.values()])

    for receiver, spending_data in receivers_and_expenses.items():
        receivers_and_expenses[receiver].update({
            "contribution" : round(100 * (spending_data["amount"] / total_amount_of_spending), 2)
            })
        
    return receivers_and_expenses

def calculate_percentage_of_groups(database_session):
    # An empty dictionary object contains the groups and their expense information
    # as -keyvalue pairs
    groups_and_expenses = {}

    # Get the list of categories
    list_of_categories = database_session.get_all_categories_from_db()

    # With each category, collect amount of spending
    for category in list_of_categories:
        # Get list of expense belong to <category>
        list_of_expenses = database_session.get_expenses_based_on_category(category)

        # Get the total amount of spending
        spending = 0
        for expense in list_of_expenses:
            spending = spending + expense.amount
            
        # Update result to <groups_and_expenses>
        groups_and_expenses.update({
            category.name : {
                "amount" : spending
                }})
        
    # Get the total amount of spending that aren't assigned to any category (if any available).
    # This group will be named as "Others"
    list_of_expenses_with_no_category = database_session.get_expense_with_no_assigned_category()
    if list_of_expenses_with_no_category:
        # Get the total amount of spending
        spending = 0
        for expense in list_of_expenses_with_no_category:
            spending = spending + expense.amount

        # Update result to <groups_and_expenses>
        groups_and_expenses.update({
            "Others" : {
                "amount" : spending
            }})

        # Analyze <receiver_and_spending> dictionary to calculate the contributed
        # percentage of individual receiver
        # The percentage is rounded to 2 decimals
        total_amount_of_spending = sum([ x["amount"] for x in groups_and_expenses.values()])

        for category, spending_data in groups_and_expenses.items():
            groups_and_expenses[category].update({
                "contribution" : round(100 * (spending_data["amount"] / total_amount_of_spending), 2)
                })
    
        return groups_and_expenses