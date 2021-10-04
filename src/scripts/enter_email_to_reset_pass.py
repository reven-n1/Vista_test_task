# -*- coding: utf-8 -*-
from register_validator import fields_filling_validator, change_pass_validator
from validation_exceptions import UserNotFound, FiledsNotFullyFieled
from pass_recovery_form import pass_recovery_form
from notifications import show_notification
from src.database.db_handler import db
from PyQt4 import QtGui, uic
import login_form


class enter_email_to_reset_pass(QtGui.QMainWindow):
    def __init__(self):
        super(enter_email_to_reset_pass, self).__init__()
        uic.loadUi("src/ui/reset_password.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("")

        self.reset_pus_but.clicked.connect(self.cont_pass_reset)
        self.cancel_but.clicked.connect(self.cancel_click)     

        self.db = db
        

    def cont_pass_reset(self):
        try:
            fields_filling_validator(self.email_field.text())
            change_pass_validator(self.email_field.text())
            self.set_new_pass = pass_recovery_form(self.email_field.text())
            self.set_new_pass.show()  
            self.close()

        except UserNotFound:
            show_notification(self, u"Ошибка смены пароля", u"Пользователя с таким email не существует")
        except FiledsNotFullyFieled:
            show_notification(self, u"Ошибка смены пароля", u"Присутсвуют незаполненые поля")    
 

    def cancel_click(self):
        self.close()


    def on_exit_click(self):
        exit()