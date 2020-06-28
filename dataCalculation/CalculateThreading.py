import json
from datetime import datetime
from threading import Thread
from dataCalculation import TCDownsGraph, LoggerFile
from sqlServer.QueryData import QueryData

logger = LoggerFile.MyLog()


class CalculateThreading(Thread):
    data_list = []
    median_config = {}
    weight_config = {}

    def __init__(self, dll_path, config_ini_path, lock, queue, median_flag, weight_flag):
        super().__init__()
        self.dll_path = dll_path
        self.config_ini_path = config_ini_path
        self.queue = queue
        self.median_flag = median_flag
        self.weight_flag = weight_flag
        # 线程资源锁
        self.lock = lock
        # downs计算
        self.tcdowns = TCDownsGraph.TCDowns(dll_path)
        # 数据库连接
        with open("./database.json", 'r') as data_base:
            setting = json.load(data_base)
            server = setting["server"]
            database = setting["databaseName"]
            user_name = setting["user"]
            user_password = setting["password"]
        data_base.close()
        self.connect = QueryData()
        self.connect.connect("{SQL Server}", server, database, user_name, user_password)

    def run(self):
        while len(self.data_list) > 0:
            self.lock.acquire()
            if len(self.data_list) <= 0:
                break
            data = self.data_list.pop()
            self.lock.release()
            self.handle_data(data)

    def handle_data(self, data):
        self.checkNo = data.CheckNo
        logger.info("CheckNo = %s" % self.checkNo)
        if data.SolutionRiskSerialID is None:
            logger.error("SolutionRiskSerialID为空, CheckNo = %s" % self.checkNo)
            self.queue.put(self.checkNo)
            return False
        plan = self.connect.query_screening_plan(data.SolutionRiskSerialID)[0][0]
        if int(plan) == 3 and (data.EarlySampleSerialID is None or data.MiddleSampleSerialID is None):
            logger.error("该条数据是联合方案，计算缺少样本, CheckNo = %s" % self.checkNo)
            self.queue.put(self.checkNo)
            return False
        if data.EarlySampleSerialID is None and data.MiddleSampleSerialID is None:
            logger.error("该条数据没有样本号, CheckNo = %s" % self.checkNo)
            self.queue.put(self.checkNo)
            return False
        # 获取孕周类型
        if data.GestationType_E is None:
            if data.GestationType_M is None:
                logger.error("该条数据没有孕周类型, CheckNo = %s" % self.checkNo)
                self.queue.put(self.checkNo)
                return False
            else:
                gestation_type = data.GestationType_M
        else:
            gestation_type = data.GestationType_E
        # 从WOR_DS_SolutionRiskInfo数据表中拿出拼串
        old_parameter = self.connect.query_parameterList(data.SolutionRiskSerialID)[0][0]
        logger.info("old_parameter = %s" % old_parameter)
        # 如果没有拿到拼串，则开始计算下一条数据
        if old_parameter is None or old_parameter == "":
            list = self.handle_no_parameter(data, gestation_type)
        else:
            # 当数据库有拼串的时候
            list = old_parameter.split("&")
            r11 = list[0].split("|")
            r16 = list[1].split("|")
            # 如果配置了中位数版本，处理第二个拼串
            if self.median_flag:
                # 一个孕妇她测试了多少个标记物，按照123……进行排序放进list中
                self.median_list = {}
                # 遍历前14条数据，不为空说明该种标记物有值，上次进行了计算
                for i in range(1, 14):
                    if r16[i] != "":
                        self.median_list[self.item_convert(i)] = 0
                # 一种特殊的标记物NT_E2需要特殊判断一下
                if r16[39] != "":
                    logger.info("该条数据有标记物NT_E2")
                    self.median_list["16"] = 0
                # 得到跟新过的新的拼串
                r16 = self.handle_median(r16, gestation_type, data)
            # 如果配置了体重校正参数，处理第一个拼串
            if self.weight_flag:
                r11 = self.handle_weight(r11)
            list[0] = "|".join(r11)
            list[1] = "|".join(r16)
        # 将拼串放进dll进行计算
        result = self.tcdowns.calculate(list[0], list[1])
        temp = list[0].split("|")
        temp[6] = "{0}"
        list[0] = "|".join(temp)
        new_parameter = "&".join(list)
        logger.info("new_parameter = %s" % new_parameter)
        # mom值结果
        mom = result[0].split("|")
        ONTDResult = self.handle_mom_value(mom, data)
        # 风险结果
        risk = result[1].split("|")
        self.handle_risk(risk, ONTDResult, new_parameter, data.SolutionRiskSerialID)

    # 当数据库中没有拼串时
    def handle_no_parameter(self, data, gestation_type):
        # 设置第一段拼串
        param = self.connect.no_query_r11(data.SolutionRiskSerialID)[0]
        r11 = [""] * 84
        r11[0] = "0"
        r11[1] = "2003"
        r11[2] = "0"
        r11[3] = str(int(param.DownsCritical))
        r11[4] = str(int(param.ONTDCritical))
        r11[5] = str(int(param.TrisomyCritical))
        r11[8] = "{1}_Print.bmp"
        r11[9] = str(param.ONTDCriticalType)
        r11[10] = str(param.USELimit)
        r11[11] = str(param.USETwoTrisomyRisk)
        # 配置第一个拼串12--71
        r11 = self.handle_weight(r11)
        r11[72] = str(float("%.4f" % param.PatuaCritical))
        r11[73] = "0"
        r11[74] = "1.0000"
        r11[75] = "1.0000"
        r11[76] = "1.0000"
        r11[77] = "1.0000"
        r11[78] = "1.0000"
        r11[79] = "1.0000"
        r11[80] = "1.0000"
        r11[81] = "1.0000"
        r11[82] = "1.0000"
        r11[83] = "1.0000"
        # 设置第二段拼串
        r16 = [""] * 49
        r16[0] = "0"
        # 获取检测的方案和标记物的种类
        testItems = param.TestItems.split("|")
        self.median_list = {}
        for i in testItems:
            if int(i) < 7:
                if int(i) == 2:
                    r16[self.convert_item(i)] = str(self.connect.query_item_value(data.MiddleSampleSerialID, i)[0][0]/1000)
                else:
                    r16[self.convert_item(i)] = str(self.connect.query_item_value(data.MiddleSampleSerialID, i)[0][0])
            else:
                if int(i) == 9:
                    r16[self.convert_item(i)] = str(self.connect.query_item_value(data.EarlySampleSerialID, i)[0][0]/1000)
                else:
                    r16[self.convert_item(i)] = str(self.connect.query_item_value(data.EarlySampleSerialID, i)[0][0])
            self.median_list[i] = 0
        # 处理第二段拼串1--26还有39,40
        r16 = self.handle_median(r16, gestation_type, data)
        if data.EarlySampleSerialID is not None:
            patientInfo = self.connect.query_premature_age(data.EarlySampleSerialID)[0]
            r16[28] = str(float('%.2f' % patientInfo.ChildBirthDateAge))
            r16[38] = str(patientInfo.Weight)
            r16[37] = str(patientInfo.GestationWeek*7 + patientInfo.GestationDay)
            # CRL孕周日
            if gestation_type == 3:
                sampling_day = datetime.date(patientInfo.SamplingDate).day
                crl = self.connect.query_CRL_weekday(data.EarlySampleSerialID, gestation_type)[0].CheckDate
                if crl is not None:
                    check_day = datetime.date(crl).day
                    r16[48] = str(patientInfo.GestationWeek * 7 + patientInfo.GestationDay + (check_day - sampling_day))
        if data.MiddleSampleSerialID is not None:
            patientInfo = self.connect.query_premature_age(data.MiddleSampleSerialID)[0]
            r16[28] = str(float('%.2f' % patientInfo.ChildBirthDateAge))
            r16[30] = str(patientInfo.Weight)
            if r16[37] != "":
                r16[37] = str(patientInfo.GestationWeek * 7 + patientInfo.GestationDay)
            r16[47] = str(patientInfo.GestationWeek*7 + patientInfo.GestationDay)
            # CRL孕周日
            if gestation_type == 3:
                sampling_day = datetime.date(patientInfo.SamplingDate).day
                crl = self.connect.query_CRL_weekday(data.MiddleSampleSerialID, gestation_type)[0].CheckDate
                if crl is not None:
                    check_day = datetime.date(crl).day
                    r16[48] = str(patientInfo.GestationWeek*7 + patientInfo.GestationDay + (check_day - sampling_day))
        r16[29] = str(self.connect.query_people_color(data.PatientSerialID)[0][0])
        list_31 = self.connect.query_r16_31_36(data.PregnantSerialID)[0]
        r16[31] = str(list_31.Diabetes)
        r16[32] = str(list_31.FetalNumber)
        r16[33] = "2" if gestation_type != 1 else "1"
        r16[34] = str(list_31.IVF)
        r16[35] = str(list_31.SmokeHistory)
        r16[36] = str(list_31.DownsHistory)
        if data.EarlySampleSerialID is not None:
            crl_len = self.connect.query_NT_MedianValue(data.EarlySampleSerialID, gestation_type)[0]
            if crl_len.CheckValueOne is None and crl_len.CheckValueTwo is None:
                if crl_len.CheckValue is None:
                    r16[41] = "0"
                    r16[42] = "0"
                else:
                    r16[41] = str(crl_len.CheckValue)
                    r16[42] = str(crl_len.CheckValue)
            else:
                r16[41] = str(crl_len.CheckValueOne)
                r16[42] = str(crl_len.CheckValueTwo)
        r16[43] = "0"
        r16[44] = "0"
        r16[45] = "0"
        r11 = "|".join(r11)
        r16 = "|".join(r16)
        return [r11, r16, "0&0|1.0000|1.0000|1.0000|0|0|1.0000|1.0000|1.0000|0|1.0000&"]

    # 处理第一个拼串
    def handle_weight(self, r11):
        r11[6] = self.config_ini_path
        r11[12] = self.weight_config.get("AFP2")[0]
        r11[13] = self.weight_config.get("AFP2")[1]
        r11[14] = self.weight_config.get("AFP2")[2]
        r11[15] = self.weight_config.get("AFP2")[3]
        r11[16] = self.weight_config.get("AFP2")[4]
        r11[17] = self.weight_config.get("hCG2")[0]
        r11[18] = self.weight_config.get("hCG2")[1]
        r11[19] = self.weight_config.get("hCG2")[2]
        r11[20] = self.weight_config.get("hCG2")[3]
        r11[21] = self.weight_config.get("hCG2")[4]
        r11[22] = self.weight_config.get("uE32")[0]
        r11[23] = self.weight_config.get("uE32")[1]
        r11[24] = self.weight_config.get("uE32")[2]
        r11[25] = self.weight_config.get("uE32")[3]
        r11[26] = self.weight_config.get("uE32")[4]
        r11[27] = self.weight_config.get("InhA2")[0]
        r11[28] = self.weight_config.get("InhA2")[1]
        r11[29] = self.weight_config.get("InhA2")[2]
        r11[30] = self.weight_config.get("InhA2")[3]
        r11[31] = self.weight_config.get("InhA2")[4]
        r11[32] = self.weight_config.get("fbhCG2")[0]
        r11[33] = self.weight_config.get("fbhCG2")[1]
        r11[34] = self.weight_config.get("fbhCG2")[2]
        r11[35] = self.weight_config.get("fbhCG2")[3]
        r11[36] = self.weight_config.get("fbhCG2")[4]
        r11[37] = self.weight_config.get("PAPPA2")[0]
        r11[38] = self.weight_config.get("PAPPA2")[1]
        r11[39] = self.weight_config.get("PAPPA2")[2]
        r11[40] = self.weight_config.get("PAPPA2")[3]
        r11[41] = self.weight_config.get("PAPPA2")[4]
        r11[42] = self.weight_config.get("AFP1")[0]
        r11[43] = self.weight_config.get("AFP1")[1]
        r11[44] = self.weight_config.get("AFP1")[2]
        r11[45] = self.weight_config.get("AFP1")[3]
        r11[46] = self.weight_config.get("AFP1")[4]
        r11[47] = self.weight_config.get("hCG1")[0]
        r11[48] = self.weight_config.get("hCG1")[1]
        r11[49] = self.weight_config.get("hCG1")[2]
        r11[50] = self.weight_config.get("hCG1")[3]
        r11[51] = self.weight_config.get("hCG1")[4]
        r11[52] = self.weight_config.get("uE31")[0]
        r11[53] = self.weight_config.get("uE31")[1]
        r11[54] = self.weight_config.get("uE31")[2]
        r11[55] = self.weight_config.get("uE31")[3]
        r11[56] = self.weight_config.get("uE31")[4]
        r11[57] = self.weight_config.get("InhA1")[0]
        r11[58] = self.weight_config.get("InhA1")[1]
        r11[59] = self.weight_config.get("InhA1")[2]
        r11[60] = self.weight_config.get("InhA1")[3]
        r11[61] = self.weight_config.get("InhA1")[4]
        r11[62] = self.weight_config.get("fbhCG1")[0]
        r11[63] = self.weight_config.get("fbhCG1")[1]
        r11[64] = self.weight_config.get("fbhCG1")[2]
        r11[65] = self.weight_config.get("fbhCG1")[3]
        r11[66] = self.weight_config.get("fbhCG1")[4]
        r11[67] = self.weight_config.get("PAPPA1")[0]
        r11[68] = self.weight_config.get("PAPPA1")[1]
        r11[69] = self.weight_config.get("PAPPA1")[2]
        r11[70] = self.weight_config.get("PAPPA1")[3]
        r11[71] = self.weight_config.get("PAPPA1")[4]
        return r11

    # 处理第二个拼串
    def handle_median(self, r16, gestation_type, data):
        # 获取孕妇的孕周类型，孕周类型不会改变，前中期的孕周都一样
        items = self.median_config.get(str(gestation_type))
        # 遍历标记物集合，取出对应的重新设定的标记物版本和赋予中位数值
        for i in self.median_list:
            # 如果有16号跳过，在7号标记物一并处理掉了
            if int(i) == 16:
                continue
            # 设置新的版本号
            items_new_version = int(items.get(i))
            # 7号标记物NT需要特殊处理
            if int(i) == 7:
                # 获取NT标记物的长度，可能有一个值，也可能有两个值
                check_value = self.get_nt_median(data.EarlySampleSerialID, gestation_type)
                # 获取不到NT的值
                if len(check_value) == 0:
                    self.median_list['7'] = 0

                # 重新计算的版本号为1版本
                if items_new_version == 1:
                    # 获取母版本版本号和中位数值
                    if len(check_value) == 1:
                        self.median_list['7'] = self.connect.query_NT_medianValue(items_new_version, i, 0,
                                                                             check_value[0])
                    else:
                        self.median_list['7'] = self.connect.query_NT_medianValue(items_new_version, i, 0,
                                                                             check_value[0])
                        self.median_list['16'] = self.connect.query_NT_medianValue(items_new_version, i, 0,
                                                                              check_value[1])
                else:
                    # 版本号不为1
                    if len(check_value) == 1:
                        self.median_list['7'] = self.connect.query_NT_medianValue(items_new_version, i, gestation_type,
                                                                             check_value[0])
                    else:
                        self.median_list['7'] = self.connect.query_NT_medianValue(items_new_version, i, gestation_type,
                                                                             check_value[0])
                        self.median_list['16'] = self.connect.query_NT_medianValue(items_new_version, i, gestation_type,
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
                self.median_list[i] = median_data
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
                self.median_list[i] = median_data
        # median_list以标记物序号为key,版本号和值values
        # 给拼串的数组中所有的标记物绑定新的中位数值
        for i in self.median_list:
            if i == "16":
                point_num = self.connect.query_median_points(i)[0].DefaultMedianDecimal
                r16[40] = format(self.median_list.get(i)[0][0], '.%sf' % point_num)
            else:
                if self.median_list.get(i)[0] is not None and self.median_list.get(i)[0][0] is not None:
                    point_num = self.connect.query_median_points(i)[0].DefaultMedianDecimal
                    r16[self.convert_item(i) + 13] = format(self.median_list.get(i)[0][0], '.%sf' % point_num)
                else:
                    logger.error("标记物%s，%s版本没有中位数值, solution_risk_serialID = %s, CheckNo = %s" %
                                  (i, self.median_list.get(i)[0].MedianVerNo, data.SolutionRiskSerialID, self.checkNo))
        return r16

    # 获取NT的gestationWeek长度
    def get_nt_median(self, sampleSerialID, gestation_type):
        check_data = self.connect.query_NT_MedianValue(sampleSerialID, gestation_type)[0]
        if len(check_data) == 0:
            logger.error("checkNo = %s, 获取不到7号标记物长度" % self.checkNo)
            self.queue.put(self.checkNo)
            return []

        if check_data.CheckValueOne is None and check_data.CheckValueTwo is None:
            check_value = [check_data.CheckValue]
        else:
            check_value = [check_data.CheckValueOne, check_data.CheckValueTwo]
        return check_value

    # 将新计算出的mom值跟新到数据库中
    def handle_mom_value(self, mom, data):
        # mom_dict用于存放标记物算出来的mom值
        mom_dict = {}
        # 进过dll计算，将所得标记物得到的mom值绑定
        for i in self.median_list:
            mom_dict[i] = float(mom[self.convert_item(i)])
        ONTDResult = 0
        for i in mom_dict:
            mom_value = mom_dict.get(i)
            # 当AFP标记物有值得话，设置为ONTD的值
            if i == '1':
                ONTDResult = mom_value
            if self.median_list.get(i) != 0:
                median_value = format(self.median_list.get(i)[0][0], '.2f')
                median_no = int(self.median_list.get(i)[0][1])
                logger.info("标记物 = %s, 新版本号 = %s, 数值 = %s, mom值 = %s"
                            % (i, median_no, median_value, mom_value))
                test_item_id = int(i)
                if test_item_id > 6:
                    sampleSerialID = int(data.EarlySampleSerialID)
                else:
                    sampleSerialID = int(data.MiddleSampleSerialID)
                old_median = self.connect.query_testInfo(sampleSerialID, i)[0]
                logger.info("标记物 = %s, 旧版本号 = %s, 数值 = %s, mom值 = %s"
                            % (i, old_median.MedianVerNo,
                               format(old_median.MedianValue, '.2f'),
                               format(old_median.ResultMOM, '.4f')))
                # 更新testInfo表中的medianValue和medianVerNo字段
                self.connect.update_testInfo(mom_value, median_no, median_value, test_item_id, sampleSerialID)
                # 如果数据库中的VerifyWorkFlow状态为0，更新为1
                self.connect.update_VerifyWorkFlow(data.SolutionRiskSerialID)
        return ONTDResult

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

    def handle_risk(self, risk, ONTDResult, Parameter, solution_risk_serialID):
        DownsResult = 0 if risk[1] == "" else risk[1]
        # 当没有afp值得时候，ONTN就用原来的值
        if ONTDResult == 0:
            ONTDResult = risk[2]
        TrisomyResult = 0 if risk[3] == "" else risk[3]
        ChildBirthdayDateAgeRisk = 0 if risk[5] == "" else risk[5]
        DownsResult1 = 0 if risk[8] == "" else risk[8]
        DownsResult2 = 0 if risk[9] == "" else risk[9]
        TrisomyResult1 = 0 if risk[10] == "" else risk[10]
        TrisomyResult2 = 0 if risk[11] == "" else risk[11]
        ChildBirthdayDateAgeRiskTrisomy = 0 if risk[15] == "" else risk[15]
        over_all_Risk = self.overallRisk_calculation(DownsResult, ONTDResult,
                                                     TrisomyResult, solution_risk_serialID)

        # 跟新各种风险值
        self.connect.updata_all_risk(DownsResult, ONTDResult, TrisomyResult, ChildBirthdayDateAgeRisk,
                                     DownsResult1, DownsResult2, TrisomyResult1, TrisomyResult2,
                                     ChildBirthdayDateAgeRiskTrisomy, Parameter, over_all_Risk,
                                     solution_risk_serialID)

    # 计算总体风险
    def overallRisk_calculation(self, DownsResult, ONTDResult, TrisomyResult, solution_Risk_SerialID):
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
            if ONTDCuffType == 0:
                if ONTDResult <= ONTDCuff:
                    ONTD = 1
                elif (ONTDResult > ONTDCuff) and (ONTDResult >= ONTDGrayCuff):
                    ONTD = 2
                else:
                    ONTD = 0
            else:
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
        over_all_risk += "|0|0&||||||||||||||||"
        logger.info("旧风险串  = %s" % self.connect.query_over_all_risk(solution_Risk_SerialID)[0][0])
        logger.info("新风险串 = %s" % over_all_risk)
        return over_all_risk


if __name__ == '__main__':
    pass
