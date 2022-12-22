# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'datapack_manager.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QPushButton,
    QSizePolicy, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1000, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(1000, 600))
        Dialog.setMaximumSize(QSize(1000, 600))
        self.treeWidget = QTreeWidget(Dialog)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(20, 20, 391, 561))
        self.treeWidget.setMinimumSize(QSize(291, 0))
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setMinimumSectionSize(150)
        self.treeWidget.header().setDefaultSectionSize(150)
        self.treeWidget.header().setHighlightSections(False)
        self.treeWidget.header().setProperty("showSortIndicator", False)
        self.treeWidget.header().setStretchLastSection(True)
        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(430, 20, 551, 391))
        self.textBrowser.setOpenExternalLinks(True)
        self.pushButton_local_install = QPushButton(Dialog)
        self.pushButton_local_install.setObjectName(u"pushButton_local_install")
        self.pushButton_local_install.setGeometry(QRect(840, 540, 141, 41))
        self.pushButton_install = QPushButton(Dialog)
        self.pushButton_install.setObjectName(u"pushButton_install")
        self.pushButton_install.setGeometry(QRect(690, 540, 141, 41))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"\u30d0\u30fc\u30b8\u30e7\u30f3", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"\u4f5c\u8005", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"\u30d1\u30c3\u30b1\u30fc\u30b8\u540d", None));
        self.pushButton_local_install.setText(QCoreApplication.translate("Dialog", u"\u30d5\u30a1\u30a4\u30eb\u304b\u3089\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb", None))
        self.pushButton_install.setText(QCoreApplication.translate("Dialog", u"\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb", None))
    # retranslateUi

