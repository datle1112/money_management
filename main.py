from src.gui import main_window

import sys
from PyQt5.QtWidgets import QApplication


# Check for python version
if sys.version_info[0] < 3:
    print('You need to run this with Python 3')
    sys.exit(1)


def main():
    # GUI
    app = QApplication(sys.argv)
    gui = main_window.Main_Window()
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()