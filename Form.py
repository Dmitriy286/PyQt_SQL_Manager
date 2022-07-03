# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Form.ui'
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
        MainWindow.resize(967, 736)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mainTableView = QTableView(self.centralwidget)
        self.mainTableView.setObjectName(u"mainTableView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTableView.sizePolicy().hasHeightForWidth())
        self.mainTableView.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.mainTableView)

        self.secondaryTableView = QTableView(self.centralwidget)
        self.secondaryTableView.setObjectName(u"secondaryTableView")
        sizePolicy.setHeightForWidth(self.secondaryTableView.sizePolicy().hasHeightForWidth())
        self.secondaryTableView.setSizePolicy(sizePolicy)
        self.secondaryTableView.setMinimumSize(QSize(0, 0))
        self.secondaryTableView.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout.addWidget(self.secondaryTableView)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setMinimumSize(QSize(0, 200))
        self.groupBox.setMaximumSize(QSize(16777215, 300))
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(650, 10, 300, 31))
        sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy1)
        self.comboBox.setMinimumSize(QSize(300, 0))
        self.comboBox.setMaximumSize(QSize(300, 16777215))
        self.savePB = QPushButton(self.groupBox)
        self.savePB.setObjectName(u"savePB")
        self.savePB.setGeometry(QRect(10, 30, 231, 31))
        self.showAllPB = QPushButton(self.groupBox)
        self.showAllPB.setObjectName(u"showAllPB")
        self.showAllPB.setGeometry(QRect(10, 120, 231, 31))
        self.findPB = QPushButton(self.groupBox)
        self.findPB.setObjectName(u"findPB")
        self.findPB.setGeometry(QRect(10, 150, 231, 31))
        self.plainTextEdit = QPlainTextEdit(self.groupBox)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(250, 150, 211, 31))
        self.addRowPB = QPushButton(self.groupBox)
        self.addRowPB.setObjectName(u"addRowPB")
        self.addRowPB.setGeometry(QRect(10, 90, 231, 31))
        self.deleteRowPB = QPushButton(self.groupBox)
        self.deleteRowPB.setObjectName(u"deleteRowPB")
        self.deleteRowPB.setGeometry(QRect(10, 60, 231, 31))
        self.lcdNumber = QLCDNumber(self.groupBox)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QRect(480, 60, 111, 31))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(480, 30, 111, 31))
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.deleteBasePB = QPushButton(self.groupBox)
        self.deleteBasePB.setObjectName(u"deleteBasePB")
        self.deleteBasePB.setGeometry(QRect(240, 30, 231, 31))
        self.createBasePB = QPushButton(self.groupBox)
        self.createBasePB.setObjectName(u"createBasePB")
        self.createBasePB.setGeometry(QRect(240, 60, 231, 31))

        self.horizontalLayout_2.addWidget(self.groupBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 967, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"CRUD Menu", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Employee", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Customer", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Order", None))

        self.savePB.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.showAllPB.setText(QCoreApplication.translate("MainWindow", u"Show all", None))
        self.findPB.setText(QCoreApplication.translate("MainWindow", u"Find by name", None))
        self.addRowPB.setText(QCoreApplication.translate("MainWindow", u"Add row", None))
        self.deleteRowPB.setText(QCoreApplication.translate("MainWindow", u"Delete row", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Row count", None))
        self.deleteBasePB.setText(QCoreApplication.translate("MainWindow", u"Delete base", None))
        self.createBasePB.setText(QCoreApplication.translate("MainWindow", u"Create base", None))
    # retranslateUi

