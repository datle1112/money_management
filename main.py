from data_storage import Storage
from models import Base, Category, Expense
from data_parser import *
from calculator import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
from os import path
import os
import pprint

from PyQt5.QtWidgets import QApplication
from gui import Main_Window

"""
Version 1.0
"""

# Check for python version
if sys.version_info[0] < 3:
    print('You need to run this with Python 3')
    sys.exit(1)


def main():
    # # Create folder that store file based database
    # if not path.isdir("database"):
    #     os.mkdir("database")

    # parser = Savings_bank_parser("example/Saas_bank.csv")
    # # parser = S_bank_parser("example/S_bank.csv")

    # # Open the connection to database on disk
    # # an Engine, which the Session will use for connection
    # # resources, typically in module scope
    # engine = create_engine("sqlite:///playground/spending.db")

    # # Create a new session based on <engine>
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # # Generate database schema
    # Base.metadata.create_all(engine)

    # # Parse the input file to get information about expense
    # list_of_expenses = parser.data

    # # Add those objects to database
    # database_instance = Storage(session)
    # database_instance.add_expenses_to_db(list_of_expenses)

    # # Calculate the percentage
    # pprint.pprint(calculate_percentage_of_individual_expenses(database_instance))
    
    # # Close the connection to database
    # session.commit()
    # session.close()

    # GUI
    app = QApplication(sys.argv)
    gui = Main_Window()
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()