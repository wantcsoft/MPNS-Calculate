import ctypes


class TCDowns:
	def __init__(self, path):
		# dll1 = r"D:\pythonWorkSpace\TCSOFT-MPNS\source\bin1\TCDownsGraph.dll"
		# dll2 = r"D:\Program Files (x86)\TCSOFT\MPNS\bin\TCDownsGraph.dll"
		# 加载dll文件
		# self.TCDownsGraph = ctypes.CDLL(r"D:\Program Files (x86)\TCSOFT\MPNS\bin\TCDownsGraph.dll")
		self.TCDownsGraph = ctypes.CDLL(path)
		# 初始化dll
		self.TCDownsGraph.InitCalcDefaultPara()

	def calculate(self, res11, res16):
		self.TCDownsGraph.CalculateParameterSet(res11.encode("ascii"), "11".encode("ascii"))
		self.TCDownsGraph.CalculateParameterSet(res16.encode("ascii"), "16".encode("ascii"))
		buffer1 = ctypes.c_buffer(1000)
		buffer2 = ctypes.c_buffer(1000)
		self.TCDownsGraph.RiskGetEx_Mozzie(buffer1, buffer2, 0)
		mom_value = buffer1.value.decode("ascii")
		risk_value = buffer2.value.decode("ascii")
		buffer1 = None
		buffer2 = None
		return [mom_value, risk_value]


if __name__ == '__main__':
	pass

	# res11 = r"0|2003|0|380|2|350|D:\Program Files (x86)\TCSOFT\MPNS\Config\DownsGraph.ini|D:\Program Files (x86)\TCSOFT\MPNS\RiskFile\71_UI.bmp|D:\Program Files (x86)\TCSOFT\MPNS\RiskFile\71_Print.bmp|1|1|1|1|0.236265|0.004145|0|0|1|0.212382|0.003726|0|0|1|0.089205|0.001565|0|0|1|0.169005|0.002965|0|0|1|0.212382|0.003726|0|0|2|0.2128|40.1|0|0|1|0.236265|0.004145|0|0|1|0.212382|0.003726|0|0|1|0.089205|0.001565|0|0|1|0.169005|0.002965|0|0|1|0.212382|0.003726|0|0|2|0.2128|40.1|0|0|0|0|1.0000|1.0000|1.0000|0|0|1.0000|1.0000|1.0000|0|1.0000"
	# res16 = "0||||||||29.56|0.63|25.6|||||||||||34|0.7|66.25|||||30.30|1|51|0|0|2|0|0|0|104||||0|0|0|||||"
	#
	# re11 = r"0|2003|0|380|2|350|{0}||{1}_Print.bmp|1|1|1|1|0.236265|0.004145|0|0|1|0.212382|0.003726|0|0|1|0.089205|0.001565|0|0|1|0.169005|0.002965|0|0|1|0.212382|0.003726|0|0|2|0.2128|40.1|0|0|1|0.236265|0.004145|0|0|1|0.212382|0.003726|0|0|1|0.089205|0.001565|0|0|1|0.169005|0.002965|0|0|1|0.212382|0.003726|0|0|2|0.2128|40.1|0|0|0.0001|0|1.0000|1.0000|1.0000|0|0|1.0000|1.0000|1.0000|0|1.0000"
	# re16 = "0||||||||40|1.5|20|||||||||||54.99|1.56|28.74|||||30.80|1|57|0|0|2|0|0|0|127||||0|0|0|||||"

	# r11 = r"0|2003|0|380|2|350|{0}||{1}_Print.bmp|1|1|1|1|0.236265|0.004145|0|0|1|0.212382|0.003726|0|0|1|0.089205|0.001565|0|0|1|0.169005|0.002965|0|0|1|0.212382|0.003726|0|0|2|0.2128|40.1|0|0|1|0.236265|0.004145|0|0|1|0.212382|0.003726|0|0|1|0.089205|0.001565|0|0|1|0.169005|0.002965|0|0|1|0.212382|0.003726|0|0|2|0.2128|40.1|0|0|0.0001|0|1.0000|1.0000|1.0000|0|0|1.0000|1.0000|1.0000|0|1.0000"
	# r16 = "0||||||||40|1.5|20|||||||||||54.99|1.56|28.74|||||30.80|1|57|0|0|2|0|0|0|127||||0|0|0|||||"
	# list = os.path.abspath(__file__).split('\\')
	# list[-1], list[-2] = "bin1", "source"
	# list.append("TCDownsGraph.dll")
	# dll_path = '\\'.join(list)
	# print(dll_path)
	r11 = "0|2003|0|380|2|350|D:\\pythonWorkSpace\\MPNS-Calculate\\source\\Config\\DownsGraph1.ini||{1}_Print.bmp|1|1|1|1|0.236265|0.004145|0|0|1|0.212382|0.003726|0|0|1|0.089205|0.001565|0|0|1|0.169005|0.002965|0|0|1|0.212382|0.003726|0|0|2|0.2128|40.1|0|0|1|0.236265|0.004145|0|0|1|0.212382|0.003726|0|0|1|0.089205|0.001565|0|0|1|0.169005|0.002965|0|0|1|0.212382|0.003726|0|0|2|0.2128|40.1|0|0|0.0001|0|1.0000|1.0000|1.0000|0|0|1.0000|1.0000|1.0000|0|1.0000"
	re16 = '0|||||||||||||||||163.94|||587.36||||||||22.78|1||0|0|3|0|0|0|77|54.0|||||0|0|0|||77'
	r16 = "0||||3.245|||5435||||||||||161.09|||628||||||||21.33|1||0|0|2|0|0|0|78|56|||43|43|0|0|0|||78"
	dll_path = r"../source/bin1/TCDownsGraph.dll"
	tc = TCDowns(dll_path)
	result1 = tc.calculate(r11, r16)
	print(result1[0])
	print(result1[1])
