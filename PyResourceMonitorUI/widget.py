import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QGroupBox, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QThread, pyqtSignal

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

        # Access the table widgets
        self.cpuTableWidget = self.findChild(QTableWidget, 'cpu_table')
        self.ramTableWidget = self.findChild(QTableWidget, 'ram_table')
        self.storageTableWidget = self.findChild(QTableWidget, 'storage_table')
        self.networkTableWidget = self.findChild(QTableWidget, 'network_table')

        self.cpuGroupBoxWidget = self.findChild(QGroupBox, 'cpu_groupbox')
        self.ramGroupBoxWidget = self.findChild(QGroupBox, 'ram_groupbox')
        self.storageGroupBoxWidget = self.findChild(QGroupBox, 'storage_groupbox')
        self.networkGroupBoxWidget = self.findChild(QGroupBox, 'network_groupbox')

        self.refreshButton = self.findChild(QPushButton, 'refresh_button')
        self.refreshButton.clicked.connect(self.refresh_tables)

        self.collector = ProcessesCollector()
        self.populate_tables()

        self.plot_cpu()
        self.plot_ram()

        # Create and start the worker thread
        self.worker = Worker(self.collector)
        self.worker.data_updated.connect(self.update_tables_and_plot)
        self.worker.start()

    def update_tables_and_plot(self, cpu_dict, ram_dict, storage_dict, network_dict, total_cpu_percent, total_ram_percent):
        self.populate_cpu_table(cpu_dict)
        self.populate_ram_table(ram_dict)
        self.populate_storage_table(storage_dict)
        self.populate_network_table(network_dict)

        self.cpu_usage_history.append(total_cpu_percent)
        self.ram_usage_history.append(total_ram_percent)

        if len(self.cpu_usage_history) > 10:
            self.cpu_usage_history.pop(0)
        if len(self.ram_usage_history) > 10:
            self.ram_usage_history.pop(0)

        self.plot_cpu()
        self.plot_ram()

    def refresh_tables(self):
        self.populate_tables()

    def populate_tables(self):
        self.collector.fill_processes_dicts()  # Collect the processes information
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

        total_cpu_percent = 0.0  # Pour calculer la somme des cpu_percent

        for row, pid in enumerate(cpu_dict):
            self.cpuTableWidget.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.cpuTableWidget.setItem(row, 1, QTableWidgetItem(cpu_dict[pid]['name']))
            self.cpuTableWidget.setItem(row, 2, QTableWidgetItem(cpu_dict[pid]['user']))
            self.cpuTableWidget.setItem(row, 3, QTableWidgetItem(str(cpu_dict[pid]['create_time'])))
            self.cpuTableWidget.setItem(row, 4, QTableWidgetItem(str(cpu_dict[pid]['cpu_times'])))
            self.cpuTableWidget.setItem(row, 5, QTableWidgetItem(cpu_dict[pid]['status']))

            # Format the CPU percent with more precision
            cpu_percent_formatted = f"{cpu_dict[pid]['cpu_percent']:.4f}"
            self.cpuTableWidget.setItem(row, 6, QTableWidgetItem(cpu_percent_formatted))

            self.cpuTableWidget.setItem(row, 7, QTableWidgetItem(str(cpu_dict[pid]['num_threads'])))

            total_cpu_percent += cpu_dict[pid]['cpu_percent']  # Ajouter le cpu_percent au total

        self.cpu_usage_history.append(total_cpu_percent)  # Ajouter la somme totale à l'historique

        # Ensure the history list does not exceed 10 elements
        if len(self.cpu_usage_history) > 10:
            self.cpu_usage_history.pop(0)

        print(self.cpu_usage_history)

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

            # Format the memory percent with more precision
            memory_percent_formatted = f"{ram_dict[pid]['memory_percent']:.4f}"
            self.ramTableWidget.setItem(row, 7, QTableWidgetItem(memory_percent_formatted))

            total_ram_percent += ram_dict[pid]['memory_percent']

        self.ram_usage_history.append(total_ram_percent)

        if len(self.ram_usage_history) > 10:
            self.ram_usage_history.pop(0)

        print(self.ram_usage_history)

    def populate_storage_table(self, storage_dict=None):
        if storage_dict is None:
            storage_dict = self.collector.storage_process_dict

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

        self.networkTableWidget.setColumnCount(9)
        self.networkTableWidget.setRowCount(len(network_dict))
        self.networkTableWidget.setHorizontalHeaderLabels(['PID', 'Name', 'User', 'Create Time', 'Laddr', 'Raddr', 'Status', 'Bytes Sent', 'Bytes Recv'])

        for row, pid in enumerate(network_dict):
            self.networkTableWidget.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.networkTableWidget.setItem(row, 1, QTableWidgetItem(network_dict[pid]['name']))
            self.networkTableWidget.setItem(row, 2, QTableWidgetItem(network_dict[pid]['user']))
            self.networkTableWidget.setItem(row, 3, QTableWidgetItem(str(network_dict[pid]['create_time'])))
            self.networkTableWidget.setItem(row, 4, QTableWidgetItem(str(network_dict[pid]['laddr'])))
            self.networkTableWidget.setItem(row, 5, QTableWidgetItem(str(network_dict[pid]['raddr'])))
            self.networkTableWidget.setItem(row, 6, QTableWidgetItem(network_dict[pid]['status']))
            self.networkTableWidget.setItem(row, 7, QTableWidgetItem(str(network_dict[pid]['bytes_sent'])))
            self.networkTableWidget.setItem(row, 8, QTableWidgetItem(str(network_dict[pid]['bytes_recv'])))

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

    def closeEvent(self, event):
        self.worker.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
