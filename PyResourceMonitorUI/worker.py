from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    # recherche
    data_updated = pyqtSignal(dict, dict, dict, dict, float, float, float, float)

    def __init__(self, collector):
        # recherche
        super().__init__()
        self.collector = collector
        self.running = True

    def run(self):
        while self.running:
            self.collector.fill_processes_dicts()
            cpu_dict = self.collector.cpu_process_dict
            ram_dict = self.collector.ram_process_dict
            storage_dict = self.collector.storage_process_dict
            network_dict = self.collector.network_process_dict

            total_cpu_percent = sum(proc['cpu_percent'] for proc in cpu_dict.values())
            total_ram_percent = sum(proc['memory_percent'] for proc in ram_dict.values())
            total_storage_writting = sum(proc['write_bytes'] for proc in storage_dict.values())
            total_storage_reading = sum(proc['read_bytes'] for proc in storage_dict.values())

            # recherche
            self.data_updated.emit(cpu_dict, ram_dict, storage_dict, network_dict, total_cpu_percent, total_ram_percent, total_storage_writting, total_storage_reading)
            # recherche
            self.msleep(1000)

    def stop(self):
        self.running = False
        self.wait()
