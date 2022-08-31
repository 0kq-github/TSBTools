# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tsbupdater.ui'
##
## Created by: Qt User Interface Compiler version 6.1.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(480, 280)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 0))
        Dialog.setMaximumSize(QSize(9999, 9999))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 441, 51))
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(270, 220, 191, 41))
        self.checkBox = QCheckBox(Dialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(270, 140, 191, 21))
        self.checkBox_2 = QCheckBox(Dialog)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(270, 180, 181, 21))
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(20, 101, 231, 161))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 80, 231, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u6e08\u307f\u306eTSB\u306e\u30d0\u30fc\u30b8\u30e7\u30f3: v0.0.0</p><p align=\"center\">Minecraft\u306e\u30d0\u30fc\u30b8\u30e7\u30f3: 0.00<br/></p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u30a2\u30c3\u30d7\u30c7\u30fc\u30c8", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"\u4e92\u63db\u6027\u306e\u306a\u3044\u30d0\u30fc\u30b8\u30e7\u30f3\u3092\u8868\u793a\u3059\u308b", None))
        self.checkBox_2.setText(QCoreApplication.translate("Dialog", u"\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u3092\u4f5c\u6210\u3059\u308b", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>\u30d0\u30fc\u30b8\u30e7\u30f3\u4e00\u89a7</p></body></html>", None))
    # retranslateUi

