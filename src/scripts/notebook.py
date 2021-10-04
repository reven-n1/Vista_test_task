# -*- coding: utf-8 -*-
from update_contact_form import update_contact_form
from validation_exceptions import NoNearestBirth
from notifications import show_notification
from PyQt4.QtGui import QTableWidgetItem
from src.database.db_handler import db
from PyQt4.QtCore import QSettings
import mysql.connector.errors
from PyQt4 import QtGui, uic
from PyQt4 import QtCore
import login_form


class notebook(QtGui.QMainWindow):
    def __init__(self, email):
        super(notebook, self).__init__()
        uic.loadUi("src/ui/notebook.ui", self)
        self.setWindowTitle(u"записная книжка")

        self.user_name.setText(email)
        self.sign_out_event.mousePressEvent = (self.sign_out)
        self.add_contact_event.mousePressEvent = (self.add_contact)
        self.tableWidget.clicked.connect(self.update_contact)

        self.alphabet_list.itemDoubleClicked.connect(self.move_to_selected_part)
        self.settings = QSettings("Notebook", "app")
        self.email = email
        
        self.db = db

        update_contact_list(self)
        self.birthday_list_notification()


    def birthday_list_notification(self):
        try:
            birth_list = ""
            for item in self.db.get_nearest_birthds(self.email):
                birth_list = birth_list + u"{0}   т.-{1}   {2}\n".format(item[0], item[1], item[2])
            show_notification(self, u"Ближайшие дни рождения", birth_list)
        except mysql.connector.errors.InterfaceError:
            pass
        except NoNearestBirth:
            pass
    

    def move_to_selected_part(self, item):
        try:
            for index in range(self.db.get_contacts_count(self.email)+1):
                text = u"{0}".format(item.text())
                row = u"{0}".format(self.tableWidget.item(index,0).text())

                if row[0].upper() in text:
                    self.tableWidget.selectRow(index)
                    break
                
        except Exception as e:
            pass


    def add_contact(self, _):
        self.add_contact = update_contact_form(isUpdate=False, eml = self.email, slf = self)
        self.add_contact.show()


    def update_contact(self, item):
        index = self.tableWidget.selectionModel().currentIndex()
        name = index.sibling(item.row(), 0).data().toString()
        phone = index.sibling(item.row(), 1).data().toString()
        birts_date =index.sibling(item.row(), 2).data().toDate()
        
        self.update_contact = update_contact_form(isUpdate=True, name = name, phone = phone, birth_date = birts_date, eml = self.email, slf = self)
        self.update_contact.show()


    def sign_out(self, _):
        self.settings.setValue("auto_log_in", "False")
        self.back_to_log_in = login_form.login_form()
        self.back_to_log_in.show()
        self.close()      


    def on_exit_click(self):
        exit()


def update_contact_list(self):
        self.tableWidget.setRowCount(self.db.get_contacts_count(self.email))
        try:
            contacts = self.db.get_all_contacts(self.email)
            contacts.sort(key= lambda x: x[0])
            for count, person in enumerate(contacts):
                self.tableWidget.setItem(count, 0, QTableWidgetItem(person[0]))
                self.tableWidget.setItem(count, 1, QTableWidgetItem(person[1]))
                self.tableWidget.setItem(count, 2, QTableWidgetItem(str(person[2])))

        except mysql.connector.errors.InterfaceError:
            pass
        finally:
            header = self.tableWidget.horizontalHeader()
            header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
            header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)