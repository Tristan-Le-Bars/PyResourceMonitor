# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGroupBox, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1920, 1080)
        self.refresh_button = QPushButton(Widget)
        self.refresh_button.setObjectName(u"refresh_button")
        self.refresh_button.setGeometry(QRect(20, 1020, 101, 41))
        self.cpu_table = QTableWidget(Widget)
        self.cpu_table.setObjectName(u"cpu_table")
        self.cpu_table.setGeometry(QRect(20, 40, 611, 451))
        self.ram_table = QTableWidget(Widget)
        self.ram_table.setObjectName(u"ram_table")
        self.ram_table.setGeometry(QRect(960, 40, 611, 451))
        self.storage_table = QTableWidget(Widget)
        self.storage_table.setObjectName(u"storage_table")
        self.storage_table.setGeometry(QRect(20, 540, 611, 461))
        self.network_table = QTableWidget(Widget)
        self.network_table.setObjectName(u"network_table")
        self.network_table.setGeometry(QRect(960, 540, 611, 461))
        self.graphicsView_2 = QGraphicsView(Widget)
        self.graphicsView_2.setObjectName(u"graphicsView_2")
        self.graphicsView_2.setGeometry(QRect(650, 540, 271, 461))
        self.graphicsView_3 = QGraphicsView(Widget)
        self.graphicsView_3.setObjectName(u"graphicsView_3")
        self.graphicsView_3.setGeometry(QRect(1590, 40, 291, 451))
        self.graphicsView_4 = QGraphicsView(Widget)
        self.graphicsView_4.setObjectName(u"graphicsView_4")
        self.graphicsView_4.setGeometry(QRect(1590, 540, 291, 461))
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(260, 10, 31, 20))
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(1240, 10, 31, 20))
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(260, 510, 41, 20))
        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(1250, 510, 51, 20))
        self.cpu_groupbox = QGroupBox(Widget)
        self.cpu_groupbox.setObjectName(u"cpu_groupbox")
        self.cpu_groupbox.setGeometry(QRect(650, 20, 271, 471))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.refresh_button.setText(QCoreApplication.translate("Widget", u"Refresh", None))
        self.label.setText(QCoreApplication.translate("Widget", u"CPU", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"RAM", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Storage", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Network", None))
        self.cpu_groupbox.setTitle(QCoreApplication.translate("Widget", u"GroupBox", None))
    # retranslateUi

