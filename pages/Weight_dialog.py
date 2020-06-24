# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication


class UiWeight(QDialog):

    def __init__(self):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(840, 630)
        self.setMinimumSize(QtCore.QSize(840, 630))
        self.setMaximumSize(QtCore.QSize(840, 630))
        self.setWindowTitle("体重校正参数设置")
        self.prompt_message_setting()
        self.table_setting()
        # self.select_box_setting()
        self.connect = None
        QtCore.QMetaObject.connectSlotsByName(self)

    def prompt_message_setting(self):
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 500, 780, 100))
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setPlainText("1:mom=result/median/10^(A-B*weight)\n"
                                        "2:mom=result/median/(A+B/weight)\n"
                                        "3:mom=result/median/10^(A*weight^2-B*weight+C)\n"
                                        "4:mom=result/median")

    def table_setting(self):
        self.tableWidget = QtWidgets.QTableWidget(self)
        # self.tableWidget.setEnabled(False)
        self.tableWidget.setGeometry(QtCore.QRect(30, 20, 780, 480))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setRowCount(13)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setObjectName("tableWidget")
        for i in range(6):
            for j in range(13):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(j, i, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(130)
        self.tableWidget.verticalHeader().setDefaultSectionSize(35)
        self.tableWidget.verticalHeader().setHighlightSections(True)

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText("1早/2中")
        item = self.tableWidget.item(0, 1)
        item.setText("体重校正类型")
        item = self.tableWidget.item(0, 2)
        item.setText("参数A")
        item = self.tableWidget.item(0, 3)
        item.setText("参数B")
        item = self.tableWidget.item(0, 4)
        item.setText("参数C")
        item = self.tableWidget.item(0, 5)
        item.setText("参数D")
        item = self.tableWidget.item(1, 0)
        item.setText("AFP1早")
        item = self.tableWidget.item(2, 0)
        item.setText("hCG1")
        item = self.tableWidget.item(3, 0)
        item.setText("fbhCG1")
        item = self.tableWidget.item(4, 0)
        item.setText("uE31")
        item = self.tableWidget.item(5, 0)
        item.setText("InhA1")
        item = self.tableWidget.item(6, 0)
        item.setText("PAPPA1")
        item = self.tableWidget.item(7, 0)
        item.setText("AFP2中")
        item = self.tableWidget.item(8, 0)
        item.setText("hCG2")
        item = self.tableWidget.item(9, 0)
        item.setText("fbhCG2")
        item = self.tableWidget.item(10, 0)
        item.setText("uE32")
        item = self.tableWidget.item(11, 0)
        item.setText("InhA2")
        item = self.tableWidget.item(12, 0)
        item.setText("PAPPA2")
        self.tableWidget.setSortingEnabled(__sortingEnabled)

    # def select_box_setting(self):
    #     self.AFP1 = QtWidgets.QComboBox(self)
    #     self.AFP1.setGeometry(QtCore.QRect(160, 55, 100, 30))
    #     self.AFP1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                             "font: 12pt \"Arial\";")
    #     self.AFP1.setObjectName("AFP1")
    #     self.AFP1.addItem("1")
    #     self.AFP1.addItem("2")
    #     self.AFP1.addItem("3")
    #     self.AFP1.addItem("4")
    #     self.hCG1 = QtWidgets.QComboBox(self)
    #     self.hCG1.setGeometry(QtCore.QRect(160, 90, 100, 30))
    #     self.hCG1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                             "font: 12pt \"Arial\";")
    #     self.hCG1.setObjectName("hCG1")
    #     self.hCG1.addItem("1")
    #     self.hCG1.addItem("2")
    #     self.hCG1.addItem("3")
    #     self.hCG1.addItem("4")
    #     self.fbhCG1 = QtWidgets.QComboBox(self)
    #     self.fbhCG1.setGeometry(QtCore.QRect(160, 125, 100, 30))
    #     self.fbhCG1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                               "font: 12pt \"Arial\";")
    #     self.fbhCG1.setObjectName("fbhCG1")
    #     self.fbhCG1.addItem("1")
    #     self.fbhCG1.addItem("2")
    #     self.fbhCG1.addItem("3")
    #     self.fbhCG1.addItem("4")
    #     self.uE31 = QtWidgets.QComboBox(self)
    #     self.uE31.setGeometry(QtCore.QRect(160, 160, 100, 30))
    #     self.uE31.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                             "font: 12pt \"Arial\";")
    #     self.uE31.setObjectName("uE31")
    #     self.uE31.addItem("1")
    #     self.uE31.addItem("2")
    #     self.uE31.addItem("3")
    #     self.uE31.addItem("4")
    #     self.InhA1 = QtWidgets.QComboBox(self)
    #     self.InhA1.setGeometry(QtCore.QRect(160, 195, 100, 30))
    #     self.InhA1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                              "font: 12pt \"Arial\";")
    #     self.InhA1.setObjectName("InhA1")
    #     self.InhA1.addItem("1")
    #     self.InhA1.addItem("2")
    #     self.InhA1.addItem("3")
    #     self.InhA1.addItem("4")
    #     self.PAPPA1 = QtWidgets.QComboBox(self)
    #     self.PAPPA1.setGeometry(QtCore.QRect(160, 230, 100, 30))
    #     self.PAPPA1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                               "font: 12pt \"Arial\";")
    #     self.PAPPA1.setObjectName("PAPPA1")
    #     self.PAPPA1.addItem("1")
    #     self.PAPPA1.addItem("2")
    #     self.PAPPA1.addItem("3")
    #     self.PAPPA1.addItem("4")
    #     self.AFP2 = QtWidgets.QComboBox(self)
    #     self.AFP2.setGeometry(QtCore.QRect(160, 265, 100, 30))
    #     self.AFP2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                             "font: 12pt \"Arial\";")
    #     self.AFP2.setObjectName("AFP2")
    #     self.AFP2.addItem("1")
    #     self.AFP2.addItem("2")
    #     self.AFP2.addItem("3")
    #     self.AFP2.addItem("4")
    #     self.hCG2 = QtWidgets.QComboBox(self)
    #     self.hCG2.setGeometry(QtCore.QRect(160, 300, 100, 30))
    #     self.hCG2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                             "font: 12pt \"Arial\";")
    #     self.hCG2.setObjectName("hCG2")
    #     self.hCG2.addItem("1")
    #     self.hCG2.addItem("2")
    #     self.hCG2.addItem("3")
    #     self.hCG2.addItem("4")
    #     self.fbhCG2 = QtWidgets.QComboBox(self)
    #     self.fbhCG2.setGeometry(QtCore.QRect(160, 335, 100, 30))
    #     self.fbhCG2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                               "font: 12pt \"Arial\";")
    #     self.fbhCG2.setObjectName("fbhCG2")
    #     self.fbhCG2.addItem("1")
    #     self.fbhCG2.addItem("2")
    #     self.fbhCG2.addItem("3")
    #     self.fbhCG2.addItem("4")
    #     self.uE32 = QtWidgets.QComboBox(self)
    #     self.uE32.setGeometry(QtCore.QRect(160, 370, 100, 30))
    #     self.uE32.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                             "font: 12pt \"Arial\";")
    #     self.uE32.setObjectName("uE32")
    #     self.uE32.addItem("1")
    #     self.uE32.addItem("2")
    #     self.uE32.addItem("3")
    #     self.uE32.addItem("4")
    #     self.InhA2 = QtWidgets.QComboBox(self)
    #     self.InhA2.setGeometry(QtCore.QRect(160, 405, 100, 30))
    #     self.InhA2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                              "font: 12pt \"Arial\";")
    #     self.InhA2.setObjectName("InhA2")
    #     self.InhA2.addItem("1")
    #     self.InhA2.addItem("2")
    #     self.InhA2.addItem("3")
    #     self.InhA2.addItem("4")
    #     self.PAPPA2 = QtWidgets.QComboBox(self)
    #     self.PAPPA2.setGeometry(QtCore.QRect(160, 440, 100, 30))
    #     self.PAPPA2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    #                               "font: 12pt \"Arial\";")
    #     self.PAPPA2.setObjectName("PAPPA2")
    #     self.PAPPA2.addItem("1")
    #     self.PAPPA2.addItem("2")
    #     self.PAPPA2.addItem("3")
    #     self.PAPPA2.addItem("4")

    def data_padding_setting(self):
        data = self.connect.query_weight_parameters()
        for i in data:
            # 配置体重矫正参数ABCD
            if "TemplateForDowns_AFP_Earlyweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(1, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(1, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(1, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(1, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_hCG_Earlyweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(2, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(2, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(2, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(2, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_fbhCG_Earlyweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(3, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(3, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(3, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(3, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_uE3_Earlyweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(4, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(4, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(4, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(4, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_DIA_Earlyweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(5, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(5, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(5, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(5, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_PAPPA_Earlyweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(6, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(6, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(6, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(6, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_AFPweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(7, 2)
                    item.setText(str(i[1]))

                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(7, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(7, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(7, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_hCGweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(8, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(8, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(8, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(8, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_fbhCGweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(9, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(9, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(9, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(9, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_uE3weighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(10, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(10, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(10, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(10, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_DIAweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(11, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(11, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(11, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(11, 5)
                    item.setText(str(i[1]))
                    continue
            if "TemplateForDowns_PAPPAweighttformula" in i[0]:
                if i[0][-1:] == "a":
                    item = self.tableWidget.item(12, 2)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "b":
                    item = self.tableWidget.item(12, 3)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "c":
                    item = self.tableWidget.item(12, 4)
                    item.setText(str(i[1]))
                    continue
                if i[0][-1:] == "d":
                    item = self.tableWidget.item(12, 5)
                    item.setText(str(i[1]))
                    continue
            # 配置体重校正类型
            if "TemplateForDowns_AFP_Earlyweighttype" in i[0]:
                item = self.tableWidget.item(1, 1)
                item.setText(i[1])
                # self.AFP1.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_hCG_Earlyweighttype" in i[0]:
                item = self.tableWidget.item(2, 1)
                item.setText(i[1])
                # self.hCG1.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_fbhCG_Earlyweighttype" in i[0]:
                item = self.tableWidget.item(3, 1)
                item.setText(i[1])
                # self.fbhCG1.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_uE3_Earlyweighttype" in i[0]:
                item = self.tableWidget.item(4, 1)
                item.setText(i[1])
                # self.uE31.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_DIA_Earlyweighttype" in i[0]:
                item = self.tableWidget.item(5, 1)
                item.setText(i[1])
                # self.InhA1.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_PAPPA_Earlyweighttype" in i[0]:
                item = self.tableWidget.item(6, 1)
                item.setText(i[1])
                # self.PAPPA1.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_AFPweighttype" in i[0]:
                item = self.tableWidget.item(7, 1)
                item.setText(i[1])
                # self.AFP2.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_hCGweighttype" in i[0]:
                item = self.tableWidget.item(8, 1)
                item.setText(i[1])
                # self.hCG2.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_fbhCGweighttype" in i[0]:
                item = self.tableWidget.item(9, 1)
                item.setText(i[1])
                # self.fbhCG2.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_uE3weighttype" in i[0]:
                item = self.tableWidget.item(10, 1)
                item.setText(i[1])
                # self.AFP2.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_DIAweighttype" in i[0]:
                item = self.tableWidget.item(11, 1)
                item.setText(i[1])
                # self.InhA2.setCurrentIndex(int(i[1])-1)
                continue
            if "TemplateForDowns_PAPPAweighttype" in i[0]:
                item = self.tableWidget.item(12, 1)
                item.setText(i[1])
                # self.PAPPA2.setCurrentIndex(int(i[1])-1)
                continue



if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_win = UiWeight()

    main_win.show()
    sys.exit(app.exec_())
