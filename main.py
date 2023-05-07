


import sys
import os
import platform

from PyQt5 import Qt, uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QApplication, QMenu, QAction, QToolBar, QMessageBox, QListWidgetItem, QTableWidgetItem
import qdarktheme
import qtawesome as qta
from dialogs import *
from threads import *


os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'EPSP_Djanet.EPSP_Guard.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("./ui/main_ui.ui", self)



        self._createActions()
        self._createMenuBar()
        self._createToolBars()
        self._createStatusBar()

        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.table_workers = self.findChild(QtWidgets.QTableWidget, "tableWidget")

        #self.table_workers.hideColumn(0)
        self.table_workers.setColumnWidth(1, 180)
        self.table_workers.setColumnWidth(2, 180)
        self.table_workers.setColumnWidth(3, 180)
        self.load_workers()
        self.load_services_combo()

    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        dataMenu = QMenu("&Data", self)
        menuBar.addMenu(dataMenu)
        dataMenu.addAction(self.servicesAction)
        dataMenu.addAction(self.exportData)
        dataMenu.addAction(self.exportWorkers)
        dataMenu.addAction(self.importWorkers)
        operationMenu = QMenu("&Operations", self)
        menuBar.addMenu(operationMenu)
        operationMenu.addAction(self.adAction)
        operationMenu.addAction(self.editAction)
        operationMenu.addAction(self.deleteAction)
        operationMenu.addAction(self.detailsAction)
        # Creating menus using a title
        printMenu = menuBar.addMenu("&Print")
        printMenu.addAction(self.printPerService)
        printMenu.addAction(self.printPerwWorker)
        helpMenu = menuBar.addMenu("&About")
        helpMenu.addAction(self.helpAction)

    def _createActions(self):
        # File actions
        self.adAction = QAction(self)
        self.adAction.setText("&Add worker")
        newTip = "Create a new worker"
        self.adAction.setStatusTip(newTip)
        self.adAction.setToolTip(newTip)
        icon = qta.icon("fa.user-plus")
        self.adAction.setIcon(icon)
        self.adAction.triggered.connect(self.workerAddActionClicked_)

        self.editAction = QAction(self)
        self.editAction.setText("&Edit worker")
        icon = qta.icon("fa5s.user-edit")
        self.editAction.setIcon(icon)
        newTip = "Edit selected worker"
        self.editAction.setStatusTip(newTip)
        self.editAction.setToolTip(newTip)
        self.editAction.triggered.connect(self.workerUpdateActionClicked_)

        self.deleteAction = QAction(self)
        self.deleteAction.setText("&Delete worker")
        icon = qta.icon("fa.user-times")
        self.deleteAction.setIcon(icon)
        newTip = "Delete selected worker"
        self.deleteAction.setStatusTip(newTip)
        self.deleteAction.setToolTip(newTip)
        self.deleteAction.triggered.connect(self.workerDeleteActionClicked_)

        self.detailsAction = QAction(self)
        self.detailsAction.setText("&Details")
        icon = qta.icon("mdi.account-details")
        self.detailsAction.setIcon(icon)
        newTip = "Details of selected worker"
        self.detailsAction.setStatusTip(newTip)
        self.detailsAction.setToolTip(newTip)
        self.detailsAction.triggered.connect(self.workerDetailActionClicked_)

        self.helpAction = QAction(self)
        self.helpAction.setText("&About")
        icon = qta.icon("fa5s.hands-helping")
        self.helpAction.setIcon(icon)
        newTip = "About the app"
        self.helpAction.setStatusTip(newTip)
        self.helpAction.setToolTip(newTip)

        self.helpAction.triggered.connect(self.helpActionClicked_)

        self.servicesAction = QAction(self)
        self.servicesAction.setText("&Services")
        icon = qta.icon("fa5s.hospital-user")
        self.servicesAction.setIcon(icon)
        newTip = "Manage the services"
        self.servicesAction.setStatusTip(newTip)
        self.servicesAction.setToolTip(newTip)
        self.servicesAction.triggered.connect(self.servicesActionClicked_)

        self.exportData = QAction(self)
        self.exportData.setText("&Export database")
        icon = qta.icon("mdi.database-arrow-down")
        self.exportData.setIcon(icon)
        newTip = "Export the database"
        self.exportData.setStatusTip(newTip)
        self.exportData.setToolTip(newTip)

        self.exportWorkers= QAction(self)
        self.exportWorkers.setText("&Export workers")
        icon = qta.icon("fa5s.file-export")
        self.exportWorkers.setIcon(icon)
        newTip = "Export the saved workers"
        self.exportWorkers.setStatusTip(newTip)
        self.exportWorkers.setToolTip(newTip)

        self.importWorkers= QAction(self)
        self.importWorkers.setText("&Import workers")
        icon = qta.icon("fa5s.file-import")
        self.importWorkers.setIcon(icon)
        newTip = "Import workers"
        self.importWorkers.setStatusTip(newTip)
        self.importWorkers.setToolTip(newTip)

        self.printPerService= QAction(self)
        self.printPerService.setText("&Print per service")
        icon = qta.icon("ri.printer-cloud-line")
        self.printPerService.setIcon(icon)
        newTip = "Print per service"
        self.printPerService.setStatusTip(newTip)
        self.printPerService.setToolTip(newTip)

        self.printPerwWorker= QAction(self)
        self.printPerwWorker.setText("&Print per worker")
        icon = qta.icon("ri.printer-line")
        self.printPerwWorker.setIcon(icon)
        newTip = "Print per worker"
        self.printPerwWorker.setStatusTip(newTip)
        self.printPerwWorker.setToolTip(newTip)

        self.find_worker = QtWidgets.QLineEdit()
        self.find_worker.setPlaceholderText("Find worker")
        newTip = "Find worker"
        self.find_worker.setStatusTip(newTip)
        self.find_worker.setToolTip(newTip)
        self.find_worker.textChanged.connect(self.filter_workers)

        

    def _createToolBars(self):
        # data toolbar
        operationToolBar = self.addToolBar("Operation")
        operationToolBar.addAction(self.adAction)
        operationToolBar.addAction(self.editAction)
        operationToolBar.addAction(self.deleteAction)
        operationToolBar.addAction(self.detailsAction)
        operationToolBar.addWidget(self.find_worker)
        # Edit toolbar
        dataToolBar = QToolBar("Data", self)
        self.addToolBar(dataToolBar)
        dataToolBar.addAction(self.servicesAction)
        dataToolBar.addAction(self.exportData)
        dataToolBar.addAction(self.exportWorkers)
        dataToolBar.addAction(self.importWorkers)

        printToolBar = QToolBar("Print", self)
        self.addToolBar(printToolBar)
        printToolBar.addAction(self.printPerService)
        printToolBar.addAction(self.printPerwWorker)
    
    def _createStatusBar(self):
        self.statusbar = self.statusBar()

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def helpActionClicked_(self):
        self.dialog = About_dialog()
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()
    def servicesActionClicked_(self):
        self.dialog = Service_dialog()
        self.dialog.show()
        self.dialog.add_button.clicked.connect(self._service_add_clicked)
        self.dialog.update_button.clicked.connect(self._service_update_clicked)
        self.dialog.delete_button.clicked.connect(self._service_delete_clicked)
        self.load_service_all()

    def load_services_combo(self):
        connection = sqlite3.connect("data/database.db")
        cur = connection.cursor()
        sql_q = 'SELECT service_name FROM service'
        cur.execute(sql_q)
        self.service_combo = cur.fetchall()
        connection.close()

    def workerAddActionClicked_(self):
        self.load_services_combo()
            
        self.dialog = Worker_dialog()
        self.dialog.setWindowTitle("add new worker")        
        for i in range(len(self.service_combo)):
            serv = self.service_combo[i]
            self.dialog.service.addItem(serv[0])
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        if self.dialog.exec():
            if(self.dialog.nom.text() == "" or self.dialog.prenom.text() == ""):
                self.alert_("error in firstname or lastname")
            else:
                self.thread = ThreadAddWorker(self.dialog.nom.text(), self.dialog.prenom.text(), self.dialog.service.currentText()) 
                self.thread._signal.connect(self.signal_add_worker)
                self.thread._signal_result.connect(self.signal_add_worker)
                self.thread.start()

    def signal_add_worker(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        else:
            self.progress.setValue(0)
            self.load_workers()
    
    
    def workerUpdateActionClicked_(self):
        if(self.table_workers.currentRow() == -1):
            self.alert_("select one worker")
        else:
            self.dialog = Worker_dialog()
            self.dialog.setWindowTitle("update worker")
            self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            for i in range(len(self.service_combo)):
                serv = self.service_combo[i]
                self.dialog.service.addItem(serv[0])
            self.dialog.nom.setText(self.table_workers.item(self.table_workers.currentRow(),1).text())
            self.dialog.prenom.setText(self.table_workers.item(self.table_workers.currentRow(),2).text())
            self.dialog.service.setCurrentText(self.table_workers.item(self.table_workers.currentRow(),3).text())
            self.dialog.show()

        if self.dialog.exec():
            if(self.dialog.nom.text() == "" or self.dialog.prenom.text() == ""):
                self.alert_("error in firstname or lastname")
            else:
                self.thread = ThreadUpdateWorker(self.table_workers.item(self.table_workers.currentRow(),0).text(), self.dialog.nom.text(), self.dialog.prenom.text(), self.dialog.service.currentText()) 
                self.thread._signal.connect(self.signal_update_worker)
                self.thread._signal_result.connect(self.signal_update_worker)
                self.thread.start()

    def signal_update_worker(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        else:
            self.progress.setValue(0)
            self.load_workers()

    
    def workerDeleteActionClicked_(self):
        if(self.table_workers.currentRow() == -1):
            self.alert_("select one worker")
        else:
            message = "You want to delete this worker?"
            dialog = CustomDialog(message)
            if dialog.exec():
                self.thread = ThreadDeleteWorker(self.table_workers.item(self.table_workers.currentRow(), 0).text()) 
                self.thread._signal.connect(self.signal_delete_worker)
                self.thread._signal_result.connect(self.signal_delete_worker)
                self.thread.start()
            else:
                dialog.close()

    def signal_delete_worker(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        else:
            self.progress.setValue(0)
            self.load_workers()

    
    def workerDetailActionClicked_(self):
        if(self.table_workers.currentRow() == -1):
            self.alert_("select one worker")
        else:
            message = "You want to delete this worker?"
            dialog = ChoseYearDialog()
            if dialog.exec():
                if dialog.year.text() == "" or len(dialog.year.text()) > 4 or (dialog.max.text() != "6" and dialog.max.text() != "10"):
                    self.alert_("chose a valide year")
                else:
                    dialog.close()
                    self.garde_dialog = GardeDialog(dialog.year.text(), dialog.max.text())
                    self.garde_dialog.show()

            else:
                dialog.close()
                


    def _service_add_clicked(self):
        if self.dialog.service.text() == "":
            self.alert_("service name is invalide!!")
        else:
            self.thread = ThreadAddService(self.dialog.service.text())
            self.thread._signal.connect(self.signal_add_service)
            self.thread._signal_result.connect(self.signal_add_service)
            self.thread.start()

    def _service_update_clicked(self):
        if self.dialog.service.text() == "":
            self.alert_("service name is invalide!!")
        elif self.dialog.list.currentItem() == None:
            self.alert_("select a service to update!!")
        else:
            self.thread = ThreadUpdateService(self.dialog.list.currentItem().text() ,self.dialog.service.text())
            self.thread._signal.connect(self.signal_update_service)
            self.thread._signal_result.connect(self.signal_update_service)
            self.thread.start()

    def _service_delete_clicked(self):
        if self.dialog.list.currentItem() == None:
            self.alert_("select a service to delete!!")
        else:
            self.thread = ThreadDeleteService(self.dialog.list.currentItem().text())
            self.thread._signal.connect(self.signal_delete_service)
            self.thread._signal_result.connect(self.signal_delete_service)
            self.thread.start()

    
    def signal_add_service(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            self.dialog.progress.setValue(0)
            self.dialog.list.clear()
            self.dialog.service.setText("")
            self.load_service_all()

    def signal_update_service(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            self.dialog.progress.setValue(0)
            self.dialog.list.clear()
            self.dialog.service.setText("")
            self.load_service_all()

    def signal_delete_service(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            self.dialog.progress.setValue(0)
            self.dialog.list.clear()
            self.dialog.service.setText("")
            self.load_service_all()
    
    def load_service_all(self):
        self.thread = ThreadLoadServices()
        self.thread._signal.connect(self.signal_load_service)
        self.thread._signal_list.connect(self.signal_load_service)
        self.thread._signal_result.connect(self.signal_load_service)
        self.thread.start()

    def signal_load_service(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(0)
        else:
            listWidgetItem = QListWidgetItem(str(progress))
            self.dialog.list.addItem(listWidgetItem)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "You want to exit?"
        dialog = CustomDialog(message)
        if dialog.exec():
            self.close()
        else:
            a0.ignore()

    def load_workers(self):
        
        self.load_services_combo()
        self.table_workers.setRowCount(0)

        self.thread = ThreadLoadWorkers()
        self.thread._signal.connect(self.signal_load_workers)
        self.thread._signal_list.connect(self.signal_load_workers)
        self.thread._signal_result.connect(self.signal_load_workers)
        self.thread.start()
    
    def signal_load_workers(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        elif type(progress) == bool:
            self.progress.setValue(0)
        else:
            row = self.table_workers.rowCount()
            self.table_workers.insertRow(row)
            self.table_workers.setItem(row, 0, QTableWidgetItem(str(progress[0])))
            self.table_workers.setItem(row, 1, QTableWidgetItem(str(progress[1])))
            self.table_workers.setItem(row, 2, QTableWidgetItem(str(progress[2])))
            self.table_workers.setItem(row, 3, QTableWidgetItem(str(progress[3])))

            self.table_workers.item(row, 0).setBackground(QColor(220,255,220))
            self.table_workers.item(row, 1).setBackground(QColor(220,255,220))
            self.table_workers.item(row, 2).setBackground(QColor(220,255,220))
            self.table_workers.item(row, 3).setBackground(QColor(220,255,220))

    def flt(self, filter_text):
        for i in range(self.table_workers.rowCount()):
            for j in range(self.table_workers.columnCount()):
                item = self.table_workers.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.table_workers.setRowHidden(i, match)
                if not match:
                    break


    def filter_workers(self, text):
        self.flt(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.enable_hi_dpi()
    qdarktheme.setup_theme("light")
    app.setWindowIcon(QIcon("./images/icons/epsp.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())