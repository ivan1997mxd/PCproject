# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_setting(object):
    def setupUi(self, setting):
        setting.setObjectName("setting")
        setting.resize(408, 340)
        self.gridLayout = QtWidgets.QGridLayout(setting)
        self.gridLayout.setObjectName("gridLayout")
        self.reportEdit = QtWidgets.QLineEdit(setting)
        self.reportEdit.setObjectName("reportEdit")
        self.gridLayout.addWidget(self.reportEdit, 0, 1, 1, 1)
        self.tagEdit = QtWidgets.QLineEdit(setting)
        self.tagEdit.setObjectName("tagEdit")
        self.gridLayout.addWidget(self.tagEdit, 1, 1, 1, 1)
        self.invoiceEdit = QtWidgets.QLineEdit(setting)
        self.invoiceEdit.setObjectName("invoiceEdit")
        self.gridLayout.addWidget(self.invoiceEdit, 2, 1, 1, 1)
        self.reportSetting = QtWidgets.QPushButton(setting)
        self.reportSetting.setObjectName("reportSetting")
        self.gridLayout.addWidget(self.reportSetting, 0, 2, 1, 1)
        self.tagSetting = QtWidgets.QPushButton(setting)
        self.tagSetting.setObjectName("tagSetting")
        self.gridLayout.addWidget(self.tagSetting, 1, 2, 1, 1)
        self.invoiceSetting = QtWidgets.QPushButton(setting)
        self.invoiceSetting.setObjectName("invoiceSetting")
        self.gridLayout.addWidget(self.invoiceSetting, 2, 2, 1, 1)
        self.reportlabel = QtWidgets.QLabel(setting)
        self.reportlabel.setObjectName("reportlabel")
        self.gridLayout.addWidget(self.reportlabel, 0, 0, 1, 1)
        self.tagLabel = QtWidgets.QLabel(setting)
        self.tagLabel.setObjectName("tagLabel")
        self.gridLayout.addWidget(self.tagLabel, 1, 0, 1, 1)
        self.invoiceLabel = QtWidgets.QLabel(setting)
        self.invoiceLabel.setObjectName("invoiceLabel")
        self.gridLayout.addWidget(self.invoiceLabel, 2, 0, 1, 1)
        self.save = QtWidgets.QPushButton(setting)
        self.save.setObjectName("save")
        self.gridLayout.addWidget(self.save, 3, 2, 1, 1)

        self.retranslateUi(setting)
        QtCore.QMetaObject.connectSlotsByName(setting)

    def retranslateUi(self, setting):
        _translate = QtCore.QCoreApplication.translate
        setting.setWindowTitle(_translate("setting", "setting"))
        self.reportSetting.setText(_translate("setting", "设置"))
        self.tagSetting.setText(_translate("setting", "设置"))
        self.invoiceSetting.setText(_translate("setting", "设置"))
        self.reportlabel.setText(_translate("setting", "0.报表"))
        self.tagLabel.setText(_translate("setting", "1.标签"))
        self.invoiceLabel.setText(_translate("setting", "2.发票"))
        self.save.setText(_translate("setting", "保存"))


