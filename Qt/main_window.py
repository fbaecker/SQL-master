# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(796, 590)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionBalken = QAction(MainWindow)
        self.actionBalken.setObjectName(u"actionBalken")
        self.actionTortendiagramm = QAction(MainWindow)
        self.actionTortendiagramm.setObjectName(u"actionTortendiagramm")
        self.actionStart = QAction(MainWindow)
        self.actionStart.setObjectName(u"actionStart")
        self.actionSQL_Eingabe = QAction(MainWindow)
        self.actionSQL_Eingabe.setObjectName(u"actionSQL_Eingabe")
        self.action_ber = QAction(MainWindow)
        self.action_ber.setObjectName(u"action_ber")
        self.actionSQL_History = QAction(MainWindow)
        self.actionSQL_History.setObjectName(u"actionSQL_History")
        self.actionOpen_Excel_Datei = QAction(MainWindow)
        self.actionOpen_Excel_Datei.setObjectName(u"actionOpen_Excel_Datei")
        self.actionOpen_Excel = QAction(MainWindow)
        self.actionOpen_Excel.setObjectName(u"actionOpen_Excel")
        self.actionOpen_History = QAction(MainWindow)
        self.actionOpen_History.setObjectName(u"actionOpen_History")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.checkBox_HV9 = QCheckBox(self.centralwidget)
        self.checkBox_HV9.setObjectName(u"checkBox_HV9")
        self.checkBox_HV9.setGeometry(QRect(70, 70, 75, 20))
        self.checkBox_HV8 = QCheckBox(self.centralwidget)
        self.checkBox_HV8.setObjectName(u"checkBox_HV8")
        self.checkBox_HV8.setGeometry(QRect(70, 100, 75, 20))
        self.checkBox_HV7 = QCheckBox(self.centralwidget)
        self.checkBox_HV7.setObjectName(u"checkBox_HV7")
        self.checkBox_HV7.setGeometry(QRect(70, 130, 75, 20))
        self.checkBox_NONHV = QCheckBox(self.centralwidget)
        self.checkBox_NONHV.setObjectName(u"checkBox_NONHV")
        self.checkBox_NONHV.setGeometry(QRect(70, 160, 75, 20))
        self.checkBox_Test = QCheckBox(self.centralwidget)
        self.checkBox_Test.setObjectName(u"checkBox_Test")
        self.checkBox_Test.setGeometry(QRect(70, 210, 75, 20))
        self.checkBox_PROD = QCheckBox(self.centralwidget)
        self.checkBox_PROD.setObjectName(u"checkBox_PROD")
        self.checkBox_PROD.setGeometry(QRect(70, 240, 75, 20))
        self.checkBox_Einstellung = QCheckBox(self.centralwidget)
        self.checkBox_Einstellung.setObjectName(u"checkBox_Einstellung")
        self.checkBox_Einstellung.setEnabled(True)
        self.checkBox_Einstellung.setGeometry(QRect(10, 390, 161, 20))
        self.checkBox_Einstellung.setChecked(False)
        self.checkBox_default_instanz = QCheckBox(self.centralwidget)
        self.checkBox_default_instanz.setObjectName(u"checkBox_default_instanz")
        self.checkBox_default_instanz.setGeometry(QRect(610, 60, 111, 20))
        self.lineEdit_default_instanz = QLineEdit(self.centralwidget)
        self.lineEdit_default_instanz.setObjectName(u"lineEdit_default_instanz")
        self.lineEdit_default_instanz.setGeometry(QRect(550, 60, 31, 21))
        self.lineEdit_default_instanz.setMaxLength(3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 796, 22))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuHilfe = QMenu(self.menubar)
        self.menuHilfe.setObjectName(u"menuHilfe")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuHilfe.menuAction())
        self.menuDatei.addAction(self.actionOpen_Excel)
        self.menuDatei.addAction(self.actionOpen_History)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionSQL_Eingabe)
        self.menuDatei.addAction(self.actionSQL_History)
        self.menuDatei.addAction(self.actionStart)
        self.menuDatei.addSeparator()
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionExit)
        self.menuHilfe.addSeparator()
        self.menuHilfe.addAction(self.action_ber)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionBalken.setText(QCoreApplication.translate("MainWindow", u"Balken", None))
        self.actionTortendiagramm.setText(QCoreApplication.translate("MainWindow", u"Tortendiagramm", None))
        self.actionStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.actionSQL_Eingabe.setText(QCoreApplication.translate("MainWindow", u"SQL-Eingabe", None))
        self.action_ber.setText(QCoreApplication.translate("MainWindow", u"\u00dcber", None))
        self.actionSQL_History.setText(QCoreApplication.translate("MainWindow", u"SQL-History", None))
        self.actionOpen_Excel_Datei.setText(QCoreApplication.translate("MainWindow", u"Open Excel-Datei", None))
        self.actionOpen_Excel.setText(QCoreApplication.translate("MainWindow", u"Open Excel-Datei", None))
        self.actionOpen_History.setText(QCoreApplication.translate("MainWindow", u"Open History-Json", None))
        self.checkBox_HV9.setText(QCoreApplication.translate("MainWindow", u"HV9", None))
        self.checkBox_HV8.setText(QCoreApplication.translate("MainWindow", u"HV8", None))
        self.checkBox_HV7.setText(QCoreApplication.translate("MainWindow", u"HV7", None))
        self.checkBox_NONHV.setText(QCoreApplication.translate("MainWindow", u"NON-HV", None))
        self.checkBox_Test.setText(QCoreApplication.translate("MainWindow", u"TEST", None))
        self.checkBox_PROD.setText(QCoreApplication.translate("MainWindow", u"PROD", None))
        self.checkBox_Einstellung.setText(QCoreApplication.translate("MainWindow", u"Einstellung beibehalten", None))
        self.checkBox_default_instanz.setText(QCoreApplication.translate("MainWindow", u"Default Instanz", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuHilfe.setTitle(QCoreApplication.translate("MainWindow", u"Hilfe", None))
    # retranslateUi

