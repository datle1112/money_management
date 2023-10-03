from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import calculator
from data_parser import *

class Main_Window(QWidget):
    def __init__(self):
        # Define the default value for used variables
        self.file_path = None
        self.display_mode = "individual"
        self.bank = "S-bank"

        # Initialize the main window
        super().__init__()
        # self.setCentralWidget(QWidget())
        self.home_window()

        # self.centralWidget().setLayout(self.final_layout)

    def home_window(self):
        # Defined the needed layouts. The UI uses nested horizontal 
        # and vertical layout.
        self.final_layout = QVBoxLayout()
        self.browse_file_layout = QHBoxLayout()
        self.screen_and_functions_layout = QGridLayout()

        # Configure the browsing feature on UI
        self.init_browse_file_feature()

        # Configure the screen, which displays the information 
        # about expenses as text and graph
        self.init_screen()

        # Configure the feature allows users to choose the Bank,
        # whose file is parsed
        self.init_bank_chosen_feature()

        # Configure the feature allows users to choose display's mode
        self.init_display_mode_chosen_feature()

        # Configure the feature allows users to categorize the expenses 
        # by themselves
        self.init_grouping_feature()
    
        # Configure the feature allows user to load the chosen file 
        # with "Browse" button. In other words, the application starts
        # to parse the chosen file and generate the text - graph
        self.init_load_feature()

        # Finalize the final layout
        self.final_layout.addLayout(self.browse_file_layout)
        self.final_layout.addLayout(self.screen_and_functions_layout)

        # Assign layout to the parent widget
        self.setLayout(self.final_layout)

        # Basic configuration of the main window
        self.setGeometry(0, 0, 900, 600)
        self.setWindowTitle("Money management")


    def init_browse_file_feature(self):
        # Initialize the "Browse" button, which allows user to browse throught
        # filesystem and get the desired file
        # In addition, initialize the text box to display the path of selected
        # file
        self.browse_file_button = QPushButton("Browse...")
        self.line_box = QLineEdit()

        # Set fixed sizes for the Widgets
        self.browse_file_button.setFixedSize(100, 25)
        self.browse_file_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.browse_file_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add the browsing function to layout
        self.browse_file_layout.addWidget(self.browse_file_button) 
        self.browse_file_layout.addWidget(self.line_box)

        # Configure the "clicked" event - occurs when users click the "Browse" button
        self.browse_file_button.clicked.connect(self.browse_file_handler)
 

    def init_screen(self):
        # Add a scene for drawing 2d objects
        # TODO: Find solution to display text on screen
        self.scene = QGraphicsScene()
        self.scene_x_axis = 0
        self.scene_y_axis = 0
        self.scene.setSceneRect(self.scene_x_axis, self.scene_y_axis, 500, 500)

        # Add a view for showing the scene
        self.view = QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.screen_and_functions_layout.addWidget(self.view, 1, 0, 5, 1)


    def init_bank_chosen_feature(self):
        # Create the QGroupBox object that holds selectable values. These
        # choices are displayed as radio buttons
        group_box = QGroupBox("Bank")

        # Set the fixed size for the QGroupBox
        group_box.setFixedSize(200, 150)
        group_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Configure the radio buttons. The "Individual" button
        # is chosen as default
        s_bank_chosen_btn = QRadioButton("S-bank")
        s_bank_chosen_btn.setChecked(True)
        s_bank_chosen_btn.toggled.connect(self.change_bank)

        savings_bank_chosen_btn = QRadioButton("Säästöpankki")
        savings_bank_chosen_btn.toggled.connect(self.change_bank)
        
        # Create a vertical layout to hold radio buttons
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(s_bank_chosen_btn)
        group_box_layout.addWidget(savings_bank_chosen_btn)

        # Wrap the QGroupBox object with radio buttons in the created vertical layout
        group_box.setLayout(group_box_layout)
        self.screen_and_functions_layout.addWidget(group_box, 1, 1, 1, 2)


    def init_display_mode_chosen_feature(self):
        # Create the QGroupBox object that holds selectable values. These
        # choices are displayed as radio buttons
        group_box = QGroupBox("Display mode")

        # Set the fixed size for the QGroupBox
        group_box.setFixedSize(200, 150)
        group_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Configure the radio buttons. The "Individual" button
        # is chosen as default
        display_individual = QRadioButton("Individual")
        display_individual.setChecked(True)
        display_individual.toggled.connect(self.change_display_mode)

        display_categories = QRadioButton("Category based")
        display_categories.toggled.connect(self.change_display_mode)

        # Create a vertical layout to hold radio buttons
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(display_individual)
        group_box_layout.addWidget(display_categories)

        # Wrap the QGroupBox object with radio buttons in the created vertical layout
        group_box.setLayout(group_box_layout)
        self.screen_and_functions_layout.addWidget(group_box, 2, 1, 1, 2)


    def init_grouping_feature(self):
        # Create the button, which is disabled by default
        self.grouping_expenses_btn = QPushButton("Group the expenses")
        self.grouping_expenses_btn.setEnabled(False)

        # Set the fixed size for it
        self.grouping_expenses_btn.setFixedSize(200, 100)
        self.grouping_expenses_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Add button to the layout
        self.screen_and_functions_layout.addWidget(self.grouping_expenses_btn, 3, 1, 1, 2)

        # TODO: Add feature to open new window
        self.grouping_expenses_btn.clicked.connect(self.grouping_expenses_handler)


    def init_load_feature(self):
        # Create the button, which is disabled by default
        self.load_btn = QPushButton("Load")
        # self.load_btn.setEnabled(False)
        
        # Set the fixed size for it
        self.load_btn.setFixedSize(200, 50)
        self.load_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Add button to the layout
        self.screen_and_functions_layout.addWidget(self.load_btn, 5, 1, 1, 2)

        # TODO: Complete code to parse file/saving data to "database"/generate graph
        self.load_btn.clicked.connect(self.load_button_handler)


    def load_button_handler(self):
        print("Parsing file....")
        data = {
            'Asian Aroma': {'amount': 13.0, 'contribution': 1.16},
            'CHU DUC BAO': {'amount': 99.0, 'contribution': 8.81},
            'DAT LE': {'amount': 400.0, 'contribution': 35.58},
            'ELISA OYJ': {'amount': 14.9, 'contribution': 1.33},
            'FITNESS24SEVEN OY': {'amount': 19.9, 'contribution': 1.77},
            'HSL Mobiili': {'amount': 35.9, 'contribution': 3.19},
            'K-supermarket Martinlaaks': {'amount': 13.15, 'contribution': 1.17},
            'MOB.PAY*DUC BAO CHU': {'amount': 30.0, 'contribution': 2.67},
            'MOB.PAY*DUC THANH NGUYEN': {'amount': 313.72, 'contribution': 27.9},
            'MOB.PAY*TRAN QUANG KHOI N': {'amount': 144.0, 'contribution': 12.81},
            'PALVELUMAKSU': {'amount': 0.4, 'contribution': 0.04},
            'PAYPAL *PATREONIREL M': {'amount': 26.78, 'contribution': 2.38},
            'Patreon* Membership': {'amount': 4.63, 'contribution': 0.41},
            'VFI*Toothpicks and Honey': {'amount': 8.9, 'contribution': 0.79}
        }

        # Set initial location of x/y axis
        x_axis = self.scene_x_axis - 50
        y_axis = self.scene_y_axis
        serifFont = QFont("Times", 10)
        square_item = QGraphicsRectItem(x_axis, y_axis, 10, 10)
        square_item.setBrush(QBrush(QColorConstants.Svg.aqua))
        self.scene.addItem(square_item)

        for receiver, info in data:
            square_item = QGraphicsRectItem(x_axis, y_axis, 5, 5)
            text_item = QGraphicsTextItem("{}e () ({}%) {}".format(info["amount"], info["contribution"], receiver))
            text_item.setFont(serifFont)
            text_item.setPos(x_axis, y_axis)
            self.scene.addItem(text_item)
            # Update x/y axis for next Text item
            y_axis = y_axis + 15

        # try:
        #     # Create parser for input file, based on the chosen Bank
        #     if self.bank == "S-bank":
        #         parser = S_bank_parser(self.file_path)
        #     else:
        #         parser = Savings_bank_parser(self.file_path)

        #     # Parse the input file to get information about expense
        #     list_of_expenses = parser.data

        #     # Print it to screen
        #     self.scene.addText(list_of_expenses)

        # except ParseError as e:
        #     self.error_window = Error_Window(e)
        #     self.error_window.show()


    def browse_file_handler(self):
        # Upload the filename to line box
        file_path = QFileDialog.getOpenFileName()
        self.line_box.setText(file_path[0])
        self.file_path = file_path[0]

        # Enable the "Load File" and "Group the Expenses" buttons
        self.load_btn.setEnabled(True)
        self.grouping_expenses_btn.setEnabled(True)

        print(self.file_path)

    
    def grouping_expenses_handler(self):
        # Query the data from the "database" and create a new
        # window object Grouping_Window() based on that
        second_windows = Grouping_Window()
        second_windows.show()

    
    def change_bank(self):
        radio_button = self.sender()

        if radio_button.isChecked():
            print(radio_button.text())

    def change_display_mode(self):
        radio_button = self.sender()

        if radio_button.isChecked():
            self.display_mode = radio_button.text()
            print(self.display_mode)
            # self.label.setText("You have selected : " + radio_button.text())


class Grouping_Window(QWidget):
    def __init__(self):
        super().__init__()

        # Place holder for second window
        print("Open new window")


class Error_Window(QMessageBox):
    def __init__(self, error_msg):
        super().__init__()
        self.setWindowTitle("Error...")
        self.setIcon(QMessageBox.Critical)
        self.setText(error_msg)
