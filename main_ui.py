# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.1.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(803, 491)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(803, 491))
        MainWindow.setMaximumSize(QSize(803, 491))
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
        self.label_5.setGeometry(QRect(20, 20, 221, 31))
        self.pushButton_datapack_update = QPushButton(self.tab_2)
        self.pushButton_datapack_update.setObjectName(u"pushButton_datapack_update")
        self.pushButton_datapack_update.setEnabled(False)
        self.pushButton_datapack_update.setGeometry(QRect(490, 190, 141, 41))
        self.pushButton_level_update = QPushButton(self.tab_2)
        self.pushButton_level_update.setObjectName(u"pushButton_level_update")
        self.pushButton_level_update.setEnabled(False)
        self.pushButton_level_update.setGeometry(QRect(490, 240, 141, 41))
        self.pushButton_datapack_delete = QPushButton(self.tab_2)
        self.pushButton_datapack_delete.setObjectName(u"pushButton_datapack_delete")
        self.pushButton_datapack_delete.setEnabled(False)
        self.pushButton_datapack_delete.setGeometry(QRect(640, 140, 141, 41))
        self.pushButton_level_explorer = QPushButton(self.tab_2)
        self.pushButton_level_explorer.setObjectName(u"pushButton_level_explorer")
        self.pushButton_level_explorer.setEnabled(False)
        self.pushButton_level_explorer.setGeometry(QRect(640, 290, 141, 41))
        self.pushButton_level_vscode = QPushButton(self.tab_2)
        self.pushButton_level_vscode.setObjectName(u"pushButton_level_vscode")
        self.pushButton_level_vscode.setEnabled(False)
        self.pushButton_level_vscode.setGeometry(QRect(490, 290, 141, 41))
        self.pushButton_datapack_extract = QPushButton(self.tab_2)
        self.pushButton_datapack_extract.setObjectName(u"pushButton_datapack_extract")
        self.pushButton_datapack_extract.setEnabled(False)
        self.pushButton_datapack_extract.setGeometry(QRect(490, 140, 141, 41))
        self.pushButton_level_extractall = QPushButton(self.tab_2)
        self.pushButton_level_extractall.setObjectName(u"pushButton_level_extractall")
        self.pushButton_level_extractall.setEnabled(False)
        self.pushButton_level_extractall.setGeometry(QRect(640, 240, 141, 41))
        self.pushButton_datapack_add = QPushButton(self.tab_2)
        self.pushButton_datapack_add.setObjectName(u"pushButton_datapack_add")
        self.pushButton_datapack_add.setEnabled(False)
        self.pushButton_datapack_add.setGeometry(QRect(640, 190, 141, 41))
        self.treeWidget = QTreeWidget(self.tab_2)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(20, 60, 460, 271))
        self.treeWidget.setWordWrap(False)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setDefaultSectionSize(160)
        self.lineEdit_2 = QLineEdit(self.tab_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(490, 110, 251, 21))
        self.toolButton_2 = QToolButton(self.tab_2)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setGeometry(QRect(750, 110, 31, 21))
        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(490, 60, 141, 41))
        self.pushButton_11 = QPushButton(self.tab_2)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(640, 60, 141, 41))
        self.pushButton_12 = QPushButton(self.tab_2)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setGeometry(QRect(390, 20, 91, 31))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setEnabled(True)
        self.tabWidget.addTab(self.tab, "")
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
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u30ef\u30fc\u30eb\u30c9\u4e00\u89a7</p></body></html>", None))
        self.pushButton_datapack_update.setText(QCoreApplication.translate("MainWindow", u"\u30c7\u30fc\u30bf\u30d1\u30c3\u30af\u3092\u30a2\u30c3\u30d7\u30c7\u30fc\u30c8", None))
        self.pushButton_level_update.setText(QCoreApplication.translate("MainWindow", u"\u6700\u65b0\u306ecommit\u3092\u9069\u7528", None))
        self.pushButton_datapack_delete.setText(QCoreApplication.translate("MainWindow", u"\u30c7\u30fc\u30bf\u30d1\u30c3\u30af\u3092\u524a\u9664", None))
        self.pushButton_level_explorer.setText(QCoreApplication.translate("MainWindow", u"\u30a8\u30af\u30b9\u30d7\u30ed\u30fc\u30e9\u30fc\u3067\u8868\u793a", None))
        self.pushButton_level_vscode.setText(QCoreApplication.translate("MainWindow", u"VSCode\u3067\u958b\u304f", None))
        self.pushButton_datapack_extract.setText(QCoreApplication.translate("MainWindow", u"\u30c7\u30fc\u30bf\u30d1\u30c3\u30af\u3092\u5c55\u958b", None))
        self.pushButton_level_extractall.setText(QCoreApplication.translate("MainWindow", u"\u5168\u3066\u306e\u30c7\u30fc\u30bf\u30d1\u30c3\u30af\u3092\u5c55\u958b", None))
        self.pushButton_datapack_add.setText(QCoreApplication.translate("MainWindow", u"\u30c7\u30fc\u30bf\u30d1\u30c3\u30af\u3092\u8ffd\u52a0", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u8a73\u7d30", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u30ef\u30fc\u30eb\u30c9 / \u30c7\u30fc\u30bf\u30d1\u30c3\u30af", None));
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">saves\u30d5\u30a9\u30eb\u30c0</p><p align=\"center\">\u53c8\u306f\u30b5\u30fc\u30d0\u30fc\u306e\u30d5\u30a9\u30eb\u30c0</p></body></html>", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52d5\u691c\u51fa", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"\u518d\u8aad\u307f\u8fbc\u307f", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u30c4\u30fc\u30eb (\u4e00\u822c)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u30c4\u30fc\u30eb (\u8a73\u7d30)", None))
    # retranslateUi

