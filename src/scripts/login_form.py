# -*- coding: utf-8 -*-
import os.path as path
import sys
sys.path.append(path.abspath("src"))

from notifications import show_notification
from registration_form import registration_form
#from src.database.db_handler import Database
from PyQt4 import QtGui, uic
from PyQt4 import QtCore
from PyQt4.QtGui import QLineEdit
from PyQt4.QtCore import QSettings

class login_form(QtGui.QMainWindow):
    def __init__(self):
        super(login_form, self).__init__()
        uic.loadUi('src/ui/login_window.ui', self)
        self.setFixedSize(self.width(), self.height())

        self.settings = QSettings('Notebook', 'app')

        try:
            print(self.settings.value('auto_log_in').toBool())
            if self.settings.value('auto_log_in').toBool():
                self.login_input.setText(self.settings.value('email').toString())
                self.pass_input.setText(self.settings.value('password').toString())
                self.remember_user_checkbox.setChecked(True)
                self.sign_in_click()
        except:
            pass

        self.sign_in_but.clicked.connect(self.sign_in_click)
        self.cancel_but.clicked.connect(self.cancel_click)
        self.sign_up_but.clicked.connect(self.sign_up_click)       
        self.show_pass_checkbox.toggled.connect(self.show_pass)
        self.remember_user_checkbox.toggled.connect(self.remember_user)
        self.frogot_pass.mousePressEvent = (self.forgot_pass_click)

        #self.db = Database()


    def sign_in_click(self):
        if self.db.sign_in():
            self.close()
        else:
            show_notification(self, u"Ошибка входа", u"Неверный логин или пароль")
        

    def sign_up_click(self):
        self.save_data()
        self.registration = registration_form()
        self.registration.show()  
        

    def forgot_pass_click(self, _):
        self.password_recovery = pass_recovery_form()
        self.password_recovery.show()


    def show_pass(self, state):
        if state:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

    

    def remember_user(self, state):
        if state:
            self.settings.setValue("auto_log_in", "True")
        else:
            self.settings.setValue("auto_log_in", "False")


    def save_data(self):
        self.settings.setValue("email", self.login_input.text())
        self.settings.setValue("password", self.pass_input.text())


    def cancel_click(self):
        exit() 


    def on_exit_click(self):
        exit()