"""
Unit tests for src/app/data_parser.py
"""

import unittest
import os
import os.path
from parameterized import parameterized
from tests.common import create_test_file

from src.app.data_parser import *
from src.app.models import *
from src.app.storage import Storage



class TestParser(unittest.TestCase):
    @parameterized.expand([
        [
            "S_bank",
            [
                "29.03.2022;29.03.2022;-4,36;MOBILEPAY;DAT LE;MobilePay Hai Pham;-;-;-;'431871******7336 046560822544';20220329392990651656",
                "28.03.2022;26.03.2022;-13,80;KORTTIOSTO;DAT LE;MOMOTOKO KAMPPI;-;-;-;'431871******7336 220326050814';20220328392991065902"
            ],
            [
                Expense(receiver="MobilePay Hai Pham", date= "29.03.2022", amount= 4.36),
                Expense(receiver="MOMOTOKO KAMPPI", date= "28.03.2022", amount= 13.80)
            ]
        ],
        [
            "Savings_bank", 
            [
                "30.3.2022;K-supermarket Martinlaaks;KORTTIOSTO;Vantaa;-9,5",
                "29.3.2022;ELISA OYJ;TILISIIRTO;55511556588112310295;-14,9"
            ]
            ,
            [
                Expense(receiver="K-supermarket Martinlaaks", date= "30.3.2022", amount= 9.5),
                Expense(receiver="ELISA OYJ", date= "29.3.2022", amount= 14.9)
            ]

        ]
    ])
    def test_parser_can_parse_valid_csv_file_from_supported_banks(self, bank, dataset, expected_result):
        # Prepare the test data
        if bank == "S_bank":
            supported_headers = S_bank_parser.supported_headers
        else:
            supported_headers = Savings_bank_parser.supported_headers

        test_csv_file_path = "valid_csv_file.csv"
        create_test_file(test_csv_file_path, supported_headers, dataset)
        storage = Storage()

        # Run test
        try:
            # Parse the test file with tested parser
            if bank == "S_bank":
                S_bank_parser(storage, test_csv_file_path)
            else:
                Savings_bank_parser(storage, test_csv_file_path)
            list_of_expenses = storage.all_expenses

            # Check number of created Expense() object
            self.assertEqual(len(list_of_expenses), 2)


            # Check attributes of each object
            self.assertEqual(list_of_expenses[0].amount, expected_result[0].amount)
            self.assertEqual(list_of_expenses[0].receiver, expected_result[0].receiver)
            self.assertEqual(list_of_expenses[0].date, expected_result[0].date)

            self.assertEqual(list_of_expenses[1].amount, expected_result[1].amount)
            self.assertEqual(list_of_expenses[1].receiver, expected_result[1].receiver)
            self.assertEqual(list_of_expenses[1].date, expected_result[1].date)
        except ParseError:
            self.fail("Loading a correctly structured file caused an exception")
        finally:
            # Remove the test csv file
            os.remove(test_csv_file_path)

    @parameterized.expand([
        [
            "S_bank",
            [
                "29.03.2022;29.03.2022;-4,36;MOBILEPAY;DAT LE;MobilePay Hai Pham;-;-;-;'431871******7336 046560822544';20220329392990651656",
                "28.03.2022;26.03.2022;-13,80;KORTTIOSTO;DAT LE;MOMOTOKO KAMPPI;-;-;-;'431871******7336 220326050814';20220328392991065902"
            ]
        ],
        [
            "Savings_bank", 
            [
                "30.3.2022;K-supermarket Martinlaaks;KORTTIOSTO;Vantaa;-9,5",
                "29.3.2022;ELISA OYJ;TILISIIRTO;55511556588112310295;-14,9"
            ]
        ]
    ])
    def test_parser_complains_if_input_file_has_invalid_extension(self, bank, dataset):
        # Prepare the test data
        if bank == "S_bank":
            supported_headers = S_bank_parser.supported_headers
        else:
            supported_headers = Savings_bank_parser.supported_headers

        test_csv_file_path = "invalid_csv_file.txt"
        create_test_file(test_csv_file_path, supported_headers, dataset)
        storage = Storage()
        
        # Run test
        try:
            with self.assertRaises(ParseError) as context:
                S_bank_parser(storage, test_csv_file_path)
            self.assertTrue("Invalid file. Please provide bank transaction as csv file" in str(context.exception))

            with self.assertRaises(ParseError) as context:
                Savings_bank_parser(storage, test_csv_file_path)
            self.assertTrue("Invalid file. Please provide bank transaction as csv file" in str(context.exception))
        finally:
            # Remove the test csv file
            os.remove(test_csv_file_path)


    @parameterized.expand([
        [
            [ "2022.03.30;K-supermarket Martinlaaks;KORTTIOSTO;Vantaa;-9,5" ],
            "Field `Date` must follow format dd.mm.yy\n-Receive: {}\n\nFailed row: ".format("2022.03.30")
        ],
        [
            [ "30.3.2022;K-supermarket Martinlaaks;KORTTIOSTO;Vantaa;-4.number" ],
            "Field `Amount` must contain all numbers\n-Receive: {}\n\nFailed row: ".format("-4.number")
        ]
    ])
    def test_parser_for_Saving_bank_complains_if_data_in_input_file_has_invalid_format(self, dataset, error_msg):
        # Prepare the test data
        test_csv_file_path = "invalid_csv_file.csv"
        create_test_file(test_csv_file_path, Savings_bank_parser.supported_headers, dataset)
        storage = Storage()

        # Run test
        try:
            expected_error_msg = error_msg + dataset[0]
            with self.assertRaises(ParseError) as context:
                Savings_bank_parser(storage, test_csv_file_path)
            self.assertTrue(expected_error_msg in str(context.exception))
        finally:
            # Remove the test csv file
            os.remove(test_csv_file_path)


    @parameterized.expand([
        [
            [ "29-03-2022;29/03/2022;-4,36;MOBILEPAY;DAT LE;MobilePay Hai Pham;-;-;-;'431871******7336 046560822544';20220329392990651656" ],
            "Field `Date` and `Term` must follow format dd.mm.yy\n-Receive: {} and {}\n\nFailed row: ".format("29-03-2022", "29/03/2022")
        ],
        [
            [ "29.03.2022;29.03.2022;-4.some_number;MOBILEPAY;DAT LE;MobilePay Hai Pham;-;-;-;'431871******7336 046560822544';20220329392990651656" ],
            "Field `Amount` must contain all numbers\n-Receive: {}\n\nFailed row: ".format("-4.some_number")
        ],
        [
            [ "29.03.2022;29.03.2022;-4,36;MOBILEPAY;DAT LE;MobilePay Hai Pham;-;-;-;'431871******7336 046560822544';1234567891234567891" ],
            "Field `Archiving ID` must contain 20 numbers\n-Receive: {}\n\nFailed row: ".format("1234567891234567891")
        ]
    ])
    def test_parser_for_S_bank_complains_if_data_in_input_file_has_invalid_format(self, dataset, error_msg):
        # Prepare the test data
        test_csv_file_path = "invalid_csv_file.csv"
        create_test_file(test_csv_file_path, S_bank_parser.supported_headers, dataset)
        storage = Storage()

        # Run test
        try:
            expected_error_msg = error_msg + dataset[0]
            with self.assertRaises(ParseError) as context:
                S_bank_parser(storage, test_csv_file_path)
            self.assertTrue(expected_error_msg in str(context.exception))
        finally:
            # Remove the test csv file
            os.remove(test_csv_file_path)