# Money Management

## 1. Introduction
The purpose of this file is providing information about the structure of `Money Management`
application, as well as the user manual.

`Money Management` application allows users to visualize the data from bank transactions 
in `.csv` format with pie chart and texts. The visualized data point out the total amount
of spending on defined objects and their contribution to all spending.

In addition, users are free to group the expenses into different categories and visualize their 
data, also, in pie chart and texts.

The application supports input files from `S bank` and `Säästöpankki` (or `Saving Bank`).

## 2. File and directory structure

- `main.py` contains the main loop, which launches the program. For the first prototype,
the input .csv file will be given as argument to this script.
- `data_parser.py` contains the functions used to parse the input .csv file.
- `models.py` defines the model of __Expense()__ and __Category()__ objects as well as the
relation between these two in database `sqlite`
- `data_storage.py` defines the method to add/modify/delete data point in database `sqlite`
- `calculator.py` defines the method used to calculate the contribution of each expense to
the total amount of spending
- `tests` contains unittest of the application.
- 
## 3. Installation instructions
User can install all necessary packages by running following command:
```
pip install -r requirements.txt 
```
## 4. User instructions
To use the application, users need to install all necessary packages (step `3. Installation instructions`).
After that, the application can be launched with command:
```
python main.py
```
