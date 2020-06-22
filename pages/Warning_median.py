# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'warnning_median.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog


class UiWarningMedian(QDialog):

    def __init__(self):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(700, 300)
        self.setMaximumSize(QtCore.QSize(700, 300))
        self.setMinimumSize(QtCore.QSize(700, 300))
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(40, 100, 650, 71))
        self.label.setMinimumSize(QtCore.QSize(221, 71))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 0, 0);")
        self.label.setObjectName("label")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "请先配置中位数或者体重矫正参数"))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_win = UiWarningMedian()

    main_win.show()
    sys.exit(app.exec_())