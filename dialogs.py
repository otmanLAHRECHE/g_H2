from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QDialogButtonBox, QVBoxLayout, QLabel



class Worker_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Worker_dialog, self).__init__()
        uic.loadUi("./ui/worker_dialog.ui", self)

        self.nom = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.prenom = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")
        self.service = self.findChild(QtWidgets.QComboBox, "comboBox")


class Service_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Service_dialog, self).__init__()
        uic.loadUi("./ui/services_dialog.ui", self)

        self.list = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.service = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.add_button = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.update_button = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.delete_button = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")


class About_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(About_dialog, self).__init__()
        uic.loadUi("./ui/about.ui", self)

        
        self.frame = self.findChild(QtWidgets.QFrame, "frame")
        self.frame.setStyleSheet("background-image : url(./images/images/epsp.png);")



class CustomDialog(QtWidgets.QDialog):
    def __init__(self, msg, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Alert")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)