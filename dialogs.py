from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMessageBox, QDialogButtonBox, QVBoxLayout, QLabel, QTableWidgetItem
from threads import *


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
    def __init__(self, worker_id):
        super(ChoseYearDialog, self).__init__()
        uic.loadUi("./ui/chose_year_dialog.ui", self)

        self.chose = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.year = self.findChild(QtWidgets.QLineEdit, "lineEdit_3")
        self.max = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")
        self.worker_id = worker_id
        
        self.year.setEnabled(True)
        self.max.setEnabled(True)

        self.thread = ThreadChoseYear(self.worker_id)
        self.thread._signal_list.connect(self.signal_chose_year)
        self.thread._signal_result.connect(self.signal_chose_year)

        self.chose.currentTextChanged.connect(self.chose_changed)

    def signal_chose_year(self, progress):
        if type(progress) == list:
            if len(progress) > 0:
                for i in range(len(progress)):
                    self.chose.addItem(progress[i])
            

    def chose_changed(self, value):
        if(value == "new_year"):
            self.year.setEnabled(True)
            self.max.setEnabled(True)
        else:
            self.year.setEnabled(False)
            self.max.setEnabled(False)
            connection = sqlite3.connect("data/database.db")
            cur = connection.cursor()
            sql_q = 'SELECT DISTINCT j_s FROM garde WHERE gardien_id= ? and year=?'
            cur.execute(sql_q, (self.worker_id, int(value)))
            results = cur.fetchall()
            connection.close()
            results = results[0]
            self.year.setText(value)
            self.max.setText(results[0])



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
        self.check.clicked.connect(self.calc_total)
        self.initialising_table()



    def initialising_table(self):
        for i in range(self.table_garde.rowCount()):
            for j in range(self.table_garde.columnCount()):
                if(j == 0):
                        self.table_garde.setItem(i, j, QTableWidgetItem(str(i + 1)))
                elif(j == 1):
                        self.table_garde.setItem(i, j, QTableWidgetItem(str(self.year)))
                else:
                    self.table_garde.setItem(i, j, QTableWidgetItem(str("0")))


    def calc_total(self):
        for i in range(self.table_garde.rowCount()):
            total_x = 0
            sup = 0
            for j in range(2, 5):
                total_x = total_x + int(self.table_garde.item(i, j).text()) 
            if total_x > self.max:
                sup = total_x - self.max
                total_x = self.max
                self.table_garde.setItem(i, 6, QTableWidgetItem(str(total_x)))
                self.table_garde.item(i, 6).setBackground(QColor(220,255,220))
                self.table_garde.setItem(i, 5, QTableWidgetItem(str(sup)))
                self.table_garde.item(i, 5).setBackground(QColor(224, 221, 119))
            elif total_x == self.max:
                self.table_garde.setItem(i, 6, QTableWidgetItem(str(total_x)))
                self.table_garde.item(i, 6).setBackground(QColor(220,255,220))
            else:
                self.table_garde.setItem(i, 6, QTableWidgetItem(str(total_x)))
        
        self.alert_("ready to save...")

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "You want to exit?"
        dialog = CustomDialog(message)
        if dialog.exec():
            self.close()
        else:
            a0.ignore()
