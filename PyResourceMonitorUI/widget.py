import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QGroupBox, QVBoxLayout, QSpinBox, QMessageBox
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QThread, pyqtSignal
import psutil

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from processesCollector import ProcessesCollector
from worker import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        uic.loadUi('form.ui', self)

        self.cpu_usage_history = []
        self.ram_usage_history = []
        self.storage_writting_history = []
        self.storage_reading_history = []
        self.network_receiving_history = []
        self.network_sending_history = []

        self.max_storage_writting = 0.0
        self.max_storage_reading = 0.0
        self.max_network_receiving = 0.0
        self.max_network_sending = 0.0

        self.plots_size = 20

        # Access the table widgets
        self.cpuTableWidget = self.findChild(QTableWidget, 'cpu_table')
        self.ramTableWidget = self.findChild(QTableWidget, 'ram_table')
        self.storageTableWidget = self.findChild(QTableWidget, 'storage_table')
        self.networkTableWidget = self.findChild(QTableWidget, 'network_table')

        self.cpuGroupBoxWidget = self.findChild(QGroupBox, 'cpu_groupbox')
        self.ramGroupBoxWidget = self.findChild(QGroupBox, 'ram_groupbox')
        self.storageGroupBoxWidget = self.findChild(QGroupBox, 'storage_groupbox')
        self.networkGroupBoxWidget = self.findChild(QGroupBox, 'network_groupbox')

        self.terminateButton = self.findChild(QPushButton, 'terminate')
        self.terminateButton.clicked.connect(self.terminate_process)
        self.pidSpinbox = self.findChild(QSpinBox, 'pid_spinbox')

        self.collector = ProcessesCollector()
        self.populate_tables()

        self.plot_cpu()
        self.plot_ram()
        self.plot_storage()
        self.plot_network()

        # Create and start the worker thread
        self.worker = Worker(self.collector)
        self.worker.data_updated.connect(self.update_tables_and_plot)
        # recherche
        self.worker.start()

    def terminate_process(self):
        pid = self.pidSpinbox.value()
        print(f"Tentative de terminaison du processus avec le PID {pid}")
        try:
            proc = psutil.Process(pid)
            proc_name = proc.name()

            # Trouver tous les processus avec le même nom
            processes = [p for p in psutil.process_iter(['pid', 'name']) if p.info['name'] == proc_name]

            for p in processes:
                try:
                    print(f"Tentative de terminaison du processus: {p.info['name']} (PID: {p.info['pid']})")
                    p.terminate()
                    try:
                        p.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        p.kill()
                        p.wait(timeout=3)

                    if not p.is_running():
                        print(f"Processus {p.info['pid']} terminé avec succès.")
                    else:
                        print(f"Le processus {p.info['pid']} n'a pas pu être terminé.")
                except psutil.NoSuchProcess:
                    print(f"Aucun processus trouvé avec le PID {p.info['pid']}.")
                except psutil.AccessDenied:
                    print(f"Accès refusé pour terminer le processus avec le PID {p.info['pid']}.")

            QMessageBox.information(self, 'Succès', f"Tous les processus liés à {proc_name} ont été terminés.")
        except psutil.NoSuchProcess:
            print(f"Aucun processus trouvé avec le PID {pid}.")
            QMessageBox.warning(self, 'Erreur', f"Aucun processus trouvé avec le PID {pid}.")
        except psutil.AccessDenied:
            print(f"Accès refusé pour terminer le processus avec le PID {pid}.")
            QMessageBox.warning(self, 'Erreur', f"Accès refusé pour terminer le processus avec le PID {pid}.")




    def update_tables_and_plot(self, cpu_dict, ram_dict, storage_dict, network_dict, total_cpu_percent, total_ram_percent, total_storage_writting, total_storage_reading, total_network_receiving, total_network_sending):
        self.populate_cpu_table(cpu_dict)
        self.populate_ram_table(ram_dict)
        self.populate_storage_table(storage_dict)
        self.populate_network_table(network_dict)
        if total_cpu_percent > 100.0:
            total_cpu_percent = 100.0
        self.cpu_usage_history.append(total_cpu_percent)
        if total_ram_percent > 100.0:
            total_ram_percent = 100.0
        self.ram_usage_history.append(total_ram_percent)
        self.storage_writting_history.append(total_storage_writting)
        self.storage_reading_history.append(total_storage_reading)
        self.network_receiving_history.append(total_network_receiving)
        self.network_sending_history.append(total_network_sending)

        if  len(self.cpu_usage_history) > 0:
            if self.storage_writting_history[-1] > self.max_storage_writting:
                self.max_storage_writting = self.storage_writting_history[-1]
            if self.storage_reading_history[-1] > self.max_storage_reading:
                self.max_storage_reading = self.storage_reading_history[-1]
            if self.network_receiving_history[-1] > self.max_network_receiving:
                self.max_network_receiving = self.network_receiving_history[-1]
            if self.network_sending_history[-1] > self.max_network_sending:
                self.max_network_sending = self.network_sending_history[-1]
        if len(self.cpu_usage_history) > self.plots_size:
            self.cpu_usage_history.pop(0)
        #if len(self.ram_usage_history) > self.plots_size:
            self.ram_usage_history.pop(0)
        #if len(self.storage_writting_history) > self.plots_size:
            self.storage_writting_history.pop(0)
        #if len(self.storage_reading_history) > self.plots_size:
            self.storage_reading_history.pop(0)
        #if len(self.network_receiving_history) > self.plots_size:
            self.network_receiving_history.pop(0)
        #if len(self.network_sending_history) > self.plots_size:
            self.network_sending_history.pop(0)

        self.plot_cpu()
        self.plot_ram()
        self.plot_storage()
        self.plot_network()

    def refresh_tables(self):
        self.populate_tables()

    def populate_tables(self):

        self.collector.fill_processes_dicts()
        self.populate_cpu_table()
        self.populate_ram_table()
        self.populate_storage_table()
        self.populate_network_table()

    def populate_cpu_table(self, cpu_dict=None):
        if cpu_dict is None:
            cpu_dict = self.collector.cpu_process_dict

        self.cpuTableWidget.setColumnCount(8)
        self.cpuTableWidget.setRowCount(len(cpu_dict))
        self.cpuTableWidget.setHorizontalHeaderLabels(['PID', 'Name', 'User', 'Create Time', 'CPU Times', 'Status', 'CPU Percent', 'Num Threads'])

        total_cpu_percent = 0.0

        for row, pid in enumerate(cpu_dict):
            self.cpuTableWidget.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.cpuTableWidget.setItem(row, 1, QTableWidgetItem(cpu_dict[pid]['name']))
            self.cpuTableWidget.setItem(row, 2, QTableWidgetItem(cpu_dict[pid]['user']))
            self.cpuTableWidget.setItem(row, 3, QTableWidgetItem(str(cpu_dict[pid]['create_time'])))
            self.cpuTableWidget.setItem(row, 4, QTableWidgetItem(str(cpu_dict[pid]['cpu_times'])))
            self.cpuTableWidget.setItem(row, 5, QTableWidgetItem(cpu_dict[pid]['status']))

            cpu_percent_formatted = f"{cpu_dict[pid]['cpu_percent']:.4f}"
            self.cpuTableWidget.setItem(row, 6, QTableWidgetItem(cpu_percent_formatted))

            self.cpuTableWidget.setItem(row, 7, QTableWidgetItem(str(cpu_dict[pid]['num_threads'])))


    def populate_ram_table(self, ram_dict=None):
        if ram_dict is None:
            ram_dict = self.collector.ram_process_dict

        self.ramTableWidget.setColumnCount(8)
        self.ramTableWidget.setRowCount(len(ram_dict))
        self.ramTableWidget.setHorizontalHeaderLabels(['PID', 'Name', 'User', 'Create Time', 'RSS', 'VMS', 'Shared', 'Memory Percent'])

        total_ram_percent = 0.0

        for row, pid in enumerate(ram_dict):
            self.ramTableWidget.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.ramTableWidget.setItem(row, 1, QTableWidgetItem(ram_dict[pid]['name']))
            self.ramTableWidget.setItem(row, 2, QTableWidgetItem(ram_dict[pid]['user']))
            self.ramTableWidget.setItem(row, 3, QTableWidgetItem(str(ram_dict[pid]['create_time'])))
            self.ramTableWidget.setItem(row, 4, QTableWidgetItem(str(ram_dict[pid]['rss'])))
            self.ramTableWidget.setItem(row, 5, QTableWidgetItem(str(ram_dict[pid]['vms'])))
            self.ramTableWidget.setItem(row, 6, QTableWidgetItem(str(ram_dict[pid]['shared'])))

            memory_percent_formatted = f"{ram_dict[pid]['memory_percent']:.4f}"
            self.ramTableWidget.setItem(row, 7, QTableWidgetItem(memory_percent_formatted))


    def populate_storage_table(self, storage_dict=None):
        if storage_dict is None:
            storage_dict = self.collector.storage_process_dict

        total_writting = 0.0
        total_reading = 0.0

        self.storageTableWidget.setColumnCount(9)
        self.storageTableWidget.setRowCount(len(storage_dict))
        self.storageTableWidget.setHorizontalHeaderLabels(['PID', 'Name', 'User', 'Create Time', 'Files', 'Read Count', 'Write Count', 'Read Bytes', 'Write Bytes'])

        for row, pid in enumerate(storage_dict):
            self.storageTableWidget.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.storageTableWidget.setItem(row, 1, QTableWidgetItem(storage_dict[pid]['name']))
            self.storageTableWidget.setItem(row, 2, QTableWidgetItem(storage_dict[pid]['user']))
            self.storageTableWidget.setItem(row, 3, QTableWidgetItem(str(storage_dict[pid]['create_time'])))
            self.storageTableWidget.setItem(row, 4, QTableWidgetItem(str(storage_dict[pid]['files'])))
            self.storageTableWidget.setItem(row, 5, QTableWidgetItem(str(storage_dict[pid]['read_count'])))
            self.storageTableWidget.setItem(row, 6, QTableWidgetItem(str(storage_dict[pid]['write_count'])))
            self.storageTableWidget.setItem(row, 7, QTableWidgetItem(str(storage_dict[pid]['read_bytes'])))
            self.storageTableWidget.setItem(row, 8, QTableWidgetItem(str(storage_dict[pid]['write_bytes'])))



    def populate_network_table(self, network_dict=None):
        if network_dict is None:
            network_dict = self.collector.network_process_dict

        self.networkTableWidget.setColumnCount(7)
        self.networkTableWidget.setRowCount(len(network_dict))
        self.networkTableWidget.setHorizontalHeaderLabels(['PID', 'Name', 'User', 'Create Time', 'Laddr', 'Raddr', 'Status'])

        for row, pid in enumerate(network_dict):
            self.networkTableWidget.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.networkTableWidget.setItem(row, 1, QTableWidgetItem(network_dict[pid]['name']))
            self.networkTableWidget.setItem(row, 2, QTableWidgetItem(network_dict[pid]['user']))
            self.networkTableWidget.setItem(row, 3, QTableWidgetItem(str(network_dict[pid]['create_time'])))
            self.networkTableWidget.setItem(row, 4, QTableWidgetItem(str(network_dict[pid]['laddr'])))
            self.networkTableWidget.setItem(row, 5, QTableWidgetItem(str(network_dict[pid]['raddr'])))
            self.networkTableWidget.setItem(row, 6, QTableWidgetItem(network_dict[pid]['status']))


    def plot_cpu(self):
        # Create the line series data from cpu_usage_history
        series = QLineSeries()
        for i, value in enumerate(self.cpu_usage_history):
            series.append(i, value)

        # Create the chart
        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle("CPU Usage History")
        chart.legend().hide()
        axisY = chart.axisY()
        axisY.setRange(0, 100)

        # Create the chart view
        chart_view = QChartView(chart)

        # Check if the cpu_groupbox already has a layout
        if self.cpuGroupBoxWidget.layout() is not None:
            # Remove the old widgets from the layout
            old_layout = self.cpuGroupBoxWidget.layout()
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
            # Add the new chart view to the existing layout
            old_layout.addWidget(chart_view)
        else:
            # Create and set the new layout if there is none
            layout = QVBoxLayout(self.cpuGroupBoxWidget)
            layout.addWidget(chart_view)
            self.cpuGroupBoxWidget.setLayout(layout)

    def plot_ram(self):
        # Create the line series data from ram_usage_history
        series = QLineSeries()
        for i, value in enumerate(self.ram_usage_history):
            series.append(i, value)

        # Create the chart
        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle("RAM Usage History")
        chart.legend().hide()
        axisY = chart.axisY()
        axisY.setRange(0, 100)

        # Create the chart view
        chart_view = QChartView(chart)

        # Check if the ram_groupbox already has a layout
        if self.ramGroupBoxWidget.layout() is not None:
            # Remove the old widgets from the layout
            old_layout = self.ramGroupBoxWidget.layout()
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
            # Add the new chart view to the existing layout
            old_layout.addWidget(chart_view)
        else:
            # Create and set the new layout if there is none
            layout = QVBoxLayout(self.ramGroupBoxWidget)
            layout.addWidget(chart_view)
            self.ramGroupBoxWidget.setLayout(layout)

    def plot_storage(self):
        max_height = 0.0
        if self.max_storage_reading > self.max_storage_writting:
            max_height = self.max_storage_reading
        else:
            max_height = self.max_storage_writting

        writting_series = QLineSeries()
        for i, value in enumerate(self.storage_writting_history):
            writting_series.append(i, value)

        reading_series = QLineSeries()
        for i, value in enumerate(self.storage_reading_history):
            reading_series.append(i, value)


        # Create the chart
        chart = QChart()
        chart.addSeries(writting_series)
        chart.addSeries(reading_series)
        chart.createDefaultAxes()
        chart.setTitle("Storage reading/writting History")
        chart.legend().hide()
        axisY = chart.axisY()
        axisY.setRange(0, max_height)

        # Create the chart view
        chart_view = QChartView(chart)

        # Check if the ram_groupbox already has a layout
        if self.storageGroupBoxWidget.layout() is not None:
            # Remove the old widgets from the layout
            old_layout = self.storageGroupBoxWidget.layout()
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
            # Add the new chart view to the existing layout
            old_layout.addWidget(chart_view)
        else:
            # Create and set the new layout if there is none
            layout = QVBoxLayout(self.storageGroupBoxWidget)
            layout.addWidget(chart_view)
            self.storageGroupBoxWidget.setLayout(layout)


    def plot_network(self):
        # Create the line series data from ram_usage_history
        max_height = 0.0
        if self.max_network_receiving > self.max_network_sending:
            max_height = self.max_network_receiving
        else:
            max_height = self.max_network_sending

        receive_series = QLineSeries()
        for i, value in enumerate(self.network_receiving_history):
            receive_series.append(i, value)

        send_series = QLineSeries()
        for i, value in enumerate(self.network_sending_history):
            send_series.append(i, value)


        # Create the chart
        chart = QChart()
        chart.addSeries(receive_series)
        chart.addSeries(send_series)
        chart.createDefaultAxes()
        chart.setTitle("Network receiving/sending History")
        chart.legend().hide()
        axisY = chart.axisY()
        axisY.setRange(0, max_height)

        # Create the chart view
        chart_view = QChartView(chart)

        # Check if the ram_groupbox already has a layout
        if self.networkGroupBoxWidget.layout() is not None:
            # Remove the old widgets from the layout
            old_layout = self.networkGroupBoxWidget.layout()
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
            # Add the new chart view to the existing layout
            old_layout.addWidget(chart_view)
        else:
            # Create and set the new layout if there is none
            layout = QVBoxLayout(self.networkGroupBoxWidget)
            layout.addWidget(chart_view)
            self.networkGroupBoxWidget.setLayout(layout)



    def closeEvent(self, event):
        self.worker.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
