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



class ThreadDeleteService(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, service_name):
        super(ThreadDeleteService, self).__init__()
        self.service_name = service_name

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        id = get_service_id_from_name(self.service_name)
        id = id[0]
        delete_service(id[0])

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)


class ThreadLoadWorkers(QThread):
    _signal = pyqtSignal(int)
    _signal_list = pyqtSignal(list)
    _signal_result = pyqtSignal(bool)

    def __init__(self):
        super(ThreadLoadWorkers, self).__init__()

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        workers = load_workers()
        for i in range(len(workers)):
            self._signal.emit(i)
            time.sleep(0.005)
            work = workers[i]
            service_name = get_service_name_from_id(int(work[3]))
            service_name = service_name[0]
            work_list = list(work)
            work_list[3] = service_name[0]
            self._signal_list.emit(work_list)

        self._signal_result.emit(True)



class ThreadAddWorker(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, first_name, last_name, service_name):
        super(ThreadAddWorker, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.service_name = service_name

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)            
            time.sleep(0.005)

        id = get_service_id_from_name(self.service_name)
        id = id[0]
        create_worker(self.first_name, self.last_name, id[0])

        for i in range(30, 99):
            self._signal.emit(i)            
            time.sleep(0.005)

        self._signal_result.emit(True)



class ThreadUpdateWorker(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, id, first_name, last_name, service_name):
        super(ThreadUpdateWorker, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.service_name = service_name

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)
            time.sleep(0.005)

        id = get_service_id_from_name(self.service_name)
        id = id[0]
        update_worker(int(self.id), str(self.first_name), str(self.last_name), int(id[0]))

        for i in range(30, 99):
            self._signal.emit(i)
            time.sleep(0.005)

        self._signal_result.emit(True)



class ThreadDeleteWorker(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, id):
        super(ThreadDeleteWorker, self).__init__()
        self.id = id

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)
            time.sleep(0.005)

        
        delete_worker(int(self.id))

        for i in range(30, 99):
            self._signal.emit(i)
            time.sleep(0.005)

        self._signal_result.emit(True)

class ThreadChoseYear(QThread):
    _signal_list = pyqtSignal(list)
    _signal_result = pyqtSignal(bool)

    def __init__(self, worker_id):
        super(ThreadChoseYear, self).__init__()
        self.worker_id = worker_id

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):

        years = get_garde_years_for_worker(int(self.worker_id))

        self._signal_list.emit(years)

        self._signal_result.emit(True)




