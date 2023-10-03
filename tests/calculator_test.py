"""
Unit tests for src/app/calculator.py
"""
import unittest
import os

from tests.common import create_test_file

from src.app.data_parser import *
from src.app.models import *
from src.app.storage import Storage
from src.app.calculator import *

TEST_DATA = {
    "S_bank_dataset" : [
            "29.03.2022;29.03.2022;-5;MOBILEPAY;DAT LE;K-supermarket Martinlaaks;-;-;-;'431871******7336 046560822544';20220329392990651656",
            "28.03.2022;26.03.2022;-10;KORTTIOSTO;DAT LE;S-supermarket Martinlaaks;-;-;-;'431871******7336 220326050814';20220328392991065902",
            "28.03.2022;25.03.2022;-5;KORTTIOSTO;DAT LE;K-supermarket Martinlaaks;-;-;-;'431871******7336 220325759993';20220328392990997503",
            "28.03.2022;26.03.2022;-30;KORTTIOSTO;DAT LE;HSL;-;-;-;'431871******7336 220326008223';20220328392990973580"
    ],
    "Saving_bank_dataset" : [
            "30.3.2022;K-supermarket Martinlaaks;KORTTIOSTO;Vantaa;-10",
            "29.3.2022;S-supermarket Martinlaaks;TILISIIRTO;55511556588112310295;-15",
            "26.3.2022;K-supermarket Martinlaaks;KORTTIOSTO;Vantaa;-5",
    ]
}

S_bank_csv_file_path = "S_bank_valid_csv_file.csv"
Saving_bank_csv_file_path = "Saving_bank_valid_csv_file.csv"

def generate_test_data_for_calculating():
        # Prepare the set of tested data
        S_bank_dataset = TEST_DATA["S_bank_dataset"]
        Saving_bank_dataset = TEST_DATA["Saving_bank_dataset"]

        # Create input files with given dataset
        create_test_file(S_bank_csv_file_path, S_bank_parser.supported_headers, S_bank_dataset)
        create_test_file(Saving_bank_csv_file_path, Savings_bank_parser.supported_headers, Saving_bank_dataset)


class TestCalculator(unittest.TestCase):
    def test_calculate_percentage_of_individual_receiver(self):
        # Create the test files
        generate_test_data_for_calculating()
        # Initialize the Storage() object to store data
        storage = Storage()

        # Run test
        try:
            # Parse the test file with tested parser
            S_bank_parser(storage, S_bank_csv_file_path)
            Savings_bank_parser(storage, Saving_bank_csv_file_path)

            # Calculate the percentage
            receivers_and_contributions = calculate_percentage_of_individual_receiver(storage)

            # Check number of receivers
            self.assertEqual(len(receivers_and_contributions.keys()), 3)

            # Check the percentage
            K_market_obj = storage.get_receiver_obj("K-supermarket Martinlaaks")
            S_market_obj = storage.get_receiver_obj("S-supermarket Martinlaaks")
            hsl_obj = storage.get_receiver_obj("HSL")

            self.assertEqual(receivers_and_contributions[K_market_obj]["amount"], 25.0)
            self.assertEqual(receivers_and_contributions[S_market_obj]["amount"], 25.0)
            self.assertEqual(receivers_and_contributions[hsl_obj]["amount"], 30.0)

            self.assertEqual(receivers_and_contributions[K_market_obj]["contribution"], 31.25)
            self.assertEqual(receivers_and_contributions[S_market_obj]["contribution"], 31.25)
            self.assertEqual(receivers_and_contributions[hsl_obj]["contribution"], 37.5)

        finally:
            # Remove the test csv file
            os.remove(S_bank_csv_file_path)
            os.remove(Saving_bank_csv_file_path)


    def test_calculate_percentage_of_categories(self):
        # Create the test files
        generate_test_data_for_calculating()
        # Initialize the Storage() object to store data
        storage = Storage()

        try:
            # Parse the test file with tested parser
            S_bank_parser(storage, S_bank_csv_file_path)
            none_category = storage.get_category_obj("None")

            Savings_bank_parser(storage, Saving_bank_csv_file_path)
            none_category = storage.get_category_obj("None")

            # Generate Category() objects
            market_category = Category("Market")
            none_category = storage.get_category_obj("None")

            # Assign category for Receiver() objects
            K_market_obj = storage.get_receiver_obj("K-supermarket Martinlaaks")
            S_market_obj = storage.get_receiver_obj("S-supermarket Martinlaaks")
            none_category.list_of_receivers.remove(K_market_obj)
            none_category.list_of_receivers.remove(S_market_obj)

            K_market_obj.assign_category_to_receiver("Market")
            S_market_obj.assign_category_to_receiver("Market")

            # Store Receiver() object to its equivalent Category()
            market_category.add_receiver_to_category(K_market_obj)
            market_category.add_receiver_to_category(S_market_obj)

            # Store data to Storage() object
            storage.add_category_to_storage(market_category)

            # Calculate the percentage
            categories_and_contributions = calculate_percentage_of_categories(storage)

            # Check number of categories
            self.assertEqual(len(categories_and_contributions.keys()), 2)

            # Check the percentage
            self.assertEqual(categories_and_contributions[market_category]["amount"], 50)
            self.assertEqual(categories_and_contributions[none_category]["amount"], 30)

            self.assertEqual(categories_and_contributions[market_category]["contribution"], 62.5)
            self.assertEqual(categories_and_contributions[none_category]["contribution"], 37.5)
        finally:
            # Remove the test csv file
            os.remove(S_bank_csv_file_path)
            os.remove(Saving_bank_csv_file_path)