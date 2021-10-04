# -*- coding: utf-8 -*-
from register_validator import fields_filling_validator, note_add_validator
from validation_exceptions import FiledsNotFullyFieled, UserAlreadyExists
from notifications import show_notification
from src.database.db_handler import db
import mysql.connector.errors
from PyQt4 import QtGui, uic
import notebook


class update_contact_form(QtGui.QMainWindow):
    def __init__(self, **kwargs):
        super(update_contact_form, self).__init__()
        uic.loadUi('src/ui/update_contact_form.ui', self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(u"Добавление/изменение контакта")

        self.save_but.clicked.connect(self.update_click)
        self.cancel_but.clicked.connect(self.cancel)
        self.delete_contact_but.clicked.connect(self.delete)

        self.db = db

        self.isUpdate = kwargs["isUpdate"]
        self.email = kwargs["eml"]
        self.notebook = kwargs["slf"]

        self.k = kwargs
        if not self.isUpdate:
            self.delete_contact_but.deleteLater()
        else:
            self.user_name_field.setText(kwargs["name"])
            self.phone_field.setText(kwargs["phone"])
            self.date_field.setDate(kwargs["birth_date"])


    def update_click(self):
        try:
            fields_filling_validator(self.user_name_field.text(), self.phone_field.text(), self.date_field.text())   
            note_add_validator(self.user_name_field.text(), self.phone_field.text(), self.date_field.text(), self.email)         
            if self.isUpdate:              
                self.db.edit_contact(self.user_name_field.text(), self.phone_field.text(), self.date_field.date().toString("yyyy-M-d"), self.db.get_record_id(self.k["name"], self.k["phone"], self.k["birth_date"].toString("yyyy-M-d")))
            else:
                self.db.add_contact(self.user_name_field.text(), self.phone_field.text(), self.date_field.date().toString("yyyy-M-d"), self.email)

            notebook.update_contact_list(self.notebook)
            self.close()

        except FiledsNotFullyFieled:
            show_notification(self, u"Ошибка обновления", u"Не все поля заполнены")
        except mysql.connector.errors.IntegrityError:
            show_notification(self, u"Ошибка", u"Данный контакт уже существует")
        except UserAlreadyExists:
            show_notification(self, u"Ошибка обновления", u"Данный контакт уже существует")


    
    def delete(self):
        try:
            self.db.del_contact(self.db.get_record_id(self.user_name_field.text(), self.phone_field.text(),\
                 self.date_field.date().toString("yyyy-M-d")))
            notebook.update_contact_list(self.notebook)
            self.close()
        except Exception as e:
            print(e)


    def cancel(self):
        self.close()      


    def on_exit_click(self):
        exit()