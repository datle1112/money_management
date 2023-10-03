from PyQt5.QtWidgets import ( 
    QWidget, QVBoxLayout, QDesktopWidget, 
    QHBoxLayout, QListWidget, QListWidgetItem, 
    QPushButton, QLabel, QComboBox, QInputDialog
)

from src.gui.notification import Confirm_Window
from src.app.models import *

class Grouping_Window(QWidget):
    def __init__(self, storage):
        super().__init__()
        
        # Storage() object that contains all information about
        # expenses and categories
        self.storage = storage

        # Used variables
        self.chosen_category_name = None
        self.final_layout = QHBoxLayout()
        self.sub_layout = QVBoxLayout()

        # Configure the components of this window
        self.init_expenses_screen()
        self.init_categories_screen()
        self.init_button()

        # Define configuration of this window
        self.setGeometry(0, 0, 600, 400)
        self.setWindowTitle("Expenses Management")
        self.final_layout.addLayout(self.sub_layout)
        self.setLayout(self.final_layout)


    def init_expenses_screen(self):
        # Create a list which temporary shows nothing
        self.receiver_listWidget = QListWidget()
        self.final_layout.addWidget(self.receiver_listWidget)

        # Perform function when doubleclicked event is recognized
        self.receiver_listWidget.itemDoubleClicked.connect(self.showReceiverInfo)


    def init_categories_screen(self):
        self.category_listWidget = QListWidget()
        # Showing all available categories
        for category in self.storage.all_categories:
            QListWidgetItem(category.name, self.category_listWidget)
        self.sub_layout.addWidget(self.category_listWidget)

        # Perform function when doubleclicked event is recognized
        self.category_listWidget.itemDoubleClicked.connect(self.showReceivers)


    def init_button(self):
        # Initialize the buttons for:
        # - Adding new category
        # - Delete chosen category
        self.add_category = QPushButton("Add category")
        self.delete_chosen_category = QPushButton("Delete category")

        self.sub_layout.addWidget(self.add_category)
        self.sub_layout.addWidget(self.delete_chosen_category)

        self.add_category.clicked.connect(self.add_new_category)
        self.delete_chosen_category.clicked.connect(self.delete_category)

    
    def add_new_category(self):
        name, new_name_is_given = QInputDialog.getText(self, 'Create new category', 'Enter name of category')
        if new_name_is_given:
            self.storage.add_category_to_storage(Category(name))
            # Display new one with added
            QListWidgetItem(name, self.category_listWidget)
            self.category_listWidget.update()


    def delete_category(self):
        selected_items = self.category_listWidget.selectedItems()
        for item in selected_items:
            deleted_category = item.text()
            # Pop a window to ask for the confirmation 
            # from users on their action
            self.notify = Confirm_Window("Do you want to delete category `{}`".format(deleted_category))
            self.show()

            # If the pop-up window is executed (OK button 
            # is pressed), execute the action
            if self.notify.exec():
                # Delete the category from Storage() object...
                self.storage.remove_category_from_storage(deleted_category)

                # ...and the UI
                self.category_listWidget.takeItem(self.category_listWidget.row(item))
                self.category_listWidget.update()


    def showReceivers(self):
        # Clear the current display of receivers
        self.receiver_listWidget.clear()

        # Get the name of clicked category
        self.chosen_category_name = [item.text() for item in self.category_listWidget.selectedItems()][0]

        # Get the receiver belong to this category
        receivers = self.storage.get_receivers_based_on_category(self.chosen_category_name)

        # Show them on UI
        for receiver in receivers:
            QListWidgetItem(receiver.name, self.receiver_listWidget)


    def showReceiverInfo(self):
        # Get the modified Receiver() object based on its name
        receiver_name = [item.text() for item in self.receiver_listWidget.selectedItems()][0]
        receiver_obj = self.storage.get_receiver_obj(receiver_name)

        # Launch new window for modifying
        self.modify_window = Modify_Receiver_Window(receiver_obj, self.storage)
        self.modify_window.center()
        self.modify_window.show()

        # Update
        self.showReceivers()


    def center(self):
        # Get current geometry of the window
        geometry = self.frameGeometry()

        # Get the center point of current desktop
        center_point = QDesktopWidget().availableGeometry().center()

        # Move the center of the window to the center of the desktop
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())


class Modify_Receiver_Window(QWidget):
    def __init__(self, receiver_obj, storage):
        super().__init__()
        self.receiver_obj = receiver_obj
        self.storage = storage

        # Get the original category of the modified Receiver() object
        self.original_category_name = self.receiver_obj.category
        self.current_category_name = self.original_category_name

        # Configure the window
        self._layout = QVBoxLayout()
        self.init_UI()
        self.setGeometry(0, 0, 160, 100)
        self.setLayout(self._layout)


    def center(self):
        # Get current geometry of the window
        geometry = self.frameGeometry()

        # Get the center point of current desktop
        center_point = QDesktopWidget().availableGeometry().center()

        # Move the center of the window to the center of the desktop
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())


    def init_UI(self):
        # Plain text about the basic info
        name_item = QLabel("Name: {}".format(self.receiver_obj.name))
        amount_item = QLabel("Amount: {}e".format(self.receiver_obj.get_total_spending_of_receiver()))

        # Creating a combo box widget
        self.categories_combo_box = QComboBox()

        # Get the name of all categories
        name_of_categories = []
        for category_obj in self.storage.all_categories:
            name_of_categories.append(category_obj.name)
        
        # Configure the combo box
        self.categories_combo_box.addItems(name_of_categories)
        self.categories_combo_box.currentIndexChanged.connect(self.change_category)
        self.categories_combo_box.setCurrentText(self.original_category_name)

        # Configure the layout of the window
        self._layout.addWidget(name_item)
        self._layout.addWidget(amount_item)
        self._layout.addWidget(self.categories_combo_box)


    def change_category(self):
        self.current_category_name = self.categories_combo_box.currentText()


    def closeEvent(self, event):
        # If the "category" field is changed, pop a windown
        # to ask for confirmation from users
        if self.current_category_name != self.original_category_name:
            self.notify = Confirm_Window("Do you want to change the category?\n {} -> {}".format(self.original_category_name, self.current_category_name))
            self.show()

            # If users confirm their action (by clicking the "OK" button),
            # execute this action
            if self.notify.exec():
                # Update the "category" field of the <self.receiver_obj> by:
                self.receiver_obj.assign_category_to_receiver(self.current_category_name)

                # Remove the <self.receiver_obj> from its original Category() object
                modified_category_remove = self.storage.get_category_obj(self.original_category_name)
                modified_category_remove.remove_receiver_from_category(self.receiver_obj)

                # Add the <self.receiver_obj> to the chosen Category() object
                modified_category_add = self.storage.get_category_obj(self.current_category_name)
                modified_category_add.add_receiver_to_category(self.receiver_obj)

                # Close the notified window
                event.accept()
            else:
                event.ignore()