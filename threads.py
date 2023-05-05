import time
from calendar import monthrange
from daatabase_ops import *

import PyQt5
from PyQt5.QtCore import QThread, pyqtSignal

class ThreadLoadServices(QThread):
    _signal = pyqtSignal(int)
    _signal_list = pyqtSignal(str)
    _signal_result = pyqtSignal(bool)

    def __init__(self):
        super(ThreadLoadServices, self).__init__()

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        services = load_services()
        for i in range(len(services)):
            self._signal.emit(i)
            ser = services[i]
            self._signal_list.emit(ser[1])

        self._signal_result.emit(True)

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



class ThreadUpdateService(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, service_name, new_service_name):
        super(ThreadUpdateService, self).__init__()
        self.service_name = service_name
        self.new_service_name = new_service_name

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        id = get_service_id_from_name(self.service_name)
        id = id[0]
        update_service(id[0], self.new_service_name)

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)



