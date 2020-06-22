from PyQt5.QtWidgets import *
from pages import Main_windows
import sys


# 显示数据库设置页面
def ui_database():
	main_win.show_database()


# 显示中位数设置页面
def ui_median():
	main_win.show_median()


# 显示体重校正参数页面
def ui_weight():
	main_win.show_weight()


# 显示多线程设置界面
def ui_multithreading():
	main_win.show_multithreading()


# 主程序入口
if __name__ == "__main__":

	app = QApplication(sys.argv)
	# 创建主窗口类
	main_win = Main_windows.UiMainWindow()
	main_win.calculate_sucess.hide()
	# 数据库按钮设置事件
	main_win.database_setting.clicked.connect(ui_database)
	# 中位数版本选择按钮设置事件
	main_win.median_setting.clicked.connect(ui_median)
	# 体重校正参数设置
	main_win.weight_setting.clicked.connect(ui_weight)
	# 多线程设置
	main_win.multithreading_setting.clicked.connect(ui_multithreading)

	main_win.show()
	sys.exit(app.exec_())
