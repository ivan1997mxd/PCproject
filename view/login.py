# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import resource


class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(756, 470)
        login.setAutoFillBackground(False)
        login.setStyleSheet("#login{\n"
                            "background:url(:/image/bg.jpg);\n"
                            "}\n"
                            "#UI{\n"
                            "background:rgba(0,0,0,0.5);\n"
                            "}\n"
                            "#loginBtn{\n"
                            "background:#03a9f4;\n"
                            "color:#fff;\n"
                            "border-radius:15px;\n"
                            "font-size:22px;\n"
                            "}\n"
                            "#faceBtn{\n"
                            "background:transparent;\n"
                            "font-size:18px;\n"
                            "color:#fff;\n"
                            "font-size:22px;\n"
                            "}\n"
                            "#faceRegister{\n"
                            "background:transparent;\n"
                            "font-size:18px;\n"
                            "color:#fff;\n"
                            "font-size:22px;\n"
                            "}\n"
                            "#username{\n"
                            "border-radius:15px;\n"
                            "color:#03a9f4;\n"
                            "font-size:22px;\n"
                            "}\n"
                            "#password{\n"
                            "border-radius:15px;\n"
                            "color:#03a9f4;\n"
                            "font-size:22px;\n"
                            "}\n"
                            "#title{\n"
                            "color:#fff;\n"
                            "background:transparent;\n"
                            "font-size:24px;\n"
                            "}\n"
                            "")
        self.UI = QtWidgets.QFrame(login)
        self.UI.setGeometry(QtCore.QRect(90, 50, 581, 371))
        self.UI.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UI.setFrameShadow(QtWidgets.QFrame.Raised)
        self.UI.setObjectName("UI")
        self.loginBtn = QtWidgets.QPushButton(self.UI)
        self.loginBtn.setGeometry(QtCore.QRect(20, 300, 541, 51))
        self.loginBtn.setObjectName("loginBtn")
        self.username = QtWidgets.QLineEdit(self.UI)
        self.username.setGeometry(QtCore.QRect(20, 90, 541, 51))
        self.username.setText("")
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(self.UI)
        self.password.setGeometry(QtCore.QRect(20, 170, 541, 51))
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.title = QtWidgets.QLabel(self.UI)
        self.title.setGeometry(QtCore.QRect(150, 30, 261, 31))
        self.title.setObjectName("title")
        self.faceRegister = QtWidgets.QPushButton(self.UI)
        self.faceRegister.setGeometry(QtCore.QRect(20, 250, 93, 28))
        self.faceRegister.setObjectName("faceRegister")
        self.faceBtn = QtWidgets.QPushButton(self.UI)
        self.faceBtn.setGeometry(QtCore.QRect(450, 250, 93, 28))
        self.faceBtn.setObjectName("faceBtn")

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "登录"))
        self.loginBtn.setText(_translate("login", "Log in"))
        self.username.setPlaceholderText(_translate("login", "Username"))
        self.password.setPlaceholderText(_translate("login", "Password"))
        self.title.setText(_translate("login", "Welcome, Please Log in"))
        self.faceBtn.setText(_translate("login", "人脸登录"))
        self.faceRegister.setText(_translate("login", "账号注册"))
