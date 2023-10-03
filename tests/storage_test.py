"""
Unit tests for src/app/storage.py
"""
import unittest

from src.app.models import *
from src.app.storage import *


class TestStorage(unittest.TestCase):
    def test_adding_expenses_to_storage(self):
        # Prepare the test data
        expense_1 = Expense("K-market", "1.1.2011", 5.5)
        expense_2 = Expense("K-market", "1.1.2011", 10.5)
        expense_3 = Expense("Lidl", "1.1.2011", 12.5)

        # Initialize the Storage() object to store data
        storage = Storage()

        # Run test
        storage.add_expense_to_storage(expense_1)
        storage.add_expense_to_storage(expense_2)
        storage.add_expense_to_storage(expense_3)

        # Check number of created Expense() objects
        self.assertEqual(len(storage.all_expenses), 3)

        # Check number of created Receiver() objects
        self.assertEqual(len(storage.all_receivers), 2)

        # Check content of the created Receiver() objects
        k_market_receiver = storage.get_receiver_obj("K-market")
        lidl_market_receiver = storage.get_receiver_obj("Lidl")
        self.assertEqual(len(k_market_receiver.list_of_expenses), 2)
        self.assertEqual(k_market_receiver.list_of_expenses, [expense_1, expense_2])

        self.assertEqual(len(lidl_market_receiver.list_of_expenses), 1)
        self.assertEqual(lidl_market_receiver.list_of_expenses, [expense_3])

        # Check number of Receiver() objects in Category() object with
        # name "None" (default category of all newly created Receiver() objects)
        none_category = storage.get_category_obj("None")
        self.assertEqual(len(none_category.list_of_receivers), 2)


    def test_adding_duplicated_expenses_storage(self):
        # Prepare the test data
        expense_1 = Expense("K-market", "1.1.2011", 5.5)
        expense_2 = Expense("K-market", "1.1.2011", 5.5)
        expense_3 = Expense("S-market", "1.1.2011", 10.5)
        expense_4 = Expense("S-market", "1.1.2011", 10.5)
        expense_5 = Expense("Lidl", "1.1.2011", 10.5)

        # Initialize the Storage() object to store data
        storage = Storage()

        # Add Expense() objects to 
        storage.add_expense_to_storage(expense_1)
        storage.add_expense_to_storage(expense_2)
        storage.add_expense_to_storage(expense_3)
        storage.add_expense_to_storage(expense_4)
        storage.add_expense_to_storage(expense_5)

        # Check number of created Expense() objects
        self.assertEqual(len(storage.all_expenses), 3)

        # Check number of created Receiver() objects
        self.assertEqual(len(storage.all_receivers), 3)

        # Check content of the created Receiver() objects
        k_market_receiver = storage.get_receiver_obj("K-market")
        s_market_receiver = storage.get_receiver_obj("S-market")
        lidl_market_receiver = storage.get_receiver_obj("Lidl")
        
        self.assertEqual(len(k_market_receiver.list_of_expenses), 1)
        self.assertEqual(k_market_receiver.list_of_expenses, [expense_1])

        self.assertEqual(len(s_market_receiver.list_of_expenses), 1)
        self.assertEqual(s_market_receiver.list_of_expenses, [expense_3])

        self.assertEqual(len(lidl_market_receiver.list_of_expenses), 1)
        self.assertEqual(lidl_market_receiver.list_of_expenses, [expense_5])

        # Check number of Receiver() objects in Category() object with
        # name "None" (default category of all newly created Receiver() objects)
        none_category = storage.get_category_obj("None")
        self.assertEqual(len(none_category.list_of_receivers), 3)


    def test_adding_receivers_to_storage(self):
        # Prepare the test data
        expense_1 = Expense("K-market", "1.1.2011", 5.5)
        receiver_1 = Receiver("K-market")
        receiver_2 = Receiver("S-market")

        # Initialize the Storage() object to store data
        storage = Storage()

        # Add Expense() object to receiver
        receiver_1.add_expense_to_receiver(expense_1)

        # Add Receiver() objects to 
        storage.add_receiver_to_storage(receiver_1)
        storage.add_receiver_to_storage(receiver_2)

        # Check number of created Receiver() objects
        self.assertEqual(len(storage.all_receivers), 2)

        # Check content of the created Receiver() objects
        k_market_receiver = storage.get_receiver_obj("K-market")
        s_market_receiver = storage.get_receiver_obj("S-market")

        self.assertEqual(len(k_market_receiver.list_of_expenses), 1)
        self.assertEqual(k_market_receiver.list_of_expenses, [expense_1])

        self.assertEqual(len(s_market_receiver.list_of_expenses), 0)
        self.assertEqual(s_market_receiver.list_of_expenses, [])

        # Check number of Receiver() objects in Category() object with
        # name "None" (default category of all newly created Receiver() objects)
        none_category = storage.get_category_obj("None")
        self.assertEqual(len(none_category.list_of_receivers), 2)



    def test_adding_duplicated_receivers_to_storage(self):
        # Prepare the test data
        expense_1 = Expense("K-market", "1.1.2011", 5.5)
        receiver_1 = Receiver("K-market")
        receiver_2 = Receiver("K-market")

        # Initialize the Storage() object to store data
        storage = Storage()

        # Add Expense() object to receiver
        receiver_1.add_expense_to_receiver(expense_1)

        # Add Receiver() objects to 
        storage.add_receiver_to_storage(receiver_1)
        storage.add_receiver_to_storage(receiver_2)

        # Check number of created Receiver() objects
        self.assertEqual(len(storage.all_receivers), 1)

        # Check content of the created Receiver() objects
        self.assertEqual(len(storage.all_receivers[0].list_of_expenses), 1)
        self.assertEqual(storage.all_receivers[0].list_of_expenses, [expense_1])

        # Check number of Receiver() objects in Category() object with
        # name "None" (default category of all newly created Receiver() objects)
        none_category = storage.get_category_obj("None")
        self.assertEqual(len(none_category.list_of_receivers), 1)


    def test_adding_categories_to_storage(self):
        # Prepare the test data
        category_1 = Category("Market")
        category_2 = Category("Restaurant")

        # Initialize the Storage() object to store data
        storage = Storage()
        
        # Add Category() objects to 
        storage.add_category_to_storage(category_1)
        storage.add_category_to_storage(category_2)

        # Check content of the available Category() objects in
        # <storage>
        self.assertEqual(len(storage.all_categories), 2)
        self.assertEqual(len(category_1.list_of_receivers), 0)
        self.assertEqual(len(category_2.list_of_receivers), 0)


    def test_assigning_category_to_receiver(self):
        # Prepare the test data
        receiver_1 = Receiver("K-market")
        receiver_2 = Receiver("S-market")
        receiver_3 = Receiver("Hesburger")
        category_1 = Category("Market")
        category_2 = Category("Restaurant")

        # Initialize the Storage() object to store data
        storage = Storage()
        
        # Add Category() objects to 
        storage.add_category_to_storage(category_1)
        storage.add_category_to_storage(category_2)

        # Assign category to receiver
        receiver_1.assign_category_to_receiver(category_1.name)
        receiver_2.assign_category_to_receiver(category_1.name)
        receiver_3.assign_category_to_receiver(category_2.name)

        category_1.add_receiver_to_category(receiver_1)
        category_1.add_receiver_to_category(receiver_2)
        category_2.add_receiver_to_category(receiver_3)

        # Check content
        self.assertEqual(len(category_1.list_of_receivers), 2)
        self.assertEqual(category_1.list_of_receivers, [receiver_1, receiver_2])

        self.assertEqual(len(category_2.list_of_receivers), 1)
        self.assertEqual(category_2.list_of_receivers, [receiver_3])


    def test_adding_duplicated_categories_to_storage(self):
        # Prepare the test data
        category_1 = Category("Market")
        category_2 = Category("Market")

        # Initialize the Storage() object to store data
        storage = Storage()
        
        # Add Category() objects to 
        storage.add_category_to_storage(category_1)
        storage.add_category_to_storage(category_2)

        # Check content of the available Category() objects in
        # <storage>
        self.assertEqual(len(storage.all_categories), 1)


    def test_get_receivers_based_on_category(self):
        # Prepare the test data
        receiver_1 = Receiver("K-market")
        receiver_2 = Receiver("S-market")
        receiver_3 = Receiver("Hesburger")
        category_1 = Category("Market")
        category_2 = Category("Restaurant")

        # Initialize the Storage() object to store data
        storage = Storage()
        
        # Add Category() objects to 
        storage.add_category_to_storage(category_1)
        storage.add_category_to_storage(category_2)

        # Assign category to receiver
        receiver_1.assign_category_to_receiver(category_1.name)
        receiver_2.assign_category_to_receiver(category_1.name)
        receiver_3.assign_category_to_receiver(category_2.name)

        category_1.add_receiver_to_category(receiver_1)
        category_1.add_receiver_to_category(receiver_2)
        category_2.add_receiver_to_category(receiver_3)

        # Check
        receivers_belong_to_market = storage.get_receivers_based_on_category("Market")
        receiver_belong_to_restaurant = storage.get_receivers_based_on_category("Restaurant")

        self.assertEqual(len(receivers_belong_to_market), 2)
        self.assertEqual(receivers_belong_to_market, [receiver_1 , receiver_2])

        self.assertEqual(len(receiver_belong_to_restaurant), 1)
        self.assertEqual(receiver_belong_to_restaurant, [ receiver_3 ])


    def test_remove_category_from_storage(self):
        # Prepare the test data
        receiver_1 = Receiver("K-market")
        receiver_2 = Receiver("S-market")
        category_1 = Category("Market")

        # Initialize the Storage() object to store data
        storage = Storage()
        
        # Add Category() objects to 
        storage.add_category_to_storage(category_1)

        # Assign category to receiver
        receiver_1.assign_category_to_receiver(category_1.name)
        receiver_2.assign_category_to_receiver(category_1.name)

        category_1.add_receiver_to_category(receiver_1)
        category_1.add_receiver_to_category(receiver_2)

        # Check the content of Category() object before removing
        receivers_belong_to_market = storage.get_receivers_based_on_category("Market")
        self.assertEqual(len(receivers_belong_to_market), 2)
        self.assertEqual(receivers_belong_to_market, [receiver_1 , receiver_2])

        # Removing Category() object
        storage.remove_category_from_storage("Market")
        receiver_belong_to_none = storage.get_receivers_based_on_category("None")
        self.assertEqual(len(receiver_belong_to_none), 2)
        self.assertEqual(receiver_belong_to_none, [receiver_1 , receiver_2])


    def test_query_unavailable_receiver_from_storage(self):
        # Prepare the test data
        receiver_1 = Receiver("K-market")

        # Initialize the Storage() object to store data
        storage = Storage()

        # Add Category() objects to 
        storage.add_receiver_to_storage(receiver_1)

        # Query the Category() object, whose name is different
        # with <category_1>
        with self.assertRaises(QueryError) as context:
            storage.get_receiver_obj("S-market")
        self.assertTrue("Invalid name of receiver" in str(context.exception))        


    def test_query_unavailable_category_from_storage(self):
        # Prepare the test data
        category_1 = Category("Market")

        # Initialize the Storage() object to store data
        storage = Storage()

        # Add Category() objects to 
        storage.add_category_to_storage(category_1)

        # Query the Category() object, whose name is different
        # with <category_1>
        with self.assertRaises(QueryError) as context:
            storage.get_category_obj("Restaurant")
        self.assertTrue("Invalid name of category" in str(context.exception))