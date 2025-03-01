# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'eingabe_window.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPlainTextEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form_eingabe(object):
    def setupUi(self, Form_eingabe):
        if not Form_eingabe.objectName():
            Form_eingabe.setObjectName(u"Form_eingabe")
        Form_eingabe.resize(656, 585)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form_eingabe.sizePolicy().hasHeightForWidth())
        Form_eingabe.setSizePolicy(sizePolicy)
        Form_eingabe.setMinimumSize(QSize(100, 100))
        self.pushButton_sql_start = QPushButton(Form_eingabe)
        self.pushButton_sql_start.setObjectName(u"pushButton_sql_start")
        self.pushButton_sql_start.setGeometry(QRect(240, 540, 75, 24))
        self.pushButton_sql_start.setAutoDefault(True)
        self.label = QLabel(Form_eingabe)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 49, 16))
        self.label_id = QLabel(Form_eingabe)
        self.label_id.setObjectName(u"label_id")
        self.label_id.setGeometry(QRect(40, 10, 49, 16))
        self.plainTextEdit_statement = QPlainTextEdit(Form_eingabe)
        self.plainTextEdit_statement.setObjectName(u"plainTextEdit_statement")
        self.plainTextEdit_statement.setGeometry(QRect(10, 40, 571, 221))
        self.plainTextEdit_commend = QPlainTextEdit(Form_eingabe)
        self.plainTextEdit_commend.setObjectName(u"plainTextEdit_commend")
        self.plainTextEdit_commend.setGeometry(QRect(10, 280, 571, 201))
        self.pushButton_history_lesen = QPushButton(Form_eingabe)
        self.pushButton_history_lesen.setObjectName(u"pushButton_history_lesen")
        self.pushButton_history_lesen.setGeometry(QRect(20, 540, 75, 24))
        self.pushButton_history_schreiben = QPushButton(Form_eingabe)
        self.pushButton_history_schreiben.setObjectName(u"pushButton_history_schreiben")
        self.pushButton_history_schreiben.setGeometry(QRect(120, 540, 101, 24))

        self.retranslateUi(Form_eingabe)

        QMetaObject.connectSlotsByName(Form_eingabe)
    # setupUi

    def retranslateUi(self, Form_eingabe):
        Form_eingabe.setWindowTitle(QCoreApplication.translate("Form_eingabe", u"Form", None))
        self.pushButton_sql_start.setText(QCoreApplication.translate("Form_eingabe", u"SQL-Start", None))
        self.label.setText(QCoreApplication.translate("Form_eingabe", u"ID", None))
        self.label_id.setText(QCoreApplication.translate("Form_eingabe", u"TextLabel", None))
        self.pushButton_history_lesen.setText(QCoreApplication.translate("Form_eingabe", u"History lesen", None))
        self.pushButton_history_schreiben.setText(QCoreApplication.translate("Form_eingabe", u"History schreiben", None))
    # retranslateUi

