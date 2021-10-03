# -*- coding: utf-8 -*-
from notifications import show_notification
from src.database.db_handler import db
from PyQt4 import QtGui, uic
from PyQt4 import QtCore
from PyQt4.QtCore import QSettings
from update_contact_form import update_contact_form
import login_form
#from add_contact_form import add_contact_form


class notebook(QtGui.QMainWindow):
    def __init__(self, email):
        super(notebook, self).__init__()
        uic.loadUi('src/ui/notebook.ui', self)

        self.sign_out_event.mousePressEvent = (self.sign_out)
        self.add_contact_event.mousePressEvent = (self.add_contact)

        self.settings = QSettings('Notebook', 'app')
        self.email = email
        self.db = db


    def birthday_list_notification(self):
        pass 


    def update_contact_list(self):
        pass


    def add_contact(self):
        self.add_contact = add_contact_from()
        self.add_contact.show()


    def update_contact(self):
        self.upade_contact = update_contact_form()
        self.upade_contact.show()


    def sign_out(self, _):
        self.settings.setValue("auto_log_in", "False")
        self.back_to_log_in = login_form.login_form()
        self.back_to_log_in.show()
        self.close()      


    def on_exit_click(self):
        exit()