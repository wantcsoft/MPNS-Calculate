import os
import threading
import datetime
import time
from queue import Queue

from dataCalculation import CalculateThreading, LoggerFile

logger = LoggerFile.MyLog()


class MultiThreading(threading.Thread):

    def __init__(self, main_windows, data_list, total_count):
        threading.Thread.__init__(self)
        self.main_windows = main_windows
        self.data_list = data_list
        self.total_count = total_count

        # 创建5个dll文件
        list = os.getcwd().split('\\')
        list.append("source")
        list.append("bin1")
        list.append("TCDownsGraph.dll")
        self.dll_list = []
        self.dll_list.append('\\'.join(list))
        list[-2] = "bin2"
        self.dll_list.append('\\'.join(list))
        list[-2] = "bin3"
        self.dll_list.append('\\'.join(list))
        list[-2] = "bin4"
        self.dll_list.append('\\'.join(list))
        list[-2] = "bin5"
        self.dll_list.append('\\'.join(list))

        # 创建五个dll配置文件
        list[-2], list[-1] = "Config", "DownsGraph1.ini"
        self.config_ini_list = []
        self.config_ini_list.append('\\'.join(list))
        list[-1] = "DownsGraph2.ini"
        self.config_ini_list.append('\\'.join(list))
        list[-1] = "DownsGraph3.ini"
        self.config_ini_list.append('\\'.join(list))
        list[-1] = "DownsGraph4.ini"
        self.config_ini_list.append('\\'.join(list))
        list[-1] = "DownsGraph5.ini"
        self.config_ini_list.append('\\'.join(list))

    def run(self):
        lock = threading.Lock()
        queue = Queue()
        CalculateThreading.CalculateThreading.data_list = self.data_list
        CalculateThreading.CalculateThreading.median_config = self.main_windows.median_config
        CalculateThreading.CalculateThreading.weight_config = self.main_windows.weight_config
        CalculateThreading.CalculateThreading.connect = self.main_windows.connect
        threading_num = self.main_windows.ui_multithreading.num
        for i in range(0, threading_num):
            thread = CalculateThreading.CalculateThreading(self.dll_list[i], self.config_ini_list[i], lock, queue,
                                                           self.main_windows.main_median_flag,
                                                           self.main_windows.main_weight_flag)
            thread.start()

        self.end_time(queue)

    def end_time(self, queue):
        self.main_windows.lable_exception.setText("异常数量：")
        self.main_windows.lable_complete_time.setText("预估完成时间：")
        self.main_windows.lable_complete_time.setText("计算结束时间：")
        time.sleep(1)
        start_time = time.time()
        while len(self.data_list) > 0:
            current = time.time()
            time.sleep(1)
            time_num = start_time + (current-start_time) * (self.total_count/(self.total_count-len(self.data_list)))
            estimate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_num))
            self.main_windows.progressBar.setText("计算进度:还剩 %s 例" % len(self.data_list))
            self.main_windows.progressBar.show()
            self.main_windows.lable_complete_time.setText("预估完成时间：%s" % estimate_time)
            self.main_windows.lable_left_time.setText("剩余时间：%s" % str(datetime.timedelta(seconds=(time_num-current)))[: 7])
            self.main_windows.lable_exception.setText("异常数量：%s 例" % queue.qsize())
            self.main_windows.lable_exception.show()

        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.main_windows.calculate_sucess.show()
        self.main_windows.lable_complete_time.setText("计算结束时间：%s" % end_time)
        self.main_windows.lable_spend_time.setText("本次计算用时：%s" % str(datetime.timedelta(seconds=(time.time()-start_time)))[: 7])
        self.main_windows.setEnabled(True)


if __name__ == '__main__':
    pass
