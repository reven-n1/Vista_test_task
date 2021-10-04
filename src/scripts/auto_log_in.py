#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.scripts.register_validator import user_sign_in_validation
from src.scripts.login_form import login_form
from PyQt4.QtCore import QSettings
from notebook import notebook
from PyQt4 import QtGui, uic
import sys


def log_in():
    application = QtGui.QApplication(sys.argv)
    settings = QSettings("Notebook", "app")
    
    if settings.value("auto_log_in").toBool(): 
        notebook_form = notebook(u"{0}".format(settings.value("email").toString()))
        notebook_form.show()
    else:
        window = login_form()
        window.show()

    application.exec_()