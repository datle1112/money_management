class Category():
    def __init__(self, name):
        self.name = name
        self.list_of_receivers = []

    def add_receiver_to_category(self, added_receiver_obj):
        self.list_of_receivers.append(added_receiver_obj)


    def remove_receiver_from_category(self, removed_receiver_obj):
        for receiver in self.list_of_receivers:
            if receiver.name == removed_receiver_obj.name:
                self.list_of_receivers.remove(removed_receiver_obj)
                break
    
    def get_total_spending_of_category(self):
        total_spending = 0
        for receiver in self.list_of_receivers:
            # Get spending of <receiver>
            spending = receiver.get_total_spending_of_receiver()
            total_spending = total_spending + spending
        return total_spending
    

class Receiver():
    def __init__(self, name):
        self.name = name
        self.list_of_expenses = []
        self.category = "None"

    def add_expense_to_receiver(self, added_expense_obj):
        self.list_of_expenses.append(added_expense_obj)

    def assign_category_to_receiver(self, category):
        self.category = category

    def get_total_spending_of_receiver(self):
        total_spending = 0
        for expense in self.list_of_expenses:
            total_spending = total_spending + expense.amount
        return total_spending

class Expense():
    all_expenses = []
    
    def __init__(self, receiver, date, amount):
        self.receiver = receiver
        self.date = date
        self.amount = amount
