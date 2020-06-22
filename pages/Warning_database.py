# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication


class UiWarningDatabase(QDialog):

    def __init__(self):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(450, 300)
        self.setMaximumSize(QtCore.QSize(450, 300))
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(80, 100, 300, 71))
        self.label.setMinimumSize(QtCore.QSize(221, 71))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 0, 0);")
        self.label.setObjectName("label")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(self.translate("Dialog", "Dialog"))
        self.label.setText(self.translate("Dialog", "请先配置数据库"))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_win = UiWarningDatabase()

    main_win.show()
    sys.exit(app.exec_())