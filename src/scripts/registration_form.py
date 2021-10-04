# -*- coding: utf-8 -*-
from src.scripts.validation_exceptions import FiledsNotFullyFieled, PassMissmatching, UserAlreadyExists
from src.scripts.register_validator import fields_filling_validator, pass_validator, user_exists_validation
from notifications import show_notification
from src.database.db_handler import db
from PyQt4.QtCore import QSettings
from PyQt4 import QtGui, uic


class registration_form(QtGui.QMainWindow):
    def __init__(self):
        super(registration_form, self).__init__()
        uic.loadUi("src/ui/sign_up.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(u"записная книжка")

        self.ok_but.clicked.connect(self.ok_click)
        self.cancel_but.clicked.connect(self.cancel_click)

        self.settings = QSettings("Notebook", "app")
        
        self.db = db


    def ok_click(self):
        
        name = self.user_name_field.text()
        password = self.password_field.text()
        password_conf = self.confirm_pass_field.text()
        births_date = self.date_field.date().toString("yyyy-M-d")

        # можно было бы написать нормальный qValidator...
        try:
            fields_filling_validator(name, password, password_conf, births_date)
            pass_validator(password, password_conf)
            user_exists_validation(name)
            self.db.sign_up(name, password, births_date)
            self.settings.setValue("auto_log_in", "False")
            self.close()

        except PassMissmatching:
            show_notification(self, u"Ошибка регистрации", u"Пароли не совпадают")
        except FiledsNotFullyFieled:
            show_notification(self, u"Ошибка регистрации", u"Не все поля заполнены")
        except UserAlreadyExists:
            show_notification(self, u"Ошибка регистрации", u"Пользователь с такой почтой уже существует")
        except Exception as e:
            print(e)
        

    def cancel_click(self):
        self.close()


    def on_exit_click(self):
        exit()