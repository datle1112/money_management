from models import Expense, Category

"""
Create the disk-based database for the application, where all data
about spending/groups.
Consider to implement password to protect personal data
"""
class Storage():
    def __init__(self, session):
        self.session = session

    def get_expense_obj_from_db(self, expense):
        return self.session.query(Expense).filter(
            Expense.receiver == expense.receiver,
            Expense.date == expense.date,
            Expense.amount == expense.amount,
        ).first()


    def add_expenses_to_db(self, expenses):
        for expense in expenses:
            # Check whether <expense> object is already added to the
            # database
            expense_obj = self.get_expense_obj_from_db(expense)
            if expense_obj == None:
                self.session.add(expense)


    def get_receivers_of_expense_from_db(self):
        # Create a list variable to hold receivers of expense
        list_of_receivers = []

        # Get all names of expense from database
        expenses = self.session.query(Expense).all()
        for expense in expenses:
            list_of_receivers.append(expense.receiver)

        # Remove the duplicate elements in <list_of_receivers> to get
        # unique receivers and return
        return list(set(list_of_receivers))


    def get_expenses_based_on_receiver(self, receiver):
        return self.session.query(Expense).filter(
            Expense.receiver == receiver
        ).all()


    def get_expenses_based_on_category(self, category):
        # Get the Category() object that is equivalent with <category>
        # in database
        category_obj_from_db = self.get_category_obj_from_db(category)
        
        # Get ID of the given category
        return self.session.query(Expense).join(Category).filter(
            Category.id == category_obj_from_db.id).all()

    
    def get_expense_with_no_assigned_category(self):
        list_of_expenses_with_no_category = []

        # Get all names of expense from database
        expenses = self.session.query(Expense).all()
        
        # Get the Expense() objects that aren't assigned to
        # any category
        for expense in expenses:
            if expense.category == None:
                list_of_expenses_with_no_category.append(expense)
    
        return list_of_expenses_with_no_category


    def assign_expenses_with_category(self, receiver_of_expenses, category):
        # Get the Expense() objects from the database that match
        # the <receiver_of_expenses>
        modified_expenses = self.get_expenses_based_on_receiver(receiver_of_expenses)

        # Modify the <category> field of each Expense() object in
        # <modified_expense>
        for expense in modified_expenses:
            assigned_category_obj_from_db = self.get_category_obj_from_db(category)
            expense.category = assigned_category_obj_from_db

        # Commit change to database
        self.session.commit()


    def get_all_categories_from_db(self):
        return self.session.query(Category).all()


    def get_category_obj_from_db(self, category):
        return self.session.query(Category).filter(
            Category.name == category.name,
        ).first()


    def add_category_to_db(self, category):
        # Only add category to database if we don't have any
        # category with similar <name> field
        category_obj = self.get_category_obj_from_db(category)
        if category_obj == None:
            self.session.add(category)


    def delete_category_from_db(self, category):
        # Only delete the category that is available in database
        deleted_category = self.get_category_obj_from_db(category)
        if deleted_category != None:
            self.session.delete(category)
        
        self.session.commit()