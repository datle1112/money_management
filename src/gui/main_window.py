from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QFont, QBrush, QColor
from PyQt5.QtCore import Qt

from src.app.data_parser import *
from src.app.calculator import *
from src.app.storage import Storage

from src.gui.notification import *
from src.gui.grouping import Grouping_Window

import random

class Main_Window(QWidget):
    def __init__(self):
        # Define the default value for used variables
        self.file_path = None
        self.data_is_loaded = False

        self.bank = "S-bank"
        self.grouping_mode = "individual"
        self.display_order = "ascending"

        # Initialize the storage
        self.storage = Storage()

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

        # Configure the feature allows users to choose grouping's mode
        self.init_grouping_mode_chosen_feature()

        # Configure the feature allows users to choose the display mode of
        # spending info
        self.init_display_mode_chosen_feature()

        # Configure the feature allows users to categorize the expenses 
        # by themselves
        self.init_grouping_feature()
    
        # Configure the feature allows user to load the chosen file 
        # with "Browse" button. In other words, the application starts
        # to parse the chosen file and generate the text - graph
        self.init_load_display_feature()

        # Finalize the final layout
        self.final_layout.addLayout(self.browse_file_layout)
        self.final_layout.addLayout(self.screen_and_functions_layout)

        # Assign layout to the parent widget
        self.setLayout(self.final_layout)

        # Basic configuration of the main window
        self.setGeometry(0, 0, 900, 700)
        self.setWindowTitle("Money management")


    def init_browse_file_feature(self):
        # Initialize the "Browse" button, which allows user to browse through
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
        self.scene = QGraphicsScene()
        self.scene_x_axis = 0
        self.scene_y_axis = 0
        self.scene.setSceneRect(self.scene_x_axis, self.scene_y_axis, 600, 500)

        # Add a view for showing the scene
        self.view = QGraphicsView(self.scene)
        self.view.adjustSize()
        self.view.show()
        self.screen_and_functions_layout.addWidget(self.view, 1, 0, 6, 1)


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


    def init_grouping_mode_chosen_feature(self):
        # Create the QGroupBox object that holds selectable values. These
        # choices are displayed as radio buttons
        group_box = QGroupBox("Grouping mode")

        # Set the fixed size for the QGroupBox
        group_box.setFixedSize(200, 150)
        group_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Configure the radio buttons. The "Individual" button
        # is chosen as default
        display_individual = QRadioButton("Individual")
        display_individual.setChecked(True)
        display_individual.toggled.connect(self.change_grouping_mode)

        display_categories = QRadioButton("Category based")
        display_categories.toggled.connect(self.change_grouping_mode)

        # Create a vertical layout to hold radio buttons
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(display_individual)
        group_box_layout.addWidget(display_categories)

        # Wrap the QGroupBox object with radio buttons in the created vertical layout
        group_box.setLayout(group_box_layout)
        self.screen_and_functions_layout.addWidget(group_box, 2, 1, 1, 2)


    def init_display_mode_chosen_feature(self):
        # Create the QGroupBox object that holds selectable values. These
        # choices are displayed as radio buttons
        group_box = QGroupBox("Display order")

        # Set the fixed size for the QGroupBox
        group_box.setFixedSize(200, 150)
        group_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Configure the radio buttons. The "Individual" button
        # is chosen as default
        ascending_order = QRadioButton("Ascending")
        ascending_order.setChecked(True)
        ascending_order.toggled.connect(self.change_display_mode)

        descending_order = QRadioButton("Descending")
        descending_order.toggled.connect(self.change_display_mode)

        # Create a vertical layout to hold radio buttons
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(ascending_order)
        group_box_layout.addWidget(descending_order)

        # Wrap the QGroupBox object with radio buttons in the created vertical layout
        group_box.setLayout(group_box_layout)
        self.screen_and_functions_layout.addWidget(group_box, 3, 1, 1, 2)


    def init_grouping_feature(self):
        # Create the button, which is disabled by default
        self.grouping_expenses_btn = QPushButton("Group the expenses")
        self.grouping_expenses_btn.setEnabled(False)

        # Set the fixed size for it
        self.grouping_expenses_btn.setFixedSize(200, 100)
        self.grouping_expenses_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Add button to the layout
        self.screen_and_functions_layout.addWidget(self.grouping_expenses_btn, 4, 1, 1, 2)
        self.grouping_expenses_btn.clicked.connect(self.grouping_expenses_handler)


    def init_load_display_feature(self):
        # Create the button, which is disabled when the path 
        # to parsed .csv file isn't provided
        self.load_btn = QPushButton("Load")
        self.display_btn = QPushButton("Display")
        self.load_btn.setEnabled(False)
        self.display_btn.setEnabled(False)
        
        # Set the fixed size for it
        self.load_btn.setFixedSize(200, 50)
        self.load_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.display_btn.setFixedSize(200, 50)
        self.display_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Add button to the layout
        self.screen_and_functions_layout.addWidget(self.load_btn, 5, 1, 1, 2)
        self.screen_and_functions_layout.addWidget(self.display_btn, 6, 1, 1, 2)

        # Connect button with functions
        self.load_btn.clicked.connect(self.load_button_handler)
        self.display_btn.clicked.connect(self.display_button_handler)


    def load_button_handler(self):
        try:
            # Create parser for input file, based on the chosen Bank
            if self.bank == "S-bank":
                S_bank_parser(self.storage, self.file_path)
            else:
                Savings_bank_parser(self.storage, self.file_path)

            # If not error occur, enable the "Display" / "Group the expenses"
            # button and get ready to generate pie chart + text
            self.display_btn.setEnabled(True)
            self.grouping_expenses_btn.setEnabled(True)

            # Notify the user that loading process is done
            self.load_btn.setStyleSheet("background-color : green")

            # Flip the flag
            self.data_is_loaded = True

        except ParseError as e:
            # Notify the user that loading process has errors
            self.load_btn.setStyleSheet("background-color : red")

            self.error_window = Error_Window(e)
            self.error_window.show()


    def display_button_handler(self):
        # Calculate the percentage
        if self.grouping_mode == "individual":    
            spending_data = calculate_percentage_of_individual_receiver(self.storage)
        else:
            spending_data = calculate_percentage_of_categories(self.storage)

        # Remove old items from screen
        for item in self.scene.items():
            self.scene.removeItem(item)

        # Generate random color for pie chart
        self.generate_random_color(spending_data)

        # Generate pie chart
        self.generate_pie_chart(spending_data)

        # Generate display for spending info
        self.generate_display_for_spending_info(spending_data)

        # Disable the "Display" button until users perform further valid
        # actions (load new .csv file, change the displaying method, etc)
        self.display_btn.setEnabled(False)


    def generate_random_color(self, data):
        for receiver in data.keys():
            number = []
            for _ in range(3):
                number.append(random.randrange(0, 255))

            # Update
            data[receiver].update({
                "color" : QColor(number[0],number[1],number[2])})


    def generate_pie_chart(self, data):
        start_angle = 0
        span_angle = 0
        total_percent =  sum([ x["contribution"] for x in data.values()])
        # Max span is 5760, so we have to calculate corresponding span angle
        angle_to_percent = 360 * 16 / total_percent

        # Create pie chart
        for _, info in data.items():
            ellipse = QGraphicsEllipseItem(0, 0, 300, 300)

            # Get the start angle
            ellipse.setStartAngle(start_angle)

            # Get the span angle
            span_angle = round(info["contribution"] * angle_to_percent)
            ellipse.setSpanAngle(span_angle)

            # Set the color
            ellipse.setPen(QPen(Qt.black,  1, Qt.SolidLine))
            ellipse.setBrush(info["color"])

            # Update the start angle
            start_angle = start_angle + span_angle
            self.scene.addItem(ellipse)


    def generate_display_for_spending_info(self, data):
        # Get the list of displayed object according to the current value
        # of self.display_order
        if self.display_order == "ascending":
            list_of_objects = sorted(data, key=lambda x: (data[x]['amount']))
        else:
            list_of_objects = sorted(data, key=lambda x: (data[x]['amount']), reverse=True)

        # Set initial location of x/y axis
        x_axis = self.scene_x_axis + 350
        y_axis = self.scene_y_axis
        serifFont = QFont("Times", 8)

        # Display the expenses with chosen order
        for obj in list_of_objects:
            info = data[obj]
            square_item = QGraphicsRectItem(x_axis - 10, y_axis + 5, 10, 10)
            square_item.setBrush(QBrush(info["color"]))
            self.scene.addItem(square_item)

            text_item = QGraphicsTextItem("{}e ({}%) {}".format(info["amount"], info["contribution"], obj.name))
            text_item.setFont(serifFont)
            text_item.setPos(x_axis, y_axis)
            self.scene.addItem(text_item)
            # Update x/y axis for next Text item
            y_axis = y_axis + 15

        # Print total spending
        total_amount_of_spending = round(sum([ x["amount"] for x in data.values()]), 2)
        text_item = QGraphicsTextItem("Total spending: {}".format(total_amount_of_spending))
        text_item.setFont(QFont("Times", 17))
        text_item.setPos(x_axis - 20, y_axis)
        self.scene.addItem(text_item)


    def browse_file_handler(self):
        # Upload the filename to line box
        file_path = QFileDialog.getOpenFileName()
        self.line_box.setText(file_path[0])
        self.file_path = file_path[0]

        # Enable the "Load File" button
        self.load_btn.setEnabled(True)


    def grouping_expenses_handler(self):
        # Query the data from the "database" and create a new
        # window object Grouping_Window() based on that
        self.second_windows = Grouping_Window(self.storage)
        self.second_windows.center()
        self.second_windows.show()

    
    def change_bank(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.bank = radio_button.text()


    def change_grouping_mode(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.grouping_mode = radio_button.text().lower()

        # Enable the "Display" button if file already loaded
        if self.data_is_loaded:
            self.display_btn.setEnabled(True)


    def change_display_mode(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.display_order = radio_button.text().lower()

        # Enable the "Display" button if file already loaded
        if self.data_is_loaded:
            self.display_btn.setEnabled(True)