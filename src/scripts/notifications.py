# -*- coding: utf-8 -*-
from PyQt4 import QtGui


def show_notification(self, title, text):
    self.alert = QtGui.QMessageBox()
    self.alert.setWindowTitle(title)
    self.alert.setText(text)
    self.alert.show()