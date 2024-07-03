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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(796, 590)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(110, 80, 401, 141))
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
        self.menuDatei.addAction(self.actionOpen)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionSQL_Eingabe)
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
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"\u00d6ffen", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionBalken.setText(QCoreApplication.translate("MainWindow", u"Balken", None))
        self.actionTortendiagramm.setText(QCoreApplication.translate("MainWindow", u"Tortendiagramm", None))
        self.actionStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.actionSQL_Eingabe.setText(QCoreApplication.translate("MainWindow", u"SQL-Eingabe", None))
        self.action_ber.setText(QCoreApplication.translate("MainWindow", u"\u00dcber", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuHilfe.setTitle(QCoreApplication.translate("MainWindow", u"Hilfe", None))
    # retranslateUi

