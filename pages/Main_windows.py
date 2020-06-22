# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
from pages import Median_dialog, Database_dialog, Warning_database, Warning_median, Weight_dialog, Multithreading_dialog
from dataCalculation import MultiThreading, LoggerFile

logger = LoggerFile.MyLog()


class UiMainWindow(QMainWindow):

    # 主窗口初始化
    def __init__(self):
        super().__init__()
        self.main_database_connect_flag = False
        self.main_median_flag = False
        self.median_config = {}
        self.main_weight_flag = False
        self.weight_config = {}
        self.calculate_state = 0
        self.error_count = 0
        self.setObjectName("MainWindow")
        self.main_window_setting()
        # 创建一个数据库设置页面
        self.ui_database = Database_dialog.UiDatabase()
        # 创建一个中位数设置界面
        self.ui_median = Median_dialog.UiMedian()
        # 创建一个体重校正参数设置界面
        self.ui_weight = Weight_dialog.UiWeight()
        # 创建一个配置数据库提示
        self.ui_warning_database = Warning_database.UiWarningDatabase()
        # 创建一个配置中位数提示
        self.ui_warning_median = Warning_median.UiWarningMedian()
        # 创建一个多线程选择界面
        self.ui_multithreading = Multithreading_dialog.UiMultithreading()

        self.database_button_setting()
        self.database_prompt_setting()
        self.weight_button_setting()
        self.label_workflow_sign_setting()
        self.label_setting()
        self.lable_exception_setting()
        self.calculate_sucess_setting()
        self.lable_start_time_setting()
        self.lable_complete_time_setting()
        self.lable_left_time_setting()
        self.lable_spend_time_setting()
        self.time_setting()
        self.calculate_button_setting()
        self.check_error_button_setting()
        self.multithreading_button_setting()
        self.progressBar_setting()
        self.workflow_setting()
        self.prompt_setting()
        self.title_setting()
        self.median_button_setting()
        self.enable_median_setting()
        self.enable_weight_setting()
        self.page_count_setting()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    # 组件命名
    def retranslateUi(self):
        self.setWindowTitle("Form")
        self.radioButton.setText("早期或者中期两个都在范围内")
        self.radioButton_2.setText("早期或中期只需一个在范围内")

        self.setWindowTitle("MPNS_Batch_Calculation")
        self.database_setting.setText("数据库设置")
        self.database_prompt.setText("数据库未连接")
        self.median_setting.setText("中位数设置")
        self.weight_setting.setText("体重校正参数设置")
        self.multithreading_setting.setText("多线程设置")
        # 中位数配置启用
        self.checkBox_median.setText("启用中位数")
        self.checkBox_weight.setText("启用体重校正参数")

        self.prompt.setText("本软件仅供科研使用")
        self.title.setText("MPNS批量计算工具")
        self.label.setText("测试日期范围")
        self.label_workflow_sign.setText("筛查流程状态选择")
        self.no_risk.setText("尚未生成风险(数据库有拼串)")
        self.have_risk.setText("已生成风险，待提交")
        self.to_check.setText("已提交审核，待审核")
        self.have_check.setText("已审核通过")

        self.calculate.setText("开始计算")
        self.check_error.setText("查看")
        self.lable_total.setText("筛查方案数量：0例")
        self.progressBar.setText("计算进度：还剩 0 例")
        self.lable_exception.setText("异常数量：0例")
        self.lable_start_time.setText("计算开始时间：")
        self.lable_complete_time.setText("预估完成时间：")
        self.lable_left_time.setText("剩余时间：")
        self.lable_spend_time.setText("本次计算用时：")
        self.calculate_sucess.setText("计算完成")

    # 主窗口设置
    def main_window_setting(self):
        # 主窗口设置
        self.resize(1200, 700)
        self.setMinimumSize(QtCore.QSize(1200, 700))
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setMouseTracking(False)
        self.setWindowOpacity(1.0)
        self.setToolTipDuration(0)
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setAutoFillBackground(True)
        self.setAnimated(False)

    # 数据库设置按钮
    def database_button_setting(self):
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setObjectName("centralwidget")
        self.database_setting = QtWidgets.QPushButton(self.centralwidget)
        self.database_setting.setGeometry(QtCore.QRect(100, 100, 180, 50))
        self.database_setting.setObjectName("database_setting")

    # 数据库连接信息
    def database_prompt_setting(self):
        self.database_prompt = QtWidgets.QLabel(self.centralwidget)
        self.database_prompt.setGeometry(QtCore.QRect(130, 150, 180, 50))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.database_prompt.setFont(font)
        self.database_prompt.setStyleSheet("color: rgb(255, 0, 0);")
        self.database_prompt.setObjectName("database_prompt")

    # 中位数按钮设置
    def median_button_setting(self):
        # 中位数设置按钮
        self.median_setting = QtWidgets.QPushButton(self.centralwidget)
        self.median_setting.setGeometry(QtCore.QRect(300, 100, 180, 50))
        self.median_setting.setObjectName("median_setting")

    # 体重矫正参数按钮设置
    def weight_button_setting(self):
        # 体重校正参数设置按钮
        self.weight_setting = QtWidgets.QPushButton(self.centralwidget)
        self.weight_setting.setGeometry(QtCore.QRect(500, 100, 180, 50))
        self.weight_setting.setObjectName("weight_setting")

    # 多线程按钮设置
    def multithreading_button_setting(self):
        # 多线程设置按钮
        self.multithreading_setting = QtWidgets.QPushButton(self.centralwidget)
        self.multithreading_setting.setGeometry(QtCore.QRect(700, 100, 180, 50))
        self.multithreading_setting.setObjectName("multithreading_setting")

    # 设置计算按钮位置大小
    def calculate_button_setting(self):
        # 计算按钮
        self.calculate = QtWidgets.QPushButton(self.centralwidget)
        self.calculate.setGeometry(QtCore.QRect(900, 100, 180, 50))
        self.calculate.setObjectName("calculate")
        self.calculate.clicked.connect(self.calculate_start)

    # 中位数配置启用按钮
    def enable_median_setting(self):
        self.checkBox_median = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_median.setGeometry(QtCore.QRect(300, 150, 120, 50))
        self.checkBox_median.setObjectName("checkBox_median")
        self.checkBox_median.toggled.connect(self.get_median_config)
    
    # 体重校正参数配置启用按钮
    def enable_weight_setting(self):
        self.checkBox_weight = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_weight.setGeometry(QtCore.QRect(500, 150, 180, 50))
        self.checkBox_weight.setObjectName("checkBox_weight")
        self.checkBox_weight.toggled.connect(self.get_weight_config)

    # 软件仅供科研使用
    def prompt_setting(self):
        # 软件仅供科研使用
        self.prompt = QtWidgets.QLabel(self.centralwidget)
        self.prompt.setGeometry(QtCore.QRect(480, 60, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.prompt.setFont(font)
        self.prompt.setStyleSheet("color: rgb(255, 0, 0);")
        self.prompt.setObjectName("prompt")  # 软件仅供科研使用

    # 标题设置
    def title_setting(self):
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(380, 0, 700, 60))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")

    # 一筛查流程状态选择
    def label_workflow_sign_setting(self):
        self.label_workflow_sign = QtWidgets.QLabel(self.centralwidget)
        self.label_workflow_sign.setGeometry(QtCore.QRect(600, 180, 300, 80))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_workflow_sign.setFont(font)

    # 测试日期范围
    def label_setting(self):
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 180, 300, 80))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)

    # 计算进度
    def progressBar_setting(self):
        # 进度条设置
        self.progressBar = QtWidgets.QLabel(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(100, 470, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.progressBar.setFont(font)
        self.progressBar.setObjectName("progressBar")

    # 工作流状态
    def workflow_setting(self):
        # 设置工作流程的位置
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(600, 240, 400, 180))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # 工作流状态
        self.no_risk = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.no_risk.setObjectName("no_risk")
        self.no_risk.click()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.no_risk.setFont(font)
        self.verticalLayout.addWidget(self.no_risk)
        self.have_risk = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.have_risk.setObjectName("have_risk")
        self.have_risk.click()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.have_risk.setFont(font)
        self.verticalLayout.addWidget(self.have_risk)
        self.to_check = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.to_check.setObjectName("to_check")
        self.to_check.click()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.to_check.setFont(font)
        self.verticalLayout.addWidget(self.to_check)
        self.have_check = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.have_check.setObjectName("have_check")
        self.have_check.click()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.have_check.setFont(font)
        self.verticalLayout.addWidget(self.have_check)

    # 开始时间结束时间设置
    def time_setting(self):
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(100, 240, 320, 180))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        # # 开始时间结束时间设置
        self.dateEdit = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDate(QDate.currentDate())
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dateEdit.setFont(font)
        self.verticalLayout.addWidget(self.dateEdit)

        self.dateEdit_2 = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.dateEdit_2.setDate(QDate.currentDate())
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dateEdit_2.setFont(font)
        self.verticalLayout.addWidget(self.dateEdit_2)

        self.radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.click()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioButton.setFont(font)
        self.verticalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName("have_check")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioButton_2.setFont(font)
        self.verticalLayout.addWidget(self.radioButton_2)

    # 数据总数文字显示
    def page_count_setting(self):
        # 筛选数据总数量
        self.lable_total = QtWidgets.QLabel(self.centralwidget)
        self.lable_total.setGeometry(QtCore.QRect(100, 420, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lable_total.setFont(font)
        self.lable_total.setObjectName("lable_total")

    # 计算异常总数量数据总数文字显示
    def lable_exception_setting(self):
        # 筛选数据总数量
        self.lable_exception = QtWidgets.QLabel(self.centralwidget)
        self.lable_exception.setGeometry(QtCore.QRect(100, 520, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lable_exception.setFont(font)
        self.lable_exception.setObjectName("lable_exception")

    # 计算开始时间
    def lable_start_time_setting(self):
        # 筛选数据总数量
        self.lable_start_time = QtWidgets.QLabel(self.centralwidget)
        self.lable_start_time.setGeometry(QtCore.QRect(600, 420, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lable_start_time.setFont(font)
        self.lable_start_time.setObjectName("lable_start_time")

    # 预估完成时间
    def lable_complete_time_setting(self):
        # 筛选数据总数量
        self.lable_complete_time = QtWidgets.QLabel(self.centralwidget)
        self.lable_complete_time.setGeometry(QtCore.QRect(600, 470, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lable_complete_time.setFont(font)
        self.lable_complete_time.setObjectName("lable_complete_time")

    # 计算剩余时间
    def lable_left_time_setting(self):
        self.lable_left_time = QtWidgets.QLabel(self.centralwidget)
        self.lable_left_time.setGeometry(QtCore.QRect(600, 520, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lable_left_time.setFont(font)
        self.lable_left_time.setObjectName("lable_left_time")

    # 总共花费时间时间
    def lable_spend_time_setting(self):
        self.lable_spend_time = QtWidgets.QLabel(self.centralwidget)
        self.lable_spend_time.setGeometry(QtCore.QRect(600, 570, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lable_spend_time.setFont(font)
        self.lable_spend_time.setObjectName("lable_spend_time")

    # 计算完成
    def calculate_sucess_setting(self):
        # 筛选数据总数量
        self.calculate_sucess = QtWidgets.QLabel(self.centralwidget)
        self.calculate_sucess.setGeometry(QtCore.QRect(510, 620, 180, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.calculate_sucess.setFont(font)
        self.calculate_sucess.setStyleSheet("color: rgb(255, 0, 0);")
        self.calculate_sucess.setObjectName("calculate_sucess")

    # 设置查看异常按钮位置大小
    def check_error_button_setting(self):
        # 计算按钮
        self.check_error = QtWidgets.QPushButton(self.centralwidget)
        self.check_error.setGeometry(QtCore.QRect(350, 530, 80, 30))
        self.check_error.setObjectName("check_error")
        self.check_error.clicked.connect(self.check_error_start)

    # 查看异常按钮点击之后
    def check_error_start(self):
        if self.error_count > 0:
            file_path = LoggerFile.error_path
            os.startfile(file_path)

    # 计算按钮点击之后
    def calculate_start(self):
        self.calculate_sucess.hide()
        self.progressBar.setProperty("value", 0)
        if not self.main_database_connect_flag:
            self.ui_warning_database.setWindowModality(Qt.ApplicationModal)
            self.ui_warning_database.exec_()
        elif not self.main_median_flag and not self.main_weight_flag:
            self.ui_warning_median.setWindowModality(Qt.ApplicationModal)
            self.ui_warning_median.exec_()
        else:
            # 设置任务开始时间
            verify_workflow = self.get_workflow_state()
            if self.dateEdit.date() == self.dateEdit_2.date():
                count = self.connect.query_workflow_count(verify_workflow.__str__())[0][0]
                self.lable_total.setText("筛查方案数量：%s" % count)
                if count > 0:
                    # 开始计算时其他控件无法使用
                    self.setEnabled(False)
                    self.lable_start_time.setText("计算开始时间：%s" %
                                                  time.strftime('%Y-%m-%d %H:%M:%S',
                                                                time.localtime(time.time())))
                    data_list = self.connect.query_workflow(verify_workflow.__str__())
                    thread = MultiThreading.MultiThreading(self, data_list, count)
                    thread.start()
            else:
                if self.dateEdit_2.date() > self.dateEdit.date():
                    end = self.dateEdit_2.date().getDate()
                    start = self.dateEdit.date().getDate()
                else:
                    start = self.dateEdit_2.date().getDate()
                    end = self.dateEdit.date().getDate()
                start_time = "%d-%d-%d 00:00:00" % (start[0], start[1], start[2])
                end_time = "%d-%d-%d 00:00:00" % (end[0], end[1], end[2])
                # 两个都在日期范围内
                if self.radioButton.isChecked():
                    count_one = self.connect.query_one_time_workflow_count(start_time,
                                                                           end_time,
                                                                           verify_workflow.__str__())[0][0]
                    count_two = self.connect.query_two_time_workflow_all_count(start_time,
                                                                               end_time,
                                                                               verify_workflow.__str__())[0][0]
                    self.lable_total.setText("筛查方案数量：%s" % (count_one + count_two))
                    if (count_one + count_two) > 0:
                        # 开始计算时其他控件无法使用
                        self.setEnabled(False)
                        self.lable_start_time.setText("计算开始时间：%s" %
                                                      time.strftime('%Y-%m-%d %H:%M:%S',
                                                                    time.localtime(time.time())))
                        data_list = self.connect.query_time_workflow_all(start_time,
                                                                         end_time,
                                                                         verify_workflow.__str__())
                        thread = MultiThreading.MultiThreading(self, data_list, count_one+count_two)
                        thread.start()
                # 只需要一个在范围内
                else:
                    count_one = self.connect.query_one_time_workflow_count(start_time,
                                                                           end_time,
                                                                           verify_workflow.__str__())[0][0]
                    count_two = self.connect.query_two_time_workflow_any_count(start_time,
                                                                               end_time,
                                                                               verify_workflow.__str__())[0][0]
                    self.lable_total.setText("筛查方案数量：%s" % (count_one + count_two))
                    if (count_one + count_two) > 0:
                        # 开始计算时其他控件无法使用
                        self.setEnabled(False)
                        self.lable_start_time.setText("计算开始时间：%s" %
                                                      time.strftime('%Y-%m-%d %H:%M:%S',
                                                                    time.localtime(time.time())))
                        data_list = self.connect.query_time_workflow_any(start_time,
                                                                         end_time,
                                                                         verify_workflow.__str__())
                        thread = MultiThreading.MultiThreading(self, data_list, count_one+count_two)
                        thread.start()

    # 返回筛选流程的状态集合
    def get_workflow_state(self):
        list = []
        if self.no_risk.isChecked():
            list.append(0)
        if self.have_risk.isChecked():
            list.append(1)
        if self.to_check.isChecked():
            list.append(2)
        if self.have_check.isChecked():
            list.append(3)
        if len(list) == 0:
            return 0
        else:
            list.append(-1)
            return tuple(list)

    # 数据库连接成功
    def connect_sucess(self):
        self.database_prompt.setText("数据库已连接")
        self.ui_median.connect = self.ui_database.connect
        self.ui_weight.connect = self.ui_database.connect
        self.connect = self.ui_database.connect
        # 体重校正参数内容配置
        self.ui_weight.data_padding_setting()
        self.main_database_connect_flag = True
        # 数据库连接成功后清除中位数下拉框内容，重新加载
        box_list = self.ui_median.findChildren(QComboBox)
        for i in box_list:
            i.clear()
        # LMP页面数据填充
        self.ui_median.LMP_content_filling()
        # BPD页面数据填充
        self.ui_median.BPD_content_filling()
        # CRL页面数据填充
        self.ui_median.CRL_content_filling()
        # IVF页面数据填充
        self.ui_median.IVF_content_filling()
        # BC页面数据填充
        self.ui_median.BC_content_filling()
        self.ui_database.close()

    # 打开数据库设置窗口
    def show_database(self):
        # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        self.ui_database.setWindowModality(Qt.ApplicationModal)
        self.ui_database.sucess_button.clicked.connect(self.connect_sucess)
        self.ui_database.exec_()

    # 中位数是否配置完成,并且将中位数版本的选择保存起来
    def get_median_config(self):
        if self.checkBox_median.isChecked():
            dict_LMP = {}
            dict_LMP["1"] = 0 if self.ui_median.version_LMP_1.currentText() == "" else \
                self.ui_median.version_LMP_1.currentText().split("  ")[0]
            dict_LMP["2"] = 0 if self.ui_median.version_LMP_2.currentText() == "" else \
                self.ui_median.version_LMP_2.currentText().split("  ")[0]
            dict_LMP["3"] = 0 if self.ui_median.version_LMP_3.currentText() == "" else \
                self.ui_median.version_LMP_3.currentText().split("  ")[0]
            dict_LMP["4"] = 0 if self.ui_median.version_LMP_4.currentText() == "" else \
                self.ui_median.version_LMP_4.currentText().split("  ")[0]
            dict_LMP["5"] = 0 if self.ui_median.version_LMP_5.currentText() == "" else \
                self.ui_median.version_LMP_5.currentText().split("  ")[0]
            dict_LMP["6"] = 0 if self.ui_median.version_LMP_6.currentText() == "" else \
                self.ui_median.version_LMP_6.currentText().split("  ")[0]
            dict_LMP["7"] = 0 if self.ui_median.version_LMP_7.currentText() == "" else \
                self.ui_median.version_LMP_7.currentText().split("  ")[0]
            dict_LMP["8"] = 0 if self.ui_median.version_LMP_8.currentText() == "" else \
                self.ui_median.version_LMP_8.currentText().split("  ")[0]
            dict_LMP["9"] = 0 if self.ui_median.version_LMP_9.currentText() == "" else \
                self.ui_median.version_LMP_9.currentText().split("  ")[0]
            dict_LMP["10"] = 0 if self.ui_median.version_LMP_10.currentText() == "" else \
                self.ui_median.version_LMP_10.currentText().split("  ")[0]
            dict_LMP["11"] = 0 if self.ui_median.version_LMP_11.currentText() == "" else \
                self.ui_median.version_LMP_11.currentText().split("  ")[0]
            dict_LMP["12"] = 0 if self.ui_median.version_LMP_12.currentText() == "" else \
                self.ui_median.version_LMP_12.currentText().split("  ")[0]
            dict_LMP["13"] = 0 if self.ui_median.version_LMP_13.currentText() == "" else \
                self.ui_median.version_LMP_13.currentText().split("  ")[0]
            dict_BPD = {}
            dict_BPD["1"] = 0 if self.ui_median.version_BPD_1.currentText() == "" else \
                self.ui_median.version_BPD_1.currentText().split("  ")[0]
            dict_BPD["2"] = 0 if self.ui_median.version_BPD_2.currentText() == "" else \
                self.ui_median.version_BPD_2.currentText().split("  ")[0]
            dict_BPD["3"] = 0 if self.ui_median.version_BPD_3.currentText() == "" else \
                self.ui_median.version_BPD_3.currentText().split("  ")[0]
            dict_BPD["4"] = 0 if self.ui_median.version_BPD_4.currentText() == "" else \
                self.ui_median.version_BPD_4.currentText().split("  ")[0]
            dict_BPD["5"] = 0 if self.ui_median.version_BPD_5.currentText() == "" else \
                self.ui_median.version_BPD_5.currentText().split("  ")[0]
            dict_BPD["6"] = 0 if self.ui_median.version_BPD_6.currentText() == "" else \
                self.ui_median.version_BPD_6.currentText().split("  ")[0]
            dict_BPD["7"] = 0 if self.ui_median.version_BPD_7.currentText() == "" else \
                self.ui_median.version_BPD_7.currentText().split("  ")[0]
            dict_BPD["8"] = 0 if self.ui_median.version_BPD_8.currentText() == "" else \
                self.ui_median.version_BPD_8.currentText().split("  ")[0]
            dict_BPD["9"] = 0 if self.ui_median.version_BPD_9.currentText() == "" else \
                self.ui_median.version_BPD_9.currentText().split("  ")[0]
            dict_BPD["10"] = 0 if self.ui_median.version_BPD_10.currentText() == "" else \
                self.ui_median.version_BPD_10.currentText().split("  ")[0]
            dict_BPD["11"] = 0 if self.ui_median.version_BPD_11.currentText() == "" else \
                self.ui_median.version_BPD_11.currentText().split("  ")[0]
            dict_BPD["12"] = 0 if self.ui_median.version_BPD_12.currentText() == "" else \
                self.ui_median.version_BPD_12.currentText().split("  ")[0]
            dict_BPD["13"] = 0 if self.ui_median.version_BPD_13.currentText() == "" else \
                self.ui_median.version_BPD_13.currentText().split("  ")[0]
            dict_CRL = {}
            dict_CRL["1"] = 0 if self.ui_median.version_CRL_1.currentText() == "" else \
                self.ui_median.version_CRL_1.currentText().split("  ")[0]
            dict_CRL["2"] = 0 if self.ui_median.version_CRL_2.currentText() == "" else \
                self.ui_median.version_CRL_2.currentText().split("  ")[0]
            dict_CRL["3"] = 0 if self.ui_median.version_CRL_3.currentText() == "" else \
                self.ui_median.version_CRL_3.currentText().split("  ")[0]
            dict_CRL["4"] = 0 if self.ui_median.version_CRL_4.currentText() == "" else \
                self.ui_median.version_CRL_4.currentText().split("  ")[0]
            dict_CRL["5"] = 0 if self.ui_median.version_CRL_5.currentText() == "" else \
                self.ui_median.version_CRL_5.currentText().split("  ")[0]
            dict_CRL["6"] = 0 if self.ui_median.version_CRL_6.currentText() == "" else \
                self.ui_median.version_CRL_6.currentText().split("  ")[0]
            dict_CRL["7"] = 0 if self.ui_median.version_CRL_7.currentText() == "" else \
                self.ui_median.version_CRL_7.currentText().split("  ")[0]
            dict_CRL["8"] = 0 if self.ui_median.version_CRL_8.currentText() == "" else \
                self.ui_median.version_CRL_8.currentText().split("  ")[0]
            dict_CRL["9"] = 0 if self.ui_median.version_CRL_9.currentText() == "" else \
                self.ui_median.version_CRL_9.currentText().split("  ")[0]
            dict_CRL["10"] = 0 if self.ui_median.version_CRL_10.currentText() == "" else \
                self.ui_median.version_CRL_10.currentText().split("  ")[0]
            dict_CRL["11"] = 0 if self.ui_median.version_CRL_11.currentText() == "" else \
                self.ui_median.version_CRL_11.currentText().split("  ")[0]
            dict_CRL["12"] = 0 if self.ui_median.version_CRL_12.currentText() == "" else \
                self.ui_median.version_CRL_12.currentText().split("  ")[0]
            dict_CRL["13"] = 0 if self.ui_median.version_CRL_13.currentText() == "" else \
                self.ui_median.version_CRL_13.currentText().split("  ")[0]
            dict_IVF = {}
            dict_IVF["1"] = 0 if self.ui_median.version_IVF_1.currentText() == "" else \
                self.ui_median.version_IVF_1.currentText().split("  ")[0]
            dict_IVF["2"] = 0 if self.ui_median.version_IVF_2.currentText() == "" else \
                self.ui_median.version_IVF_2.currentText().split("  ")[0]
            dict_IVF["3"] = 0 if self.ui_median.version_IVF_3.currentText() == "" else \
                self.ui_median.version_IVF_3.currentText().split("  ")[0]
            dict_IVF["4"] = 0 if self.ui_median.version_IVF_4.currentText() == "" else \
                self.ui_median.version_IVF_4.currentText().split("  ")[0]
            dict_IVF["5"] = 0 if self.ui_median.version_IVF_5.currentText() == "" else \
                self.ui_median.version_IVF_5.currentText().split("  ")[0]
            dict_IVF["6"] = 0 if self.ui_median.version_IVF_6.currentText() == "" else \
                self.ui_median.version_IVF_6.currentText().split("  ")[0]
            dict_IVF["7"] = 0 if self.ui_median.version_IVF_7.currentText() == "" else \
                self.ui_median.version_IVF_7.currentText().split("  ")[0]
            dict_IVF["8"] = 0 if self.ui_median.version_IVF_8.currentText() == "" else \
                self.ui_median.version_IVF_8.currentText().split("  ")[0]
            dict_IVF["9"] = 0 if self.ui_median.version_IVF_9.currentText() == "" else \
                self.ui_median.version_IVF_9.currentText().split("  ")[0]
            dict_IVF["10"] = 0 if self.ui_median.version_IVF_10.currentText() == "" else \
                self.ui_median.version_IVF_10.currentText().split("  ")[0]
            dict_IVF["11"] = 0 if self.ui_median.version_IVF_11.currentText() == "" else \
                self.ui_median.version_IVF_11.currentText().split("  ")[0]
            dict_IVF["12"] = 0 if self.ui_median.version_IVF_12.currentText() == "" else \
                self.ui_median.version_IVF_12.currentText().split("  ")[0]
            dict_IVF["13"] = 0 if self.ui_median.version_IVF_13.currentText() == "" else \
                self.ui_median.version_IVF_13.currentText().split("  ")[0]
            dict_BC = {}
            dict_BC["1"] = 0 if self.ui_median.version_BC_1.currentText() == "" else \
                self.ui_median.version_BC_1.currentText().split("  ")[0]
            dict_BC["2"] = 0 if self.ui_median.version_BC_2.currentText() == "" else \
                self.ui_median.version_BC_2.currentText().split("  ")[0]
            dict_BC["3"] = 0 if self.ui_median.version_BC_3.currentText() == "" else \
                self.ui_median.version_BC_3.currentText().split("  ")[0]
            dict_BC["4"] = 0 if self.ui_median.version_BC_4.currentText() == "" else \
                self.ui_median.version_BC_4.currentText().split("  ")[0]
            dict_BC["5"] = 0 if self.ui_median.version_BC_5.currentText() == "" else \
                self.ui_median.version_BC_5.currentText().split("  ")[0]
            dict_BC["6"] = 0 if self.ui_median.version_BC_6.currentText() == "" else \
                self.ui_median.version_BC_6.currentText().split("  ")[0]
            dict_BC["7"] = 0 if self.ui_median.version_BC_7.currentText() == "" else \
                self.ui_median.version_BC_7.currentText().split("  ")[0]
            dict_BC["8"] = 0 if self.ui_median.version_BC_8.currentText() == "" else \
                self.ui_median.version_BC_8.currentText().split("  ")[0]
            dict_BC["9"] = 0 if self.ui_median.version_BC_9.currentText() == "" else \
                self.ui_median.version_BC_9.currentText().split("  ")[0]
            dict_BC["10"] = 0 if self.ui_median.version_BC_10.currentText() == "" else \
                self.ui_median.version_BC_10.currentText().split("  ")[0]
            dict_BC["11"] = 0 if self.ui_median.version_BC_11.currentText() == "" else \
                self.ui_median.version_BC_11.currentText().split("  ")[0]
            dict_BC["12"] = 0 if self.ui_median.version_BC_12.currentText() == "" else \
                self.ui_median.version_BC_12.currentText().split("  ")[0]
            dict_BC["13"] = 0 if self.ui_median.version_BC_13.currentText() == "" else \
                self.ui_median.version_BC_13.currentText().split("  ")[0]
            self.median_config = {"1": dict_LMP, "2": dict_BPD, "3": dict_CRL, "4": dict_IVF, "5": dict_BC}
            logger.info("选择的标记物版本设置 = %s" % self.median_config)
            self.main_median_flag = True
        else:
            self.median_config = {}
            self.main_median_flag = False
            logger.info("选择的标记物版本设置 = %s" % self.median_config)

    # 保存选择好的体重校正参数
    def get_weight_config(self):
        if self.checkBox_weight.isChecked():
            AFP1 = [self.ui_weight.AFP1.currentText(), self.ui_weight.tableWidget.item(1, 2).text(), self.ui_weight.tableWidget.item(1, 3).text(), self.ui_weight.tableWidget.item(1, 4).text(), self.ui_weight.tableWidget.item(1, 5).text()]
            hCG1 = [self.ui_weight.hCG1.currentText(), self.ui_weight.tableWidget.item(2, 2).text(), self.ui_weight.tableWidget.item(2, 3).text(), self.ui_weight.tableWidget.item(2, 4).text(), self.ui_weight.tableWidget.item(2, 5).text()]
            fbhCG1 = [self.ui_weight.fbhCG1.currentText(), self.ui_weight.tableWidget.item(3, 2).text(), self.ui_weight.tableWidget.item(3, 3).text(), self.ui_weight.tableWidget.item(3, 4).text(), self.ui_weight.tableWidget.item(3, 5).text()]
            uE31 = [self.ui_weight.uE31.currentText(), self.ui_weight.tableWidget.item(4, 2).text(), self.ui_weight.tableWidget.item(4, 3).text(), self.ui_weight.tableWidget.item(4, 4).text(), self.ui_weight.tableWidget.item(4, 5).text()]
            InhA1 = [self.ui_weight.InhA1.currentText(), self.ui_weight.tableWidget.item(5, 2).text(), self.ui_weight.tableWidget.item(5, 3).text(), self.ui_weight.tableWidget.item(5, 4).text(), self.ui_weight.tableWidget.item(5, 5).text()]
            PAPPA1 = [self.ui_weight.PAPPA1.currentText(), self.ui_weight.tableWidget.item(6, 2).text(), self.ui_weight.tableWidget.item(6, 3).text(), self.ui_weight.tableWidget.item(6, 4).text(), self.ui_weight.tableWidget.item(6, 5).text()]
            AFP2 = [self.ui_weight.AFP2.currentText(), self.ui_weight.tableWidget.item(7, 2).text(), self.ui_weight.tableWidget.item(7, 3).text(), self.ui_weight.tableWidget.item(7, 4).text(), self.ui_weight.tableWidget.item(7, 5).text()]
            hCG2 = [self.ui_weight.hCG2.currentText(), self.ui_weight.tableWidget.item(8, 2).text(), self.ui_weight.tableWidget.item(8, 3).text(), self.ui_weight.tableWidget.item(8, 4).text(), self.ui_weight.tableWidget.item(8, 5).text()]
            fbhCG2 = [self.ui_weight.fbhCG2.currentText(), self.ui_weight.tableWidget.item(9, 2).text(), self.ui_weight.tableWidget.item(9, 3).text(), self.ui_weight.tableWidget.item(9, 4).text(), self.ui_weight.tableWidget.item(9, 5).text()]
            uE32 = [self.ui_weight.uE32.currentText(), self.ui_weight.tableWidget.item(10, 2).text(), self.ui_weight.tableWidget.item(10, 3).text(), self.ui_weight.tableWidget.item(10, 4).text(), self.ui_weight.tableWidget.item(10, 5).text()]
            InhA2 = [self.ui_weight.InhA2.currentText(), self.ui_weight.tableWidget.item(11, 2).text(), self.ui_weight.tableWidget.item(11, 3).text(), self.ui_weight.tableWidget.item(11, 4).text(), self.ui_weight.tableWidget.item(11, 5).text()]
            PAPPA2 = [self.ui_weight.PAPPA2.currentText(), self.ui_weight.tableWidget.item(12, 2).text(), self.ui_weight.tableWidget.item(12, 3).text(), self.ui_weight.tableWidget.item(12, 4).text(), self.ui_weight.tableWidget.item(12, 5).text()]
            self.weight_config = {"AFP1": AFP1, "hCG1": hCG1, "fbhCG1": fbhCG1, "uE31": uE31, "InhA1": InhA1, "PAPPA1": PAPPA1, "AFP2": AFP2, "hCG2": hCG2, "fbhCG2": fbhCG2, "uE32": uE32, "InhA2": InhA2, "PAPPA2": PAPPA2}
            self.main_weight_flag = True
            logger.info("体重矫正参数设置 = %s" % self.weight_config)
        else:
            self.weight_config = {}
            self.main_weight_flag = False
            logger.info("体重矫正参数设置 = %s" % self.weight_config)

    # 打开中位数设置窗口
    def show_median(self):
        if not self.ui_database.database_connect_flag:
            self.ui_warning_database.setWindowModality(Qt.ApplicationModal)
            self.ui_warning_database.exec_()
        else:
            self.ui_median.setWindowModality(Qt.ApplicationModal)
            self.ui_median.exec_()

    # 打开体重校正参数设置窗口
    def show_weight(self):
        if not self.ui_database.database_connect_flag:
            self.ui_warning_database.setWindowModality(Qt.ApplicationModal)
            self.ui_warning_database.exec_()
        else:
            self.ui_weight.setWindowModality(Qt.ApplicationModal)
            self.ui_weight.exec_()

    def show_multithreading(self):
        self.ui_multithreading.setWindowModality(Qt.ApplicationModal)
        self.ui_multithreading.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = UiMainWindow()

    main_win.show()
    sys.exit(app.exec_())
