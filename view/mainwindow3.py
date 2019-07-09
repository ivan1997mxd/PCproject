# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow3.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1093, 881)
        MainWindow.setStyleSheet("#video{\n"
                                 "background:#000;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#photo{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#info{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#videoWindow{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#browser{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#printer{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#voice{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#lights{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#status{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#redlight{\n"
                                 "background:#cc0000;\n"
                                 "}\n"
                                 "#yellowlight{\n"
                                 "background:#ffff00;\n"
                                 "}\n"
                                 "#greenlight{\n"
                                 "background:#00AA00;\n"
                                 "}\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.videoWindow = QtWidgets.QWidget(self.centralwidget)
        self.videoWindow.setObjectName("videoWindow")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.videoWindow)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.video = QtWidgets.QLabel(self.videoWindow)
        self.video.setText("")
        self.video.setObjectName("video")
        self.gridLayout_3.addWidget(self.video, 0, 0, 1, 4)
        self.lineEdit = QtWidgets.QLineEdit(self.videoWindow)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 2, 0, 1, 2)
        self.open = QtWidgets.QPushButton(self.videoWindow)
        self.open.setObjectName("open")
        self.gridLayout_3.addWidget(self.open, 2, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.videoWindow)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 2, 2, 1, 1)
        self.stop = QtWidgets.QPushButton(self.videoWindow)
        self.stop.setEnabled(False)
        self.stop.setObjectName("stop")
        self.gridLayout_3.addWidget(self.stop, 1, 3, 1, 1)
        self.start = QtWidgets.QPushButton(self.videoWindow)
        self.start.setObjectName("start")
        self.gridLayout_3.addWidget(self.start, 1, 2, 1, 1)
        self.live = QtWidgets.QPushButton(self.videoWindow)
        self.live.setObjectName("live")
        self.gridLayout_3.addWidget(self.live, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.videoWindow, 1, 3, 2, 2)
        self.browser = QtWidgets.QWidget(self.centralwidget)
        self.browser.setObjectName("browser")
        self.gridLayout.addWidget(self.browser, 0, 1, 3, 2)
        self.status = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        self.status.setStyleSheet("")
        self.status.setObjectName("status")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.status)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.printerLabel = QtWidgets.QLabel(self.status)
        self.printerLabel.setObjectName("printerLabel")
        self.gridLayout_2.addWidget(self.printerLabel, 0, 0, 1, 1)
        self.printerStatus = QtWidgets.QLabel(self.status)
        self.printerStatus.setObjectName("printerStatus")
        self.gridLayout_2.addWidget(self.printerStatus, 0, 1, 1, 1)
        self.lightsLabel = QtWidgets.QLabel(self.status)
        self.lightsLabel.setObjectName("lightsLabel")
        self.gridLayout_2.addWidget(self.lightsLabel, 1, 0, 1, 1)
        self.lightStatus = QtWidgets.QLabel(self.status)
        self.lightStatus.setObjectName("lightStatus")
        self.gridLayout_2.addWidget(self.lightStatus, 1, 1, 1, 1)
        self.internetLabel = QtWidgets.QLabel(self.status)
        self.internetLabel.setObjectName("internetLabel")
        self.gridLayout_2.addWidget(self.internetLabel, 2, 0, 1, 1)
        self.internetStatus = QtWidgets.QLabel(self.status)
        self.internetStatus.setObjectName("internetStatus")
        self.gridLayout_2.addWidget(self.internetStatus, 2, 1, 1, 1)
        self.serverLabel = QtWidgets.QLabel(self.status)
        self.serverLabel.setObjectName("serverLabel")
        self.gridLayout_2.addWidget(self.serverLabel, 3, 0, 1, 1)
        self.serverStatus = QtWidgets.QLabel(self.status)
        self.serverStatus.setObjectName("serverStatus")
        self.gridLayout_2.addWidget(self.serverStatus, 3, 1, 1, 1)
        self.fresh = QtWidgets.QPushButton(self.status)
        self.fresh.setObjectName("fresh")
        self.gridLayout_2.addWidget(self.fresh, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.status, 3, 4, 1, 1)
        self.lights = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lights.sizePolicy().hasHeightForWidth())
        self.lights.setSizePolicy(sizePolicy)
        self.lights.setObjectName("lights")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.lights)
        self.verticalLayout.setObjectName("verticalLayout")
        self.redlight = QtWidgets.QPushButton(self.lights)
        self.redlight.setObjectName("redlight")
        self.verticalLayout.addWidget(self.redlight)
        self.yellowlight = QtWidgets.QPushButton(self.lights)
        self.yellowlight.setObjectName("yellowlight")
        self.verticalLayout.addWidget(self.yellowlight)
        self.greenlight = QtWidgets.QPushButton(self.lights)
        self.greenlight.setObjectName("greenlight")
        self.verticalLayout.addWidget(self.greenlight)
        self.gridLayout.addWidget(self.lights, 3, 3, 1, 1)
        self.photo = QtWidgets.QWidget(self.centralwidget)
        self.photo.setObjectName("photo")
        self.gridLayout.addWidget(self.photo, 0, 3, 1, 1)
        self.info = QtWidgets.QWidget(self.centralwidget)
        self.info.setObjectName("info")
        self.gridLayout.addWidget(self.info, 0, 4, 1, 1)
        self.voice = QtWidgets.QWidget(self.centralwidget)
        self.voice.setObjectName("voice")
        self.gridLayout.addWidget(self.voice, 3, 1, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionrecord = QtWidgets.QAction(MainWindow)
        self.actionrecord.setObjectName("actionrecord")
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionlive = QtWidgets.QAction(MainWindow)
        self.actionlive.setObjectName("actionlive")
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.menu.addAction(self.actionexit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open.setText(_translate("MainWindow", "打开文件"))
        self.pushButton.setText(_translate("MainWindow", "浏览"))
        self.stop.setText(_translate("MainWindow", "结束录制"))
        self.start.setText(_translate("MainWindow", "开始录制"))
        self.live.setText(_translate("MainWindow", "开启相机"))
        self.printerLabel.setText(_translate("MainWindow", "打印机状态："))
        self.printerStatus.setText(_translate("MainWindow", "在线"))
        self.lightsLabel.setText(_translate("MainWindow", "指示灯状态："))
        self.lightStatus.setText(_translate("MainWindow", "在线"))
        self.internetLabel.setText(_translate("MainWindow", "网络状态："))
        self.internetStatus.setText(_translate("MainWindow", "在线"))
        self.serverLabel.setText(_translate("MainWindow", "服务器状态："))
        self.serverStatus.setText(_translate("MainWindow", "在线"))
        self.fresh.setText(_translate("MainWindow", "刷新"))
        self.redlight.setText(_translate("MainWindow", "红灯"))
        self.yellowlight.setText(_translate("MainWindow", "黄灯"))
        self.greenlight.setText(_translate("MainWindow", "绿灯"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.actionrecord.setText(_translate("MainWindow", "record"))
        self.actionopen.setText(_translate("MainWindow", "open"))
        self.actionlive.setText(_translate("MainWindow", "live"))
        self.actionexit.setText(_translate("MainWindow", "exit"))
