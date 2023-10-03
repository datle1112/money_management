"""
Unit tests for src/app/models.py
"""
import unittest

from src.app.models import *

class TestModel(unittest.TestCase):
    def test_total_spending_on_receiver_can_be_calculated(self):
        # Prepare the test data
        expense_1 = Expense("K-market", "1.1.2011", 5.5)
        expense_2 = Expense("K-market", "1.1.2011", 10.5)
        expense_3 = Expense("Lidl", "1.1.2011", 12.5)
        receiver_1 = Receiver("K-market")
        receiver_2 = Receiver("Lidl")

        # Assign Expense() objects to Receiver() objects
        receiver_1.add_expense_to_receiver(expense_1)
        receiver_1.add_expense_to_receiver(expense_2)
        receiver_2.add_expense_to_receiver(expense_3)

        # Get the total spending on each receiver
        self.assertEqual(receiver_1.get_total_spending_of_receiver(), 16)
        self.assertEqual(receiver_2.get_total_spending_of_receiver(), 12.5)
 
    def test_total_spending_on_category_can_be_calculated(self):
        # Prepare the test data
        expense_1 = Expense("K-market", "1.1.2011", 5.5)
        expense_2 = Expense("K-market", "1.1.2011", 10.5)
        expense_3 = Expense("Lidl", "1.1.2011", 12.5)
        expense_4 = Expense("Hesburger", "1.1.2011", 20)

        receiver_1 = Receiver("K-market")
        receiver_2 = Receiver("Lidl")
        receiver_3 = Receiver("Hesburger")

        category_1 = Category("Market")
        category_2 = Category("Restaurant")


        # Assign Expense() objects to Receiver() objects
        receiver_1.add_expense_to_receiver(expense_1)
        receiver_1.add_expense_to_receiver(expense_2)
        receiver_2.add_expense_to_receiver(expense_3)
        receiver_3.add_expense_to_receiver(expense_4)

        # Assign Receiver() objects to Category() objects
        category_1.add_receiver_to_category(receiver_1)
        category_1.add_receiver_to_category(receiver_2)
        category_2.add_receiver_to_category(receiver_3)

        # Get the total spending on each receiver
        self.assertEqual(category_1.get_total_spending_of_category(), 28.5)
        self.assertEqual(category_2.get_total_spending_of_category(), 20)