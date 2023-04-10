


import sys
import os
import platform

from PyQt5 import Qt, uic, QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QApplication, QMenu, QAction, QToolBar
import qdarktheme
import qtawesome as qta


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
        operationMenu = QMenu("&Operations", self)
        menuBar.addMenu(operationMenu)
        operationMenu.addAction(self.adAction)
        operationMenu.addAction(self.editAction)
        operationMenu.addAction(self.deleteAction)
        detailsMenu = QMenu("&Details", self)
        menuBar.addMenu(detailsMenu)
        # Creating menus using a title
        printMenu = menuBar.addMenu("&Print")
        helpMenu = menuBar.addMenu("&About")

    def _createActions(self):
        # File actions
        self.adAction = QAction(self)
        self.adAction.setText("&Add worker")
        newTip = "Create a new worker"
        self.adAction.setStatusTip(newTip)
        self.adAction.setToolTip(newTip)
        icon = qta.icon("fa.user-plus")
        self.adAction.setIcon(icon)

        self.editAction = QAction(self)
        self.editAction.setText("&Edit worker")
        icon = qta.icon("fa5s.user-edit")
        self.editAction.setIcon(icon)
        newTip = "Edit selected worker"
        self.editAction.setStatusTip(newTip)
        self.editAction.setToolTip(newTip)

        self.deleteAction = QAction(self)
        self.deleteAction.setText("&Delete worker")
        icon = qta.icon("fa.user-times")
        self.deleteAction.setIcon(icon)
        newTip = "Delete selected worker"
        self.deleteAction.setStatusTip(newTip)
        self.deleteAction.setToolTip(newTip)

    def _createToolBars(self):
        # data toolbar
        operationToolBar = self.addToolBar("Operation")
        operationToolBar.addAction(self.adAction)
        operationToolBar.addAction(self.editAction)
        operationToolBar.addAction(self.deleteAction)
        # Edit toolbar
        dataToolBar = QToolBar("Edit", self)
        self.addToolBar(dataToolBar)
    
    def _createStatusBar(self):
        self.statusbar = self.statusBar()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.enable_hi_dpi()
    qdarktheme.setup_theme("light")
    app.setWindowIcon(QIcon("./images/icons/epsp.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())