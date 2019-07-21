# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signup.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import view.resource


class Ui_signup(object):
    def setupUi(self, signup):
        signup.setObjectName("signup")
        signup.resize(769, 719)
        signup.setAutoFillBackground(False)
        signup.setStyleSheet("#signup{\n"
                             "background:url(:/image/timg.jpg);\n"
                             "}\n"
                             "#UI{\n"
                             "background:rgba(0,0,0,0.5);\n"
                             "}\n"
                             "#signBtn{\n"
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
                             "#title,#photoLabel,#nameLabel,#pwdLabel,#ageLabel,#jobLabel{\n"
                             "color:#fff;\n"
                             "background:transparent;\n"
                             "font-size:24px;\n"
                             "}\n"
                             "#ageBox,#jobBox,#pickBtn,#shotBtn{\n"
                             "\n"
                             "font-size:18px;\n"
                             "}\n"
                             "")
        self.UI = QtWidgets.QFrame(signup)
        self.UI.setGeometry(QtCore.QRect(90, 60, 581, 581))
        self.UI.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UI.setFrameShadow(QtWidgets.QFrame.Raised)
        self.UI.setObjectName("UI")
        self.signBtn = QtWidgets.QPushButton(self.UI)
        self.signBtn.setGeometry(QtCore.QRect(20, 500, 541, 51))
        self.signBtn.setObjectName("signBtn")
        self.username = QtWidgets.QLineEdit(self.UI)
        self.username.setGeometry(QtCore.QRect(30, 130, 531, 51))
        self.username.setText("")
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(self.UI)
        self.password.setGeometry(QtCore.QRect(30, 230, 531, 51))
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.title = QtWidgets.QLabel(self.UI)
        self.title.setGeometry(QtCore.QRect(210, 40, 151, 31))
        self.title.setObjectName("title")
        self.nameLabel = QtWidgets.QLabel(self.UI)
        self.nameLabel.setGeometry(QtCore.QRect(30, 90, 81, 31))
        self.nameLabel.setObjectName("nameLabel")
        self.pwdLabel = QtWidgets.QLabel(self.UI)
        self.pwdLabel.setGeometry(QtCore.QRect(30, 190, 51, 31))
        self.pwdLabel.setObjectName("pwdLabel")
        self.ageLabel = QtWidgets.QLabel(self.UI)
        self.ageLabel.setGeometry(QtCore.QRect(30, 300, 71, 31))
        self.ageLabel.setObjectName("ageLabel")
        self.ageBox = QtWidgets.QSpinBox(self.UI)
        self.ageBox.setGeometry(QtCore.QRect(110, 310, 81, 22))
        self.ageBox.setObjectName("ageBox")
        self.jobBox = QtWidgets.QComboBox(self.UI)
        self.jobBox.setGeometry(QtCore.QRect(110, 370, 101, 31))
        self.jobBox.setObjectName("jobBox")
        self.jobBox.addItem("")
        self.jobBox.addItem("")
        self.jobBox.addItem("")
        self.jobBox.addItem("")
        self.jobBox.addItem("")
        self.jobLabel = QtWidgets.QLabel(self.UI)
        self.jobLabel.setGeometry(QtCore.QRect(30, 370, 61, 31))
        self.jobLabel.setObjectName("jobLabel")
        self.photoLabel = QtWidgets.QLabel(self.UI)
        self.photoLabel.setGeometry(QtCore.QRect(30, 430, 71, 41))
        self.photoLabel.setObjectName("photoLabel")
        self.photo = QtWidgets.QLabel(self.UI)
        self.photo.setGeometry(QtCore.QRect(330, 300, 191, 171))
        self.photo.setText("")
        self.photo.setObjectName("photo")
        self.pickBtn = QtWidgets.QPushButton(self.UI)
        self.pickBtn.setGeometry(QtCore.QRect(110, 440, 71, 28))
        self.pickBtn.setObjectName("pickBtn")
        self.shotBtn = QtWidgets.QPushButton(self.UI)
        self.shotBtn.setGeometry(QtCore.QRect(190, 440, 71, 28))
        self.shotBtn.setObjectName("shotBtn")

        self.retranslateUi(signup)
        QtCore.QMetaObject.connectSlotsByName(signup)

    def retranslateUi(self, signup):
        _translate = QtCore.QCoreApplication.translate
        signup.setWindowTitle(_translate("signup", "注册"))
        self.signBtn.setText(_translate("signup", "注册"))
        self.username.setPlaceholderText(_translate("signup", "请输入用户名"))
        self.password.setPlaceholderText(_translate("signup", "请输入密码"))
        self.title.setText(_translate("signup", "欢迎，请注册"))
        self.nameLabel.setText(_translate("signup", "用户名"))
        self.pwdLabel.setText(_translate("signup", "密码"))
        self.ageLabel.setText(_translate("signup", "年龄"))
        self.jobBox.setItemText(0, _translate("signup", "程序员"))
        self.jobBox.setItemText(1, _translate("signup", "扫货员"))
        self.jobBox.setItemText(2, _translate("signup", "拣货员"))
        self.jobBox.setItemText(3, _translate("signup", "经理"))
        self.jobBox.setItemText(4, _translate("signup", "老板"))
        self.jobLabel.setText(_translate("signup", "职位"))
        self.photoLabel.setText(_translate("signup", "照片"))
        self.pickBtn.setText(_translate("signup", "选取"))
        self.shotBtn.setText(_translate("signup", "拍照"))
