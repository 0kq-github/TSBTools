# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'server.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 277)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 111, 21))
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(140, 20, 301, 21))
        self.toolButton = QToolButton(Dialog)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(450, 20, 31, 20))
        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(140, 60, 101, 21))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 60, 111, 21))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(260, 60, 111, 21))
        self.spinBox = QSpinBox(Dialog)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(380, 60, 101, 21))
        self.spinBox.setMaximum(65535)
        self.spinBox.setValue(25565)
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 100, 111, 21))
        self.spinBox_2 = QSpinBox(Dialog)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setGeometry(QRect(380, 100, 101, 21))
        self.spinBox_2.setMaximum(64)
        self.spinBox_2.setValue(4)
        self.horizontalSlider = QSlider(Dialog)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(140, 100, 231, 22))
        self.horizontalSlider.setMaximum(64)
        self.horizontalSlider.setValue(4)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.checkBox = QCheckBox(Dialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(140, 230, 111, 21))
        self.checkBox.setChecked(False)
        self.checkBox.setAutoRepeat(False)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(380, 230, 101, 31))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(19, 132, 111, 21))
        self.horizontalSlider_2 = QSlider(Dialog)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setGeometry(QRect(140, 130, 231, 22))
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setValue(20)
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)
        self.spinBox_3 = QSpinBox(Dialog)
        self.spinBox_3.setObjectName(u"spinBox_3")
        self.spinBox_3.setGeometry(QRect(380, 130, 101, 21))
        self.spinBox_3.setMaximum(100)
        self.spinBox_3.setValue(20)
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 230, 111, 21))
        self.label_6.setOpenExternalLinks(True)
        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 170, 111, 21))
        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(140, 170, 341, 41))
        self.textEdit.setAcceptRichText(False)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u5148</p></body></html>", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">\u30d0\u30fc\u30b8\u30e7\u30f3\u9078\u629e</p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">\u30dd\u30fc\u30c8\u756a\u53f7</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">\u30e1\u30e2\u30ea\u5272\u308a\u5f53\u3066 (GB)</p></body></html>", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"EULA\u306b\u540c\u610f\u3059\u308b", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u4f5c\u6210", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">\u30d7\u30ec\u30a4\u30e4\u30fc\u6570\u4e0a\u9650</p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><a href=\"https://www.minecraft.net/ja-jp/eula\"><span style=\" text-decoration: underline; color:#0000ff;\">Minecraft EULA</span></a></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">MOTD</p></body></html>", None))
        self.textEdit.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS UI Gothic'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\\u00A7eThe\\u00A7a Sky\\u00A7d Blessing \\u00a76 %s \\u00A7f- \\u00A7b%s</p></body></html>", None))
    # retranslateUi

