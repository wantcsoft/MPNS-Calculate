# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
import configparser


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
        self.out_put_button()
        self.in_put_button()
        # self.select_box_setting()
        self.connect = None
        QtCore.QMetaObject.connectSlotsByName(self)

    # 最下边的计算公式
    def prompt_message_setting(self):
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 500, 500, 100))
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setPlainText("1:mom=result/median/10^(A-B*weight)\n"
                                        "2:mom=result/median/(A+B/weight)\n"
                                        "3:mom=result/median/10^(A*weight^2-B*weight+C)\n"
                                        "4:mom=result/median")
        self.plainTextEdit.setEnabled(False)

    # 表格的大小位置表头设置
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

    # 表格的数据填充
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

    # 导出体重校正参数设置
    def out_put_button(self):
        self.out_button = QtWidgets.QPushButton(self)
        self.out_button.setGeometry(QtCore.QRect(555, 520, 100, 50))
        self.out_button.setObjectName("out_button")
        self.out_button.setText("导出")
        self.out_button.clicked.connect(self.out_put_setting)

    # 导入体重校正参数设置
    def in_put_button(self):
        self.in_button = QtWidgets.QPushButton(self)
        self.in_button.setGeometry(QtCore.QRect(690, 520, 100, 50))
        self.in_button.setObjectName("in_button")
        self.in_button.setText("导入")
        self.in_button.clicked.connect(self.in_put_setting)

    # 当点击导出按钮之后
    def out_put_setting(self):
        fileName, fileType = QFileDialog.getSaveFileName(None, "文件保存", "D:/", "Text Files (*.ini);")
        config = configparser.ConfigParser()
        config['AFP1'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(1, 2).text(),
                          'B': self.tableWidget.item(1, 3).text(),
                          'C': self.tableWidget.item(1, 4).text(),
                          'D': self.tableWidget.item(1, 5).text()}
        config['hCG1'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(2, 2).text(),
                          'B': self.tableWidget.item(2, 3).text(),
                          'C': self.tableWidget.item(2, 4).text(),
                          'D': self.tableWidget.item(2, 5).text()}
        config['fbhCG1'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(3, 2).text(),
                          'B': self.tableWidget.item(3, 3).text(),
                          'C': self.tableWidget.item(3, 4).text(),
                          'D': self.tableWidget.item(3, 5).text()}
        config['uE31'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(4, 2).text(),
                          'B': self.tableWidget.item(4, 3).text(),
                          'C': self.tableWidget.item(4, 4).text(),
                          'D': self.tableWidget.item(4, 5).text()}
        config['InhA1'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(5, 2).text(),
                          'B': self.tableWidget.item(5, 3).text(),
                          'C': self.tableWidget.item(5, 4).text(),
                          'D': self.tableWidget.item(5, 5).text()}
        config['PAPPA1'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(6, 2).text(),
                          'B': self.tableWidget.item(6, 3).text(),
                          'C': self.tableWidget.item(6, 4).text(),
                          'D': self.tableWidget.item(6, 5).text()}
        config['AFP2'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(7, 2).text(),
                          'B': self.tableWidget.item(7, 3).text(),
                          'C': self.tableWidget.item(7, 4).text(),
                          'D': self.tableWidget.item(7, 5).text()}
        config['hCG2'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(8, 2).text(),
                          'B': self.tableWidget.item(8, 3).text(),
                          'C': self.tableWidget.item(8, 4).text(),
                          'D': self.tableWidget.item(8, 5).text()}
        config['fbhCG2'] = {'type': self.tableWidget.item(1, 1).text(),
                            'A': self.tableWidget.item(9, 2).text(),
                            'B': self.tableWidget.item(9, 3).text(),
                            'C': self.tableWidget.item(9, 4).text(),
                            'D': self.tableWidget.item(9, 5).text()}
        config['uE32'] = {'type': self.tableWidget.item(1, 1).text(),
                          'A': self.tableWidget.item(10, 2).text(),
                          'B': self.tableWidget.item(10, 3).text(),
                          'C': self.tableWidget.item(10, 4).text(),
                          'D': self.tableWidget.item(10, 5).text()}
        config['InhA2'] = {'type': self.tableWidget.item(1, 1).text(),
                           'A': self.tableWidget.item(11, 2).text(),
                           'B': self.tableWidget.item(11, 3).text(),
                           'C': self.tableWidget.item(11, 4).text(),
                           'D': self.tableWidget.item(11, 5).text()}
        config['PAPPA2'] = {'type': self.tableWidget.item(1, 1).text(),
                            'A': self.tableWidget.item(12, 2).text(),
                            'B': self.tableWidget.item(12, 3).text(),
                            'C': self.tableWidget.item(12, 4).text(),
                            'D': self.tableWidget.item(12, 5).text()}
        with open(fileName, 'w') as configfile:
            config.write(configfile)
        configfile.close()

    # 当点击导入按钮之后
    def in_put_setting(self):
        fileName, fileType = QFileDialog.getOpenFileName(None, "打开文件", "D:\\", "Text Files (*.ini);")
        config = configparser.ConfigParser()
        config.read(fileName)
        item = self.tableWidget.item(1, 1)
        item.setText(config['AFP1']["type"])
        item = self.tableWidget.item(1, 2)
        item.setText(config['AFP1']["A"])
        item = self.tableWidget.item(1, 3)
        item.setText(config['AFP1']["B"])
        item = self.tableWidget.item(1, 4)
        item.setText(config['AFP1']["C"])
        item = self.tableWidget.item(1, 5)
        item.setText(config['AFP1']["D"])

        item = self.tableWidget.item(2, 1)
        item.setText(config['hCG1']["type"])
        item = self.tableWidget.item(2, 2)
        item.setText(config['hCG1']["A"])
        item = self.tableWidget.item(2, 3)
        item.setText(config['hCG1']["B"])
        item = self.tableWidget.item(2, 4)
        item.setText(config['hCG1']["C"])
        item = self.tableWidget.item(2, 5)
        item.setText(config['hCG1']["D"])

        item = self.tableWidget.item(3, 1)
        item.setText(config['fbhCG1']["type"])
        item = self.tableWidget.item(3, 2)
        item.setText(config['fbhCG1']["A"])
        item = self.tableWidget.item(3, 3)
        item.setText(config['fbhCG1']["B"])
        item = self.tableWidget.item(3, 4)
        item.setText(config['fbhCG1']["C"])
        item = self.tableWidget.item(3, 5)
        item.setText(config['fbhCG1']["D"])

        item = self.tableWidget.item(4, 1)
        item.setText(config['uE31']["type"])
        item = self.tableWidget.item(4, 2)
        item.setText(config['uE31']["A"])
        item = self.tableWidget.item(4, 3)
        item.setText(config['uE31']["B"])
        item = self.tableWidget.item(4, 4)
        item.setText(config['uE31']["C"])
        item = self.tableWidget.item(4, 5)
        item.setText(config['uE31']["D"])

        item = self.tableWidget.item(5, 1)
        item.setText(config['InhA1']["type"])
        item = self.tableWidget.item(5, 2)
        item.setText(config['InhA1']["A"])
        item = self.tableWidget.item(5, 3)
        item.setText(config['InhA1']["B"])
        item = self.tableWidget.item(5, 4)
        item.setText(config['InhA1']["C"])
        item = self.tableWidget.item(5, 5)
        item.setText(config['InhA1']["D"])

        item = self.tableWidget.item(6, 1)
        item.setText(config['PAPPA1']["type"])
        item = self.tableWidget.item(6, 2)
        item.setText(config['PAPPA1']["A"])
        item = self.tableWidget.item(6, 3)
        item.setText(config['PAPPA1']["B"])
        item = self.tableWidget.item(6, 4)
        item.setText(config['PAPPA1']["C"])
        item = self.tableWidget.item(6, 5)
        item.setText(config['PAPPA1']["D"])

        item = self.tableWidget.item(7, 1)
        item.setText(config['AFP2']["type"])
        item = self.tableWidget.item(7, 2)
        item.setText(config['AFP2']["A"])
        item = self.tableWidget.item(7, 3)
        item.setText(config['AFP2']["B"])
        item = self.tableWidget.item(7, 4)
        item.setText(config['AFP2']["C"])
        item = self.tableWidget.item(7, 5)
        item.setText(config['AFP2']["D"])

        item = self.tableWidget.item(8, 1)
        item.setText(config['hCG2']["type"])
        item = self.tableWidget.item(8, 2)
        item.setText(config['hCG2']["A"])
        item = self.tableWidget.item(8, 3)
        item.setText(config['hCG2']["B"])
        item = self.tableWidget.item(8, 4)
        item.setText(config['hCG2']["C"])
        item = self.tableWidget.item(8, 5)
        item.setText(config['hCG2']["D"])

        item = self.tableWidget.item(9, 1)
        item.setText(config['fbhCG2']["type"])
        item = self.tableWidget.item(9, 2)
        item.setText(config['fbhCG2']["A"])
        item = self.tableWidget.item(9, 3)
        item.setText(config['fbhCG2']["B"])
        item = self.tableWidget.item(9, 4)
        item.setText(config['fbhCG2']["C"])
        item = self.tableWidget.item(9, 5)
        item.setText(config['fbhCG2']["D"])

        item = self.tableWidget.item(10, 1)
        item.setText(config['uE32']["type"])
        item = self.tableWidget.item(10, 2)
        item.setText(config['uE32']["A"])
        item = self.tableWidget.item(10, 3)
        item.setText(config['uE32']["B"])
        item = self.tableWidget.item(10, 4)
        item.setText(config['uE32']["C"])
        item = self.tableWidget.item(10, 5)
        item.setText(config['uE32']["D"])

        item = self.tableWidget.item(11, 1)
        item.setText(config['InhA2']["type"])
        item = self.tableWidget.item(11, 2)
        item.setText(config['InhA2']["A"])
        item = self.tableWidget.item(11, 3)
        item.setText(config['InhA2']["B"])
        item = self.tableWidget.item(11, 4)
        item.setText(config['InhA2']["C"])
        item = self.tableWidget.item(11, 5)
        item.setText(config['InhA2']["D"])

        item = self.tableWidget.item(12, 1)
        item.setText(config['PAPPA2']["type"])
        item = self.tableWidget.item(12, 2)
        item.setText(config['PAPPA2']["A"])
        item = self.tableWidget.item(12, 3)
        item.setText(config['PAPPA2']["B"])
        item = self.tableWidget.item(12, 4)
        item.setText(config['PAPPA2']["C"])
        item = self.tableWidget.item(12, 5)
        item.setText(config['PAPPA2']["D"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = UiWeight()

    main_win.show()
    sys.exit(app.exec_())
