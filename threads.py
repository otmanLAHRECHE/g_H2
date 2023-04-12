import time
from calendar import monthrange
from daatabase_ops import *

import PyQt5
from PyQt5.QtCore import QThread, pyqtSignal


class ThreadAddService(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, service_name):
        super(ThreadAddService, self).__init__()
        self.service_name = service_name

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        create_service(self.service_name)

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)