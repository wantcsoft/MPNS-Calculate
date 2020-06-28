# -*- coding: utf-8 -*-
import json
import sys
from sqlServer import QueryData
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from dataCalculation import LoggerFile

logger = LoggerFile.MyLog()


class UiDatabase(QDialog):

    # 数据库设置界面初始化
    def	__init__(self):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(600, 530)
        self.setMinimumSize(QtCore.QSize(600, 530))
        self.setMaximumSize(QtCore.QSize(600, 530))
        self.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(100, 100, 400, 600))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 19, 0, 10)
        self.formLayout.setVerticalSpacing(19)
        self.formLayout.setObjectName("formLayout")
        self.database_connect_flag = False

        self.database_server_setting()
        self.database_name_setting()
        self.username_setting()
        self.password_setting()
        self.test_button_setting()
        self.result_button_setting()
        self.retranslateUi()
        self.set_default_value()
        QtCore.QMetaObject.connectSlotsByName(self)

    #组件创建命名
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "数据库设置"))
        self.server_lable.setText(_translate("Dialog", "服务器："))
        self.database_name_label.setText(_translate("Dialog", "数据库名："))
        self.user_name_label.setText(_translate("Dialog", "用户名："))
        self.user_password_label.setText(_translate("Dialog", "用户密码："))
        self.test_button.setText(_translate("Dialog", "连接测试"))
        self.sucess_button.setText(_translate("Dialog", "成功"))

    #数据库服务设置
    def database_server_setting(self):
        self.server_lable = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.server_lable.setFont(font)
        self.server_lable.setObjectName("server_lable")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.server_lable)
        self.server_lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.server_lineEdit.setObjectName("server_lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.server_lineEdit)

    #数据库名设置
    def database_name_setting(self):
        self.database_name_label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.database_name_label.setFont(font)
        self.database_name_label.setObjectName("database_name_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.database_name_label)
        self.database_name_lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.database_name_lineEdit.setObjectName("database_name_lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.database_name_lineEdit)

    #用户名设置
    def username_setting(self):
        self.user_name_label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.user_name_label.setFont(font)
        self.user_name_label.setObjectName("user_name_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.user_name_label)
        self.user_name_lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.user_name_lineEdit.setObjectName("user_name_lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.user_name_lineEdit)

    #密码输入设置
    def password_setting(self):
        self.user_password_label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.user_password_label.setFont(font)
        self.user_password_label.setObjectName("user_password_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.user_password_label)
        self.user_password_lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.user_password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.user_password_lineEdit.setObjectName("user_password_lineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.user_password_lineEdit)

    #数据库测试按钮
    def test_button_setting(self):
        self.test_button = QtWidgets.QPushButton(self)
        self.test_button.setGeometry(QtCore.QRect(250, 400, 100, 30))
        self.test_button.setObjectName("test_button")
        self.test_button.clicked.connect(self.database_login)

        self.sucess_button = QtWidgets.QPushButton(self)
        self.sucess_button.setGeometry(QtCore.QRect(250, 500, 100, 30))
        self.sucess_button.hide()

    #数据库连接结果显示
    def result_button_setting(self):
        self.result_label = QtWidgets.QLabel(self)
        self.result_label.setGeometry(QtCore.QRect(260, 450, 100, 30))
        # self.result_label.setText("连接成功")
        self.result_label.setStyleSheet("color: rgb(255, 0, 0);")
        self.result_label.setObjectName("result_label")

    #从json文件读取数值并设置
    def set_default_value(self):
        with open("./database.json", 'r') as data_base:
            setting = json.load(data_base)
            self.server_lineEdit.setText(setting["server"])
            self.database_name_lineEdit.setText(setting["databaseName"])
            self.user_name_lineEdit.setText(setting["user"])
            self.user_password_lineEdit.setText(setting["password"])
        data_base.close()

    #数据库登录
    def database_login(self):
        self.connect = QueryData.QueryData()
        result = self.connect.connect("{SQL Server}",
                             self.server_lineEdit.text(),
                             self.database_name_lineEdit.text(),
                             self.user_name_lineEdit.text(),
                             self.user_password_lineEdit.text())
        logger.info("驱动 = {SQL Server}， server = %s, database_name = %s, "
                    "user_name = %s, password = %s" % (self.server_lineEdit.text(),
                     self.database_name_lineEdit.text(),self.user_name_lineEdit.text(),
                     self.user_password_lineEdit.text()))
        if result == "链接成功":
            logger.info("数据库登陆成功！")
            #将配置保存进json文件中
            load_dict = {"driver" : "{SQL Server}",
                         "server": self.server_lineEdit.text(),
                         "databaseName": self.database_name_lineEdit.text(),
                         "user": self.user_name_lineEdit.text(),
                         "password": self.user_password_lineEdit.text()
                         }
            with open("./database.json", 'w') as dump_f:
                json.dump(load_dict, dump_f)
            dump_f.close()
            logger.info("数据库连接成功, server = %s, databaseName = %s, user = %s, password = %s"
                         % (self.server_lineEdit.text(), self.database_name_lineEdit.text(),
                            self.user_name_lineEdit.text(), self.user_password_lineEdit.text()))
            self.sucess_button.click()
            self.database_connect_flag = True
        else:
            logger.debug("数据库连接失败, server = %s, databaseName = %s, user = %s, password = %s"
                        % (self.server_lineEdit.text(), self.database_name_lineEdit.text(),
                           self.user_name_lineEdit.text(), self.user_password_lineEdit.text()))
            self.result_label.setText("连接失败")
            self.database_connect_flag = False


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_win = UiDatabase()

    main_win.show()
    sys.exit(app.exec_())