# -*- coding: utf-8 -*-
from notifications import show_notification
#from src.database.db_handler import Database
from PyQt4 import QtGui, uic
from PyQt4 import QtCore
from validation_exceptions import FiledsNotFullyFieled, UserAlreadyExists
from register_validator import fields_filling_validator



class update_contact_form(QtGui.QMainWindow):
    def __init__(self):
        super(update_contact_form, self).__init__()
        uic.loadUi('src/ui/update_contact_form.ui', self)

        self.save_but.clicked.connect(self.update_click)
        self.cancel_but.clicked.connect(self.cancel)
        self.delete_contact_but.clicked.connect(self.delete)

        self.db = Database()


    def update_click(self):
        try:
            fields_filling_validator(self.user_name_field.text(), self.phone_field.text(), self.date_field.text())
            user_exists_validation(self.user_name_field.text(), self.phone_field.text(), self.date_field.text())
            self.db.edit_contact()
            self.close()
        except FiledsNotFullyFieled:
            show_notification("Ошибка обновления", "Не все поля заполнены")
        except UserAlreadyExists:
            show_notification("Ошибка обновления", "Данный контакт уже существует")
        except Exception as e:
            print(e)

    
    def delete(self):
        pass 


    def cancel(self):
        self.close()      


    def on_exit_click(self):
        exit()