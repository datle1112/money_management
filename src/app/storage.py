from src.app.models import *

class QueryError(Exception):
    def __init__(self, message):
        self.msg = message
        super().__init__(self.msg)

class Storage():
    def __init__(self):
        self.all_categories = []
        self.all_receivers = []
        self.all_expenses= []


    def add_expense_to_storage(self, added_expense_obj):
        # Generate equivalent Receiver() object if this object has unique
        # value in "name" field
        self.add_receiver_to_storage(Receiver(added_expense_obj.receiver))

        # Check whether added Expense() object is unique
        duplicated_expense = False
        if self.all_expenses:
            # - If the <all_expenses> list is not empty
            for expense in self.all_expenses:
                if vars(added_expense_obj) == vars(expense):
                    # Raise the flag if added Expense() object already exists. The
                    # existence is verified by checking whether Expense() object's receiver - date - amount
                    # are similar with any objects in <all_expenses> list
                    duplicated_expense = True
                    break
            if not duplicated_expense:
                # Add new object to list <all_expenses>
                self.all_expenses.append(added_expense_obj)
                
                # Assign new Expense() object to the equivalent Receiver() object
                receiver_obj = self.get_receiver_obj(added_expense_obj.receiver)
                receiver_obj.add_expense_to_receiver(added_expense_obj)
        else:
            # - If the <all_expenses> list is empty, append new Expense() object to
            # <all_expenses> list directly
            self.all_expenses.append(added_expense_obj)

            # Assign new Expense() object to the equivalent Receiver() object
            receiver_obj = self.get_receiver_obj(added_expense_obj.receiver)
            receiver_obj.add_expense_to_receiver(added_expense_obj)


    def add_receiver_to_storage(self, added_receiver_obj):
        # Generate equivalent Category() object if this object has unique
        # value in "name" field
        self.add_category_to_storage(Category(added_receiver_obj.category))

        # Get the list of Receiver objects from Storage()
        list_of_receiver_names = [ receiver.name for receiver in self.all_receivers ]

        # Add new Receiver() object to storage if it has unique name 
        if not added_receiver_obj.name in list_of_receiver_names:
            self.all_receivers.append(added_receiver_obj)

            # Assign new Receiver() object to the equivalent Category() object 
            category_obj = self.get_category_obj(added_receiver_obj.category)
            category_obj.add_receiver_to_category(added_receiver_obj)


    def add_category_to_storage(self, added_category_obj):
        # Get the list of Category objects from Storage()
        list_of_category_names = [ receiver.name for receiver in self.all_categories ]

        # Add new Receiver() object to storage if it has unique name 
        if not added_category_obj.name in list_of_category_names:
            self.all_categories.append(added_category_obj)


    def remove_category_from_storage(self, name):
        deleted_category_obj = self.get_category_obj(name)

        # Check whether category "None" is created already
        try:
            none_category = self.get_category_obj("None")
        except:
            none_category = Category("None")
            self.add_category_to_storage(none_category) 

        # Change the "category" field of all Receiver() objects in
        # <deleted_category_obj> to "None".
        # In addition, re-assign them to Category() object with name "None"
        if deleted_category_obj.list_of_receivers:
            for receiver in deleted_category_obj.list_of_receivers:
                receiver.assign_category_to_receiver("None")
                none_category.add_receiver_to_category(receiver)
                
        # Remove the Category() object from <self.all_categories>
        self.all_categories.remove(deleted_category_obj)
    

    def get_receiver_obj(self, name_of_receiver):
        for receiver_obj in self.all_receivers:
            if receiver_obj.name == name_of_receiver:
                return receiver_obj
        raise QueryError("Invalid name of receiver")


    def get_category_obj(self, name_of_category):
        for category_obj in self.all_categories:
            if category_obj.name == name_of_category:
                return category_obj
        raise QueryError("Invalid name of category")


    def get_receivers_based_on_category(self, name_of_category):
        category_obj = self.get_category_obj(name_of_category)
        return  category_obj.list_of_receivers
