# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(803, 485)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(803, 485))
        MainWindow.setMaximumSize(QSize(803, 485))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 811, 491))
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.textBrowser = QTextBrowser(self.tab_1)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 60, 451, 361))
        self.textBrowser.setOpenExternalLinks(True)
        self.label_2 = QLabel(self.tab_1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(490, 20, 291, 171))
        self.label_2.setOpenExternalLinks(True)
        self.comboBox = QComboBox(self.tab_1)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(640, 210, 141, 21))
        self.comboBox.setEditable(False)
        self.pushButton_3 = QPushButton(self.tab_1)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(490, 390, 291, 31))
        self.pushButton_1 = QPushButton(self.tab_1)
        self.pushButton_1.setObjectName(u"pushButton_1")
        self.pushButton_1.setGeometry(QRect(490, 330, 291, 51))
        self.label = QLabel(self.tab_1)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(490, 210, 141, 21))
        self.lineEdit = QLineEdit(self.tab_1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(490, 290, 251, 20))
        self.lineEdit.setReadOnly(False)
        self.toolButton = QToolButton(self.tab_1)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(750, 290, 31, 21))
        self.label_3 = QLabel(self.tab_1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(490, 250, 141, 21))
        self.pushButton = QPushButton(self.tab_1)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(640, 250, 141, 23))
        self.label_4 = QLabel(self.tab_1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 20, 151, 31))
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(230, 120, 331, 141))
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 803, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TSB Tools v0.1", None))
        self.comboBox.setCurrentText("")
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u30b5\u30fc\u30d0\u30fc\u3092\u4f5c\u6210", None))
        self.pushButton_1.setText(QCoreApplication.translate("MainWindow", u"\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u30d0\u30fc\u30b8\u30e7\u30f3\u9078\u629e</p></body></html>", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\u30b2\u30fc\u30e0\u30c7\u30a3\u30ec\u30af\u30c8\u30ea</p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52d5\u691c\u51fa", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:600;\">\u66f4\u65b0\u5c65\u6b74</span></h2></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">\u672a\u5b9f\u88c5</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u30c4\u30fc\u30eb", None))
    # retranslateUi

