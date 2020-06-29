from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
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
	try:
		app = QApplication(sys.argv)
		serverName = 'testServer'
		socket = QLocalSocket()
		socket.connectToServer(serverName)
		# 如果连接成功，表明server已经存在，当前已有实例在运行
		if socket.waitForConnected(500):
			app.quit()
		else:
			localServer = QLocalServer()  # 没有实例运行，创建服务器
			localServer.listen(serverName)

			try:
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
				app.exec_()
			finally:
				localServer.close()
	except Exception as e:
		print(e)
