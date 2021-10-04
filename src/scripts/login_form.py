# -*- coding: utf-8 -*-
from validation_exceptions import UserNotFound, FiledsNotFullyFieled, WrongPassword
from register_validator import fields_filling_validator, user_sign_in_validation
from enter_email_to_reset_pass import enter_email_to_reset_pass
from registration_form import registration_form
from notifications import show_notification
from src.database.db_handler import db
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QLineEdit
from notebook import notebook
from PyQt4 import QtGui, uic
from PyQt4 import QtCore


class login_form(QtGui.QMainWindow):
    def __init__(self):
        super(login_form, self).__init__()
        uic.loadUi("src/ui/login_window.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(u"вход/регистрация")

        self.sign_in_but.clicked.connect(self.sign_in_click)
        self.cancel_but.clicked.connect(self.cancel_click)
        self.sign_up_but.clicked.connect(self.sign_up_click)       
        self.show_pass_checkbox.toggled.connect(self.show_pass)
        self.frogot_pass.mousePressEvent = (self.forgot_pass_click)

        self.settings = QSettings("Notebook", "app")
        self.db = db


    def sign_in_click(self):
        try:
            fields_filling_validator(self.login_input.text(), self.pass_input.text())
            user_sign_in_validation(self.login_input.text(), self.pass_input.text())
            self.save_data()
            self.notebook_form = notebook(self.settings.value("email").toString())
            self.notebook_form.show()
            self.close()
            
        except FiledsNotFullyFieled:
            show_notification(self, u"Ошибка входа", u"Не все поля заполнены")
        except UserNotFound:
            show_notification(self, u"Ошибка входа", u"Неверный логин")
        except WrongPassword:
            show_notification(self, u"Ошибка входа", u"Неверный пароль")
        except Exception as e:
            print(e)
        

    def sign_up_click(self):
        self.registration = registration_form()
        self.registration.show()  
        

    def forgot_pass_click(self, _):
        self.password_recovery = enter_email_to_reset_pass()
        self.password_recovery.show()


    def show_pass(self, state):
        if state:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)


    def save_data(self):
        self.settings.setValue("email", self.login_input.text())
        self.settings.setValue("password", self.pass_input.text())
        self.settings.setValue("auto_log_in", "{}".format(self.remember_user_checkbox.isChecked()))


    def cancel_click(self):
        exit()