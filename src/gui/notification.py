from PyQt5.QtWidgets import (
    QMessageBox, QDialog, QDialogButtonBox,
    QVBoxLayout, QLabel, QDesktopWidget
)

class Error_Window(QMessageBox):
    def __init__(self, error):
        super().__init__()
        self.setWindowTitle("Error...")
        self.setIcon(QMessageBox.Critical)
        # Get error message
        error_msg = error.msg
        
        # Set the content of error window
        self.setText("Invalid format of .csv file")
        self.setDetailedText(error_msg)


class Confirm_Window(QDialog):
    def __init__(self, msg):
        super().__init__()

        # Message to display on notification window
        self.msg = msg

        # Configure the function of the window
        self.dialog_window = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialog_window.accepted.connect(self.accept)
        self.dialog_window.rejected.connect(self.reject)

        # Configure the layout of the window
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(self.msg))
        self.layout.addWidget(self.dialog_window)

        # Configure the outline of window
        self.setWindowTitle("Notification")
        self.setLayout(self.layout)

    def center(self):
        # Get current geometry of the window
        geometry = self.frameGeometry()

        # Get the center point of current desktop
        center_point = QDesktopWidget().availableGeometry().center()

        # Move the center of the window to the center of the desktop
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())
