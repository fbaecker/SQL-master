# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'history_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(656, 585)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(100, 100))
        self.pushButton_ok = QPushButton(Form)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setGeometry(QRect(290, 440, 75, 24))
        self.textEdit_SQL = QTextEdit(Form)
        self.textEdit_SQL.setObjectName(u"textEdit_SQL")
        self.textEdit_SQL.setGeometry(QRect(10, 430, 241, 41))
        self.tableWidget_History = QTableWidget(Form)
        if (self.tableWidget_History.columnCount() < 3):
            self.tableWidget_History.setColumnCount(3)
        self.tableWidget_History.setObjectName(u"tableWidget_History")
        self.tableWidget_History.setGeometry(QRect(10, 60, 561, 351))
        self.tableWidget_History.setColumnCount(3)
        self.tableWidget_History.horizontalHeader().setVisible(True)
        self.lineEdit_filter = QLineEdit(Form)
        self.lineEdit_filter.setObjectName(u"lineEdit_filter")
        self.lineEdit_filter.setGeometry(QRect(10, 30, 113, 21))
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 49, 16))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"SQL-Start", None))
        self.label.setText(QCoreApplication.translate("Form", u"Filter", None))
    # retranslateUi

