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
- `main.py` contains the main loop, which launches the GUI
- `src` contains source code of the application. It includes:
    - `src/app` : Contains the logic behinds the basic mechanism of the application.
    - `src/gui` : Contains the scripts that "formulates" the GUI of the application
- `tests` contains unittest of the application.
- `doc` contains the documentation of the application.
- `example` contains the example input files.
More information can be found in `doc/project_documentation.md`.

- `doc` contains the project plan and images about application.

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
More information about the instructions can be found in `doc/project_documentation.md`.