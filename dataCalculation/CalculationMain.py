import os

from dataCalculation import TCDownsGraph
import logging

logging.basicConfig(
    # filename="./logger.logs",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
# format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


class Calculation(object):

    def __init__(self):
        self.data_list = []
        self.median_config = {}
        self.config_ini_path = r"D:\Program Files (x86)\TCSOFT\MPNS\Config\DownsGraph.ini"
        self.connect = None
        list = os.path.abspath(__file__).split('\\')
        list[-1], list[-2] = "bin1", "source"
        list.append("TCDownsGraph.dll")
        dll_path = '\\'.join(list)
        self.tcdowns = TCDownsGraph.TCDowns(dll_path)

    def start(self):
        self.get_parameterList()

    def get_parameterList(self):
        # 遍历所有的数据
        for data in self.data_list:
            logger.info("这是一条检测数据 %s" % data)
            if data.SolutionRiskSerialID == 8:
                continue
            self.solution_risk_serialID = data.SolutionRiskSerialID
            logger.info("solution_Risk_SerialID = %s" % data.SolutionRiskSerialID)
            self.EarlySampleSerialID = data.EarlySampleSerialID
            self.MiddleSampleSerialID = data.MiddleSampleSerialID
            # 获取孕周类型
            gestation_type = data.GestationType_E if data.GestationType_E != None else data.GestationType_M
            # 早期孕周天数
            gestationWeek_E = data.GestationWeek_E
            # 中期孕周天数
            gestationWeek_M = data.GestationWeek_M
            logger.info("gestationWeek_E = %s, gestationWeek_M = %s" % (gestationWeek_E, gestationWeek_M))
            # 从WOR_DS_SolutionRiskInfo数据表中拿出拼串
            parameter = self.connect.query_parameterList(self.solution_risk_serialID)[0][0]
            # 如果没有拿到拼串，则开始计算下一条数据
            if parameter == None:
                continue
            # 取出这个拼串的第一和第二部分
            r16 = parameter.split("&")[1].split("|")
            # 一个孕妇她测试了多少个标记物，按照123……进行排序放进list中
            median_list = {}
            logger.info("r16 = %s" % r16)
            for i in range(1, 14):
                if r16[i] != "":
                    median_list[self.item_convert(i)] = 0
            if r16[39] != "":
                median_list["16"] = 0
            # 获取孕妇的孕周类型，孕周类型不会改变
            logger.info("孕周类型 = %s" % gestation_type)
            items = self.median_config.get(str(gestation_type))
            # 遍历标记物集合，取出对应的重新设定的标记物版本和赋予中位数值
            for i in median_list:
                if int(i) == 16:
                    continue
                items_new_version = int(items.get(i))
                # NT需要特殊处理
                if int(i) == 7:
                    check_value = self.get_nt_median(self.EarlySampleSerialID, gestation_type)
                    if items_new_version == 1:
                        # 获取母版本版本号和中位数值
                        if len(check_value) == 1:
                            median_list['7'] = self.connect.query_NT_medianValue(items_new_version, i, 0,
                                                                                 check_value[0])
                        else:
                            median_list['7'] = self.connect.query_NT_medianValue(items_new_version, i, 0,
                                                                                 check_value[0])
                            median_list['16'] = self.connect.query_NT_medianValue(items_new_version, i, 0,
                                                                                  check_value[1])
                    else:
                        if len(check_value) == 1:
                            median_list['7'] = self.connect.query_NT_medianValue(items_new_version, i, gestation_type,
                                                                                 check_value[0])
                        else:
                            median_list['7'] = self.connect.query_NT_medianValue(items_new_version, i, gestation_type,
                                                                                 check_value[0])
                            median_list['16'] = self.connect.query_NT_medianValue(items_new_version, i, gestation_type,
                                                                                  check_value[1])
                # 早期检测
                elif int(i) > 7:
                    if items_new_version == 1:
                        # 获取母版本版本号和中位数值
                        median_data = self.connect.query_mather_medianValue(items_new_version, i,
                                                                            str(data.GestationWeek_E) + "." + str(
                                                                                data.GestationDay_E))
                    else:
                        median_data = self.connect.query_MedianValue(items_new_version, i, gestation_type,
                                                                     str(data.GestationWeek_E) + "." + str(
                                                                         data.GestationDay_E))
                    median_list[i] = median_data
                # 中期检测
                if int(i) < 7:
                    if items_new_version == 1:
                        median_data = self.connect.query_mather_medianValue(items_new_version, i,
                                                                            str(data.GestationWeek_M) + "." + str(
                                                                                data.GestationDay_M))
                    else:
                        median_data = self.connect.query_MedianValue(items_new_version, i, gestation_type,
                                                                     str(data.GestationWeek_M) + "." + str(
                                                                         data.GestationDay_M))
                    median_list[i] = median_data
            # median_list以标记物序号为key,版本号和值values
            self.tcdowns_dll(median_list, parameter)
            # break
        return "计算完成"

    # 获取NT的gestationWeek长度
    def get_nt_median(self, sampleSerialID, gestation_type):
        check_data = self.connect.query_NT_MedianValue(sampleSerialID, gestation_type)[0]
        if check_data.CheckValueOne == None and check_data.CheckValueTwo == None:
            check_value = [check_data.CheckValue]
        else:
            check_value = [check_data.CheckValueOne, check_data.CheckValueTwo]
        return check_value

    # 拼串顺序转标记物序号
    def item_convert(self, num):
        if num == 1:
            return "7"

        elif num == 2:
            return "8"

        elif num == 3:
            return "10"

        elif num == 4:
            return "9"

        elif num == 5:
            return "12"

        elif num == 6:
            return "11"

        elif num == 7:
            return "13"

        elif num == 8:
            return "1"

        elif num == 9:
            return "3"

        elif num == 10:
            return "2"

        elif num == 11:
            return "5"

        elif num == 12:
            return "4"

        elif num == 13:
            return "6"

        elif num == 14:
            return "16"

    # 标记物序号转拼串顺序
    def convert_item(self, num):
        if num == "7":
            return 1

        elif num == "8":
            return 2

        elif num == "10":
            return 3

        elif num == "9":
            return 4

        elif num == "12":
            return 5

        elif num == "11":
            return 6

        elif num == "13":
            return 7

        elif num == "1":
            return 8

        elif num == "3":
            return 9

        elif num == "2":
            return 10

        elif num == "5":
            return 11

        elif num == "4":
            return 12

        elif num == "6":
            return 13

        elif num == "16":
            return 14

    def tcdowns_dll(self, median_list, parameter):
        logger.info("原本的拼串 = %s" % parameter)
        list = parameter.split("&")
        data_list = list[1].split("|")
        logger.info(data_list)
        # 给所有的标记物绑定新的中位数值
        for i in median_list:
            if i == "16":
                data_list[40] = format(median_list.get(i)[0][0], '.2f')
            else:
                data_list[self.convert_item(i) + 13] = format(median_list.get(i)[0][0], '.2f')
        r11 = list[0].split("|")
        r11[6] = self.config_ini_path
        r11_new = "|".join(r11)
        r16 = "|".join(data_list)
        list[1] = r16
        # new_parameter 这个是生成的新串
        new_parameter = "&".join(list)
        logger.info("新生成的拼串 = %s" % new_parameter)
        result = self.tcdowns.calculate(r11_new, r16)
        mom = result[0].split("|")
        mom_dict = {}
        # 进过dll计算，将所得标记物得到的mom值绑定
        # for i in range(1, 15):
        # 	if float(mom[i]) != 0:
        # 		mom_dict[self.item_convert(i)] = float(mom[i])
        for i in median_list:
            mom_dict[i] = float(mom[self.convert_item(i)])
        logger.info("mom_dict = %s" % mom_dict)
        AFP_ONTD = 0
        for i in mom_dict:
            mom_value = mom_dict.get(i)
            if i == '1':
                AFP_ONTD = mom_value
            if median_list.get(i) != 0:
                median_value = format(median_list.get(i)[0][0], '.2f')
                median_no = int(median_list.get(i)[0][1])
                logger.info(
                    "标记物 = %s, 新的中位数版本号 = %s, 中位数值 = %s, 计算出的mom值 = %s" % (i, median_no, median_value, mom_value))
                test_item_id = int(i)
                if test_item_id > 6:
                    sampleSerialID = int(self.EarlySampleSerialID)
                elif test_item_id < 7:
                    sampleSerialID = int(self.MiddleSampleSerialID)
                # 更新testInfo表中的medianValue和medianVerNo字段
                # logger.info("sampleSerialID = %s" % sampleSerialID)
                # self.connect.update_testInfo(mom_value, median_no, median_value, test_item_id, sampleSerialID)
                # 如果数据库中的VerifyWorkFlow状态为0，更新为1
                # self.connect.update_VerifyWorkFlow(self.solution_risk_serialID)

        risk = result[1].split("|")
        logger.info("risk = %s" % risk)
        DownsResult = risk[1]
        ONTDResult = risk[2]
        TrisomyResult = risk[3]
        ChildBirthdayDateAgeRisk = risk[5]
        DownsResult1 = risk[8]
        DownsResult2 = risk[9]
        TrisomyResult1 = risk[10]
        TrisomyResult2 = risk[11]
        ChildBirthdayDateAgeRiskTrisomy = risk[15]
        ParameterList = new_parameter
        logger.info("DownsResult = %s" % DownsResult)
        logger.info("ONTDResult = %s" % ONTDResult)
        logger.info("TrisomyResult = %s" % TrisomyResult)
        # logger.info("ChildBirthdayDateAgeRisk = %s" % ChildBirthdayDateAgeRisk)
        # logger.info("DownsResult1 = %s" % DownsResult1)
        # logger.info("DownsResult2 = %s" % DownsResult2)
        # logger.info("TrisomyResult1 = %s" % TrisomyResult1)
        # logger.info("TrisomyResult2 = %s" % TrisomyResult2)
        # logger.info("ChildBirthdayDateAgeRiskTrisomy = %s" % ChildBirthdayDateAgeRiskTrisomy)
        over_all_Risk = self.overallRisk_calculation(DownsResult, ONTDResult, TrisomyResult,
                                                     self.solution_risk_serialID, AFP_ONTD)

        # 跟新各种风险值
        # self.connect.updata_all_risk(DownsResult, ONTDResult, TrisomyResult, ChildBirthdayDateAgeRisk,
        # DownsResult1, DownsResult2, TrisomyResult1, TrisomyResult2,ChildBirthdayDateAgeRiskTrisomy,
        # 							 ParameterList, over_all_Risk, self.solution_risk_serialID)

    # 计算总体风险
    def overallRisk_calculation(self, DownsResult, ONTDResult, TrisomyResult, solution_Risk_SerialID, AFP_ONTD):
        logger.info("总体风险")
        list = self.connect.query_all_cuff(solution_Risk_SerialID)[0]
        DownsCuff = list.DownsCuff
        DownsGrayCuff = list.DownsGrayCuff
        ONTDCuff = list.ONTDCuff
        ONTDGrayCuff = list.ONTDGrayCuff
        TrisomyCuff = list.TrisomyCuff
        TrisomyGrayCuff = list.TrisomyGrayCuff
        ONTDCuffType = list.ONTDCuffType
        # 阻断值是否带符号标志
        RiskEqualSign = self.connect.query_RiskEqualSign()[0][0]
        # 计算出Downs、ONTD、Trisomy的风险值
        DownsResult = float(DownsResult)
        ONTDResult = float(ONTDResult)
        TrisomyResult = float(TrisomyResult)
        if RiskEqualSign == '1':
            # 唐氏风险值判断
            if DownsResult <= DownsCuff:
                Downs = 1
            elif (DownsResult > DownsCuff) and (DownsResult <= DownsGrayCuff):
                Downs = 2
            else:
                Downs = 0

            # ONTD风险判断
			# ONTD阻断类型判断
            logger.info("ONTDCuffType = %s" % ONTDCuffType)
            if ONTDCuffType == 0:
                if ONTDResult <= ONTDCuff:
                    ONTD = 1
                elif (ONTDResult > ONTDCuff) and (ONTDResult >= ONTDGrayCuff):
                    ONTD = 2
                else:
                    ONTD = 0
            else:
                ONTDResult = AFP_ONTD
                if ONTDResult > ONTDCuff:
                    ONTD = 1
                elif (ONTDResult <= ONTDCuff) and (ONTDResult > ONTDGrayCuff):
                    ONTD = 2
                else:
                    ONTD = 0

            # Trisomy风险判断
            if TrisomyResult <= TrisomyCuff:
                Trisomy = 1
            elif (TrisomyResult > TrisomyCuff) and (TrisomyResult <= TrisomyGrayCuff):
                Trisomy = 2
            else:
                Trisomy = 0

        else:
            # 唐氏风险值判断
            if DownsResult < DownsCuff:
                Downs = 1
            elif (DownsResult >= DownsCuff) and (DownsResult < DownsGrayCuff):
                Downs = 2
            else:
                Downs = 0

            # ONTD风险判断
            # ONTD阻断类型判断
            if ONTDCuffType == 0:
                if ONTDResult < ONTDCuff:
                    ONTD = 1
                elif (ONTDResult >= ONTDCuff) and (ONTDResult < ONTDGrayCuff):
                    ONTD = 2
                else:
                    ONTD = 0
            else:
                ONTDResult = AFP_ONTD
                if ONTDResult >= ONTDCuff:
                    ONTD = 1
                elif (ONTDResult < ONTDCuff) and (ONTDResult >= ONTDGrayCuff):
                    ONTD = 2
                else:
                    ONTD = 0

            # Trisomy风险判断
            if TrisomyResult < TrisomyCuff:
                Trisomy = 1
            elif (TrisomyResult >= TrisomyCuff) and (TrisomyResult < TrisomyGrayCuff):
                Trisomy = 2
            else:
                Trisomy = 0

        risk = []
        if Downs == 1 or ONTD == 1 or Trisomy == 1:
            risk.append("high")
        elif Downs == 0 and ONTD == 0 and Trisomy == 0:
            risk.append("low")
        else:
            risk.append("middle")
        risk.append(str(Downs))
        risk.append(str(ONTD))
        risk.append(str(Trisomy))
        over_all_risk = '|'.join(risk)
        over_all_risk += "|0|0&"
        database_risk = self.connect.query_over_all_risk(solution_Risk_SerialID)[0][0]
        over_all_risk += database_risk.split("&")[1]
        logger.info("数据库中的整体的风险串= %s" % self.connect.query_over_all_risk(solution_Risk_SerialID)[0][0])
        logger.info("over_all_risk     = %s" % over_all_risk)
        return over_all_risk


if __name__ == '__main__':
    pass