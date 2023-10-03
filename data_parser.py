import csv
import re
import tempfile

from datetime import datetime
from models import Expense


class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Parser(object):
    def __init__(self, data_file_path, supported_headers):
        self.path = data_file_path

        # Generate a temporary file, which contains all data from
        # file with <data_file_path>
        self.temp_file = tempfile.TemporaryFile("a+t")

        # Copy data from file with <data_file_path> to created temporary file
        with open(self.path, "r") as f:
            data = f.readlines()
            data[0] = ";".join(supported_headers) + "\n"
            self.temp_file.writelines(data)

        # Move the cursor to the beginning of file for reading data
        self.temp_file.seek(0)

    def parse_data(self):
        """ 
        - Get information about date, amount and receiver to create
        Expense() objects.
        Since the application usage is collecting the expense, the transaction with positive
        amount is ignored.
        """
        # Move the cursor to the beginning of file for reading data
        self.temp_file.seek(0)

        # Parse file line-by-line
        list_of_spending = []
        spending_data = csv.DictReader(self.temp_file, delimiter=";")

        for row in spending_data:
            # Get the date, name of receiver and amount
            spending_date_str = row["Date"]
            spending_receiver = row["Receiver"]
            spending_definition = row["Type of event"]
            spending_amount_str = row["Amount"]

            # Convert them to desired format
            # - Datetime object with date format
            spending_date = datetime.strptime(spending_date_str, '%d.%m.%Y').date()
            # - Float format
            spending_amount_float = float(spending_amount_str.replace(",","."))

            # Using <spending_definition> as the <receiver> field in case
            # <spending_receiver> is empty
            if spending_receiver == "":
                spending_receiver = spending_definition

            # Create Spending() object if <spending_amount_float> is negative
            if spending_amount_float < 0:
                spending = Expense(
                        date=spending_date, 
                        receiver=spending_receiver, 
                        amount=abs(spending_amount_float))
                # Add to list
                list_of_spending.append(spending)
        
        return list_of_spending


class Savings_bank_parser(Parser):

    supported_headers = [
        "Date",
        "Receiver",
        "Type of event",
        "Reference / Message",
        "Amount"
    ]

    def __init__(self, data_file_path):
        self.data = None

        try:
            super().__init__(data_file_path, Savings_bank_parser.supported_headers)

            # Create a variable to 
            # Get data from .csv file - row by row
            spending_data = csv.DictReader(self.temp_file, delimiter=";")
            for row in spending_data:
                # Sanity check to make sure each row has all fields in
                # <supported_headers>
                if set(row.keys()) != set(Savings_bank_parser.supported_headers):
                    raise ParseError("Invalid fields in line:\n{}\nThe supported headers of Saastospankki's csv file is: < {} >".
                    format(";".join([ x for x in row.values() if type(x) != list]), " | ".join(Savings_bank_parser.supported_headers)))

                # Sanity check on format of data in each <row>
                self.check_format(row)

                # Parse data and save in variable
                self.data = self.parse_data()
        finally:  
            # Delete the temporary file
            self.temp_file.close()


    def check_format(self, row):
        # Check whether "Date" field has correct format
        try:
            datetime.strptime(row["Date"], "%d.%m.%Y")
        except:
            raise ParseError("Field `Date` must follow format dd.mm.yy\nFailed row: {}".format(row))

        # Check whether "Amount" field contains all numbers
        if not re.match(r'^-?\d+(,\d+)?$', row["Amount"]):
            raise ParseError("Field `Amount` must contain all numbers\nFailed row: {}".format(row))


class S_bank_parser(Parser):

    supported_headers = [
        "Date",
        "Term",
        "Amount",
        "Type of event",
        "Payer",
        "Receiver",
        "Receiver's account number",
        "Receiver's BIC",
        "Reference",
        "Message",
        "Archiving ID"
    ]

    def __init__(self, data_file_path):
        try:
            super().__init__(data_file_path, S_bank_parser.supported_headers)

            # Get data from .csv file - row by row
            spending_data = csv.DictReader(self.temp_file, delimiter=";")
            for row in spending_data:
                # Sanity check to make sure each row has all fields in
                # <supported_headers>
                if set(row.keys()) != set(S_bank_parser.supported_headers):
                    raise ParseError("Invalid fields in row: {}\nThe supported headers of Saastospankki's csv file is: < {} >".
                    format(";".join([ x for x in row.values() if type(x) != list])," | ".join(S_bank_parser.supported_headers)))

                # Sanity check on format of data in each <row>
                self.check_format(row)

                # Parse data and save in variable
                self.data = self.parse_data()
        finally:  
            # Delete the temporary file
            self.temp_file.close()


    def check_format(self, row):
        # Check whether "Date" and "Term" field has correct format
        try:
            datetime.strptime(row["Date"], "%d.%m.%Y")
            datetime.strptime(row["Term"], "%d.%m.%Y")
        except:
            raise ParseError("Field `Date` and `Term` must follow format dd.mm.yy\nFailed row: {}".format(row))

        # Check whether "Amount" field contains all numbers
        if not re.match(r'^[-|+]?\d+(,\d+)?$', row["Amount"]):
            raise ParseError("Field `Amount` must contain all numbers\nFailed row: {}".format(row))
    
        # Check whether "Archiving ID" field contains 21 numbers
        if not re.match(r'^\d{20}$', row["Archiving ID"]):
            raise ParseError("Field `Archiving ID` must contain 20 numbers\nFailed row: {}".format(row))
