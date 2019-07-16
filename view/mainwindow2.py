# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow2.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import view.resource_main


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1246, 974)
        MainWindow.setStyleSheet("#photo{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#info{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#video{\n"
                                 "background:#000;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#videoWindow{\n"
                                 "background:#fff;\n"
                                 "border:1px solid #000;\n"
                                 "}\n"
                                 "#browserWindow{\n"
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
                                 "#stuffPhoto{\n"
                                 "background:url(:/images/view/ivan1.jpg) no-repeat center center;\n"
                                 "}\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.info = QtWidgets.QWidget(self.centralwidget)
        self.info.setObjectName("info")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.info)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.age = QtWidgets.QLabel(self.info)
        self.age.setObjectName("age")
        self.gridLayout_5.addWidget(self.age, 2, 1, 1, 1)
        self.job = QtWidgets.QLabel(self.info)
        self.job.setObjectName("job")
        self.gridLayout_5.addWidget(self.job, 1, 1, 1, 1)
        self.jobLabel = QtWidgets.QLabel(self.info)
        self.jobLabel.setObjectName("jobLabel")
        self.gridLayout_5.addWidget(self.jobLabel, 1, 0, 1, 1)
        self.ageLabel = QtWidgets.QLabel(self.info)
        self.ageLabel.setObjectName("ageLabel")
        self.gridLayout_5.addWidget(self.ageLabel, 2, 0, 1, 1)
        self.name = QtWidgets.QLabel(self.info)
        self.name.setObjectName("name")
        self.gridLayout_5.addWidget(self.name, 0, 1, 1, 1)
        self.nameLabel = QtWidgets.QLabel(self.info)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout_5.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.timeLabel = QtWidgets.QLabel(self.info)
        self.timeLabel.setObjectName("timeLabel")
        self.gridLayout_5.addWidget(self.timeLabel, 3, 0, 1, 1)
        self.loginTime = QtWidgets.QLabel(self.info)
        self.loginTime.setObjectName("loginTime")
        self.gridLayout_5.addWidget(self.loginTime, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.info, 0, 6, 1, 1)
        self.photo = QtWidgets.QWidget(self.centralwidget)
        self.photo.setObjectName("photo")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.photo)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.stuffPhoto = QtWidgets.QLabel(self.photo)
        self.stuffPhoto.setText("")
        self.stuffPhoto.setScaledContents(True)
        self.stuffPhoto.setObjectName("stuffPhoto")
        self.gridLayout_6.addWidget(self.stuffPhoto, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.photo, 0, 5, 1, 1)
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
        self.logout = QtWidgets.QPushButton(self.status)
        self.logout.setObjectName("logout")
        self.gridLayout_2.addWidget(self.logout, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.status, 5, 6, 1, 1)
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
        self.redlight.setCheckable(True)
        self.verticalLayout.addWidget(self.redlight)
        self.yellowlight = QtWidgets.QPushButton(self.lights)
        self.yellowlight.setObjectName("yellowlight")
        self.yellowlight.setCheckable(True)
        self.verticalLayout.addWidget(self.yellowlight)
        self.greenlight = QtWidgets.QPushButton(self.lights)
        self.greenlight.setObjectName("greenlight")
        self.greenlight.setCheckable(True)
        self.verticalLayout.addWidget(self.greenlight)
        self.gridLayout.addWidget(self.lights, 5, 5, 1, 1)
        self.voice = QtWidgets.QWidget(self.centralwidget)
        self.voice.setObjectName("voice")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.voice)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.send = QtWidgets.QPushButton(self.voice)
        self.send.setObjectName("send")
        self.gridLayout_4.addWidget(self.send, 1, 1, 1, 1)
        self.input = QtWidgets.QLineEdit(self.voice)
        self.input.setObjectName("input")
        self.gridLayout_4.addWidget(self.input, 1, 0, 1, 1)
        self.output = QtWidgets.QTextBrowser(self.voice)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output.sizePolicy().hasHeightForWidth())
        self.output.setSizePolicy(sizePolicy)
        self.output.setObjectName("output")
        self.gridLayout_4.addWidget(self.output, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.voice, 5, 1, 1, 4)
        self.videoWindow = QtWidgets.QWidget(self.centralwidget)
        self.videoWindow.setObjectName("videoWindow")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.videoWindow)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.start = QtWidgets.QPushButton(self.videoWindow)
        self.start.setEnabled(False)
        self.start.setObjectName("start")
        self.gridLayout_3.addWidget(self.start, 1, 1, 1, 1)
        self.stop = QtWidgets.QPushButton(self.videoWindow)
        self.stop.setEnabled(False)
        self.stop.setObjectName("stop")
        self.gridLayout_3.addWidget(self.stop, 1, 2, 1, 1)
        self.live = QtWidgets.QPushButton(self.videoWindow)
        self.live.setObjectName("live")
        self.gridLayout_3.addWidget(self.live, 1, 0, 1, 1)
        self.open = QtWidgets.QPushButton(self.videoWindow)
        self.open.setObjectName("open")
        self.gridLayout_3.addWidget(self.open, 1, 3, 1, 1)
        self.video = QtWidgets.QLabel(self.videoWindow)
        self.video.setText("")
        self.video.setObjectName("video")
        self.gridLayout_3.addWidget(self.video, 0, 0, 1, 4)
        self.gridLayout.addWidget(self.videoWindow, 1, 5, 4, 2)
        self.browserWindow = QtWidgets.QWidget(self.centralwidget)
        self.browserWindow.setObjectName("browserWindow")
        self.gridLayout.addWidget(self.browserWindow, 0, 1, 5, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1246, 26))
        self.menubar.setObjectName("menubar")
        self.tsmiMainPage = QtWidgets.QMenu(self.menubar)
        self.tsmiMainPage.setObjectName("tsmiMainPage")
        self.tsmiPrinterSet = QtWidgets.QMenu(self.menubar)
        self.tsmiPrinterSet.setObjectName("tsmiPrinterSet")
        self.tsmiRePrint = QtWidgets.QMenu(self.menubar)
        self.tsmiRePrint.setObjectName("tsmiRePrint")
        self.tsmi_menu = QtWidgets.QMenu(self.menubar)
        self.tsmi_menu.setObjectName("tsmi_menu")
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
        self.tsmiPrinter = QtWidgets.QAction(MainWindow)
        self.tsmiPrinter.setObjectName("tsmiPrinter")
        self.tsmiPageset = QtWidgets.QAction(MainWindow)
        self.tsmiPageset.setObjectName("tsmiPageset")
        self.tsmiReceiptLabel = QtWidgets.QAction(MainWindow)
        self.tsmiReceiptLabel.setObjectName("tsmiReceiptLabel")
        self.tsmiB2Clist = QtWidgets.QAction(MainWindow)
        self.tsmiB2Clist.setObjectName("tsmiB2Clist")
        self.tsmiB2BRePrint = QtWidgets.QAction(MainWindow)
        self.tsmiB2BRePrint.setObjectName("tsmiB2BRePrint")
        self.tsmi_weightconfig = QtWidgets.QAction(MainWindow)
        self.tsmi_weightconfig.setObjectName("tsmi_weightconfig")
        self.tsmi_homePage = QtWidgets.QAction(MainWindow)
        self.tsmi_homePage.setObjectName("tsmi_homePage")
        self.actionforward = QtWidgets.QAction(MainWindow)
        self.actionforward.setObjectName("actionforward")
        self.actionbackward = QtWidgets.QAction(MainWindow)
        self.actionbackward.setObjectName("actionbackward")
        self.tsmiMainPage.addAction(self.tsmi_homePage)
        self.tsmiMainPage.addAction(self.actionforward)
        self.tsmiMainPage.addAction(self.actionbackward)
        self.tsmiPrinterSet.addAction(self.tsmiPrinter)
        self.tsmiPrinterSet.addAction(self.tsmiPageset)
        self.tsmiRePrint.addAction(self.tsmiReceiptLabel)
        self.tsmiRePrint.addAction(self.tsmiB2Clist)
        self.tsmiRePrint.addAction(self.tsmiB2BRePrint)
        self.tsmi_menu.addAction(self.tsmi_weightconfig)
        self.menubar.addAction(self.tsmiMainPage.menuAction())
        self.menubar.addAction(self.tsmiPrinterSet.menuAction())
        self.menubar.addAction(self.tsmiRePrint.menuAction())
        self.menubar.addAction(self.tsmi_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.age.setText(_translate("MainWindow", "22"))
        self.job.setText(_translate("MainWindow", "程序员"))
        self.jobLabel.setText(_translate("MainWindow", "职位"))
        self.ageLabel.setText(_translate("MainWindow", "年龄"))
        self.name.setText(_translate("MainWindow", "童晨"))
        self.nameLabel.setText(_translate("MainWindow", "姓名"))
        self.timeLabel.setText(_translate("MainWindow", "登录时间"))
        self.loginTime.setText(_translate("MainWindow", "2019-07-07 15：28"))
        self.printerLabel.setText(_translate("MainWindow", "打印机状态："))
        self.printerStatus.setText(_translate("MainWindow", "在线"))
        self.lightsLabel.setText(_translate("MainWindow", "指示灯状态："))
        self.lightStatus.setText(_translate("MainWindow", "在线"))
        self.internetLabel.setText(_translate("MainWindow", "网络状态："))
        self.internetStatus.setText(_translate("MainWindow", "在线"))
        self.serverLabel.setText(_translate("MainWindow", "服务器状态："))
        self.serverStatus.setText(_translate("MainWindow", "在线"))
        self.fresh.setText(_translate("MainWindow", "刷新"))
        self.logout.setText(_translate("MainWindow", "退出登录"))
        self.redlight.setText(_translate("MainWindow", "红灯"))
        self.yellowlight.setText(_translate("MainWindow", "黄灯"))
        self.greenlight.setText(_translate("MainWindow", "绿灯"))
        self.send.setText(_translate("MainWindow", "发送"))
        self.start.setText(_translate("MainWindow", "开始录制"))
        self.stop.setText(_translate("MainWindow", "结束录制"))
        self.live.setText(_translate("MainWindow", "开启相机"))
        self.open.setText(_translate("MainWindow", "打开文件"))
        self.tsmiMainPage.setTitle(_translate("MainWindow", "主页"))
        self.tsmiPrinterSet.setTitle(_translate("MainWindow", "打印设置"))
        self.tsmiRePrint.setTitle(_translate("MainWindow", "补打功能"))
        self.tsmi_menu.setTitle(_translate("MainWindow", "称重"))
        self.actionrecord.setText(_translate("MainWindow", "record"))
        self.actionopen.setText(_translate("MainWindow", "open"))
        self.actionlive.setText(_translate("MainWindow", "live"))
        self.tsmiPrinter.setText(_translate("MainWindow", "打印设置"))
        self.tsmiPageset.setText(_translate("MainWindow", "打印当前页面"))
        self.tsmiReceiptLabel.setText(_translate("MainWindow", "收货标签"))
        self.tsmiB2Clist.setText(_translate("MainWindow", "B2C清单"))
        self.tsmiB2BRePrint.setText(_translate("MainWindow", "B2B补打"))
        self.tsmi_weightconfig.setText(_translate("MainWindow", "配置"))
        self.tsmi_homePage.setText(_translate("MainWindow", "首页"))
        self.actionforward.setText(_translate("MainWindow", "前进"))
        self.actionbackward.setText(_translate("MainWindow", "返回"))
