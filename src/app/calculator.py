def calculate_percentage_of_individual_receiver(storage_obj):
    # An empty dictionary object contains the receivers and their expenditure information
    # as key-value pairs
    receivers_and_contributions = {}

    # Get the list of receivers
    list_of_receivers = storage_obj.all_receivers

    # With each receiver, collect total spending
    for receiver in list_of_receivers:
        spending = receiver.get_total_spending_of_receiver()
        # Update
        receivers_and_contributions.update({
            receiver : {
                "amount" : spending
        }})

    # Calculate the contributed percentage of individual receiver
    # The percentage is rounded to 3 decimals
    total_amount_of_spending = sum([ x["amount"] for x in receivers_and_contributions.values()])
    for receiver, spending_data in receivers_and_contributions.items():
        receivers_and_contributions[receiver].update({
            "contribution" : round(100 * (spending_data["amount"] / total_amount_of_spending), 2)
            })

    return receivers_and_contributions


def calculate_percentage_of_categories(storage_obj):
    # An empty dictionary object contains the categories and their expenditure information
    # as key-value pairs
    categories_and_contributions = {}

    # Get the list of receivers
    list_of_categories = storage_obj.all_categories

    # With each category, collect its total spending
    for category in list_of_categories:
        spending = category.get_total_spending_of_category()
        # Update
        categories_and_contributions.update({
            category : {
                "amount" : spending
        }})

    # Calculate the contributed percentage of individual receiver
    # The percentage is rounded to 3 decimals
    total_amount_of_spending = sum([ x["amount"] for x in categories_and_contributions.values()])
    for category, spending_data in categories_and_contributions.items():
        categories_and_contributions[category].update({
            "contribution" : round(100 * (spending_data["amount"] / total_amount_of_spending), 2)
            })

    return categories_and_contributions
