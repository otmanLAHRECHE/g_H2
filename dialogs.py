from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QDialogButtonBox, QVBoxLayout, QLabel, QTableWidgetItem



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



class ChoseYearDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ChoseYearDialog, self).__init__()
        uic.loadUi("./ui/chose_year_dialog.ui", self)

        self.year = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.max = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")



class GardeDialog(QtWidgets.QDialog):
    def __init__(self, year, max):
        super(GardeDialog, self).__init__()
        uic.loadUi("./ui/garde_dialog.ui", self)

        self.year = int(year)
        self.max = int(max)
        self.table_garde = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.save = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.print = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.reset = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.check = self.findChild(QtWidgets.QPushButton, "pushButton_4")

        self.initialising_table()



    def initialising_table(self):
        for i in range(self.table_garde.rowCount()):
            for j in range(self.table_garde.columnCount()):
                if(j == 0 and i < 12):
                    self.table_garde.setItem(i, j, QTableWidgetItem(str(i + 1)))
                elif(j == 1 and i < 11):
                    self.table_garde.setItem(i, j, QTableWidgetItem(str(self.year)))
                else:
                    self.table_garde.setItem(i, j, QTableWidgetItem(str("0")))

    def total(self, item):
        total_x = 0
        total_y = 0
        print(range(self.table_garde.rowCount()))
        print(range(self.table_garde.columnCount()))
        for i in range(self.table_garde.rowCount()):
            total_x = total_x + int(self.table_garde.item(i, item.column()).text()) 
        for j in range(self.table_garde.columnCount()):
            total_y = total_y + int(self.table_garde.item(item.row(), j).text()) 
        self.table_garde.setItem(item.row(), 6, QTableWidgetItem(str(total_x)))
        self.table_garde.setItem(12, item.column(), QTableWidgetItem(str(total_y)))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "You want to exit?"
        dialog = CustomDialog(message)
        if dialog.exec():
            self.close()
        else:
            a0.ignore()
