# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication


class UiMultithreading(QDialog):

    def __init__(self):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(300, 400)
        self.num = 1

        self.one = QtWidgets.QRadioButton(self)
        self.one.setGeometry(QtCore.QRect(80, 70, 200, 50))
        self.one.setObjectName("one")
        self.one.click()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.one.setFont(font)
        self.one.clicked.connect(self.one_click)

        self.two = QtWidgets.QRadioButton(self)
        self.two.setGeometry(QtCore.QRect(80, 110, 200, 50))
        self.two.setObjectName("two")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.two.setFont(font)
        self.two.clicked.connect(self.two_click)

        self.three = QtWidgets.QRadioButton(self)
        self.three.setGeometry(QtCore.QRect(80, 150, 200, 50))
        self.three.setObjectName("three")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.three.setFont(font)
        self.three.clicked.connect(self.three_click)

        self.four = QtWidgets.QRadioButton(self)
        self.four.setGeometry(QtCore.QRect(80, 190, 200, 50))
        self.four.setObjectName("four")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.four.setFont(font)
        self.four.clicked.connect(self.four_click)

        self.five = QtWidgets.QRadioButton(self)
        self.five.setGeometry(QtCore.QRect(80, 230, 200, 50))
        self.five.setObjectName("five")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.five.setFont(font)
        self.five.clicked.connect(self.five_click)

        self.setWindowTitle("Dialog")
        self.one.setText("一个线程")
        self.two.setText("两个线程")
        self.four.setText("四个线程")
        self.five.setText("五个线程")
        self.three.setText("三个线程")
        QtCore.QMetaObject.connectSlotsByName(self)

    def one_click(self):
        self.num = 1

    def two_click(self):
        self.num = 2

    def three_click(self):
        self.num = 3

    def four_click(self):
        self.num = 4

    def five_click(self):
        self.num = 5




if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_win = UiMultithreading()

    main_win.show()
    sys.exit(app.exec_())
