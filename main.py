


import sys
import os
import platform

from PyQt5 import Qt, uic, QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QApplication, QMenu, QAction, QToolBar, QMessageBox
import qdarktheme
import qtawesome as qta
from dialogs import *


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

        self.detailsAction = QAction(self)
        self.detailsAction.setText("&Details")
        icon = qta.icon("mdi.account-details")
        self.detailsAction.setIcon(icon)
        newTip = "Details of selected worker"
        self.detailsAction.setStatusTip(newTip)
        self.detailsAction.setToolTip(newTip)

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

        

    def _createToolBars(self):
        # data toolbar
        operationToolBar = self.addToolBar("Operation")
        operationToolBar.addAction(self.adAction)
        operationToolBar.addAction(self.editAction)
        operationToolBar.addAction(self.deleteAction)
        operationToolBar.addAction(self.detailsAction)
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
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()
    def workerAddActionClicked_(self):
        self.dialog = Worker_dialog()
        self.dialog.setWindowTitle("add new worker")
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()
    def workerUpdateActionClicked_(self):
        self.dialog = Worker_dialog()
        self.dialog.setWindowTitle("update worker")
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.enable_hi_dpi()
    qdarktheme.setup_theme("light")
    app.setWindowIcon(QIcon("./images/icons/epsp.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())