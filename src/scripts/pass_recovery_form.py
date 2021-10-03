# -*- coding: utf-8 -*-
from validation_exceptions import PassMissmatching
from register_validator import pass_validator
from notifications import show_notification
from src.database.db_handler import db
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QLineEdit



class pass_recovery_form(QtGui.QMainWindow):
    def __init__(self, email):
        super(pass_recovery_form, self).__init__()
        uic.loadUi("src/ui/set_new_pass.ui", self)
        self.setFixedSize(self.width(), self.height())

        self.ok_but.clicked.connect(self.set_new_pass_click)
        self.cancel_but.clicked.connect(self.cancel_click)
        self. settings = QSettings("notebook", "app")     

        self.email = email
        self.db = db


    def set_new_pass_click(self):
        try:
            pass_validator(self.password_field.text(), self.confirm_pass_field.text())
            self.db.set_new_pass(self.password_field.text(), self.email)
            self.settings.setValue("auto_log_in", "False")
            self.close()

        except PassMissmatching:
            show_notification(self, u"Ошибка смены пароля", u"Введенные пароли не совпадают")
        except Exception as e:
            print(e)     
 

    def cancel_click(self):
        exit() 


    def on_exit_click(self):
        exit()