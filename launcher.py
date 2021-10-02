from src.scripts.login_form import login_form
from PyQt4 import QtGui, uic
import sys


def main():
    application = QtGui.QApplication(sys.argv)
    window = login_form()
    window.show()
    application.exec_()


if __name__ == "__main__":
    main()