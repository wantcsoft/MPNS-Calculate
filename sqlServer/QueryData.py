from datetime import datetime

import pyodbc


class QueryData(object):

    def __init__(self):
        pass

    # 数据库连接设置
    def connect(self, driver, server, databaseName, user, password):
        try:
            cursor = pyodbc.connect(p_str="Mozzie",
                                    autocommit=True,
                                    DRIVER=driver,
                                    SERVER=server,
                                    DATABASE=databaseName,
                                    UID=user,
                                    PWD=password).cursor()
            self.cursor = cursor
            return "链接成功"
        except Exception:
            return "网络错误"

    # 中位具体的版本内容查询
    def median_version_query(self, median_no, item_id, gestation_type):
        sql = '''select GestationWeek, MedianValue, MedianUnit
				from BSC_DS_GestationMedian 
				where MedianVerNo = %d
				and TestItemID = %d
				and GestationType = %d
		union
				select GestationWeek, MedianValue, MedianUnit
				from BSC_DS_HistoryMedian 
				where MedianVerNo = %d
				and TestItemID = %d
				and GestationType = %d''' % (median_no, item_id, gestation_type, median_no, item_id, gestation_type)
        return self.cursor.execute(sql).fetchall()

    # 根据孕周类型查询中位数版本
    def version_testItem_gestation(self, gestation):
        sql = '''select MedianVerNo, TestItemID, GestationType, CONVERT (CHAR(10), MedianVerDate, 120) as date 
				from BSC_DS_MedianVerInfo 
				where GestationType in (0,%d)
		        order by MedianVerNo desc''' % (gestation)
        return self.cursor.execute(sql).fetchall()

    # 根据审核状态查询出具体的数量（与日期无关）
    def query_workflow_count(self, verify_workflow):
        sql = """select count (*)
		from V_DS_TotalInfo_based_on_SolutionRiskInfo 
		where VerifyWorkFlow in %s""" % (verify_workflow)
        return self.cursor.execute(sql).fetchall()

    # 根据审核状态查询关键字段（与日期无关）
    def query_workflow(self, verify_workflow):
        sql = """select CheckNo, SolutionRiskSerialID, PatientSerialID,
			EarlySampleSerialID, MiddleSampleSerialID, PregnantSerialID,
			GestationWeek_E, GestationWeek_M,
			GestationDay_E, GestationDay_M,
			GestationType_E, GestationType_M
			from V_DS_TotalInfo_based_on_SolutionRiskInfo
			where VerifyWorkFlow in %s""" % (verify_workflow)
        return self.cursor.execute(sql).fetchall()

    # 通过时间还有筛查流程状态查询出只有一次检查的人的个数
    def query_one_time_workflow_count(self, start, end, verify_workflow):
        sql = """select count(*)
		from V_DS_TotalInfo_based_on_SolutionRiskInfo
		where VerifyWorkFlow in %s
		and (TestDate_E is null or TestDate_M is null)
		and (TestDate_E between '%s' and '%s' 
		or TestDate_M between '%s' and '%s')""" % (verify_workflow, start, end, start, end)
        return self.cursor.execute(sql).fetchall()

    # 通过时间还有筛查流程状态查询出有两次检查的人的个数（测试日期只需要有一个在日期范围内）
    def query_two_time_workflow_any_count(self, start, end, verify_workflow):
        sql = """select count(*)
		from V_DS_TotalInfo_based_on_SolutionRiskInfo
		where VerifyWorkFlow in %s
		and (TestDate_E is not null and TestDate_M is not null)
		and 
		(TestDate_E between '%s' and '%s' 
		or TestDate_M between '%s' and '%s')""" % (verify_workflow, start, end, start, end)
        return self.cursor.execute(sql).fetchall()

    # 通过时间还有筛查流程状态查询出有两次检查的人的个数（早期和中期测试日期必须都在日期范围内）
    def query_two_time_workflow_all_count(self, start, end, verify_workflow):
        sql = """select count(*)
		from V_DS_TotalInfo_based_on_SolutionRiskInfo
		where VerifyWorkFlow in %s
		and (TestDate_E is not null and TestDate_M is not null)
		and 
		(TestDate_E between '%s' and '%s' 
		and TestDate_M between '%s' and '%s')""" % (verify_workflow, start, end, start, end)
        return self.cursor.execute(sql).fetchall()

    # 通过时间还有筛查流程状态查询出有两次检查的人的数据（测试日期只需要有一个在日期范围内）
    def query_time_workflow_any(self, start, end, verify_workflow):
        sql = """select CheckNo, SolutionRiskSerialID, PatientSerialID,
						EarlySampleSerialID, MiddleSampleSerialID, PregnantSerialID,
						GestationWeek_E, GestationWeek_M,
						GestationDay_E, GestationDay_M,
						GestationType_E, GestationType_M
						from V_DS_TotalInfo_based_on_SolutionRiskInfo
						where VerifyWorkFlow in %s
						and (TestDate_E is not null and TestDate_M is not null)
						and 
						(TestDate_E between '%s' and '%s' 
						or TestDate_M between '%s' and '%s')
		union
				select CheckNo, SolutionRiskSerialID, PatientSerialID,
					EarlySampleSerialID, MiddleSampleSerialID, PregnantSerialID,
					GestationWeek_E, GestationWeek_M,
					GestationDay_E, GestationDay_M,
					GestationType_E, GestationType_M
					from V_DS_TotalInfo_based_on_SolutionRiskInfo
					where VerifyWorkFlow in %s
					and (TestDate_E is null or TestDate_M is null)
					and (TestDate_E between '%s' and '%s' 
					or TestDate_M between '%s' and '%s')""" % (
            verify_workflow, start, end, start, end, verify_workflow, start, end, start, end)
        return self.cursor.execute(sql).fetchall()

    # 通过时间还有筛查流程状态查询出有两次检查的人的数据（早期和中期测试日期必须都在日期范围内）
    def query_time_workflow_all(self, start, end, verify_workflow):
        sql = """select CheckNo, SolutionRiskSerialID, PatientSerialID,
						EarlySampleSerialID, MiddleSampleSerialID, PregnantSerialID,
						GestationWeek_E, GestationWeek_M,
						GestationDay_E, GestationDay_M,
						GestationType_E, GestationType_M
						from V_DS_TotalInfo_based_on_SolutionRiskInfo
						where VerifyWorkFlow in %s
						and (TestDate_E is not null and TestDate_M is not null)
						and 
						(TestDate_E between '%s' and '%s' 
						and TestDate_M between '%s' and '%s')
		union
				select CheckNo, SolutionRiskSerialID, PatientSerialID,
					EarlySampleSerialID, MiddleSampleSerialID, PregnantSerialID,
					GestationWeek_E, GestationWeek_M,
					GestationDay_E, GestationDay_M,
					GestationType_E, GestationType_M
					from V_DS_TotalInfo_based_on_SolutionRiskInfo
					where VerifyWorkFlow in %s
					and (TestDate_E is null or TestDate_M is null)
					and (TestDate_E between '%s' and '%s' 
					or TestDate_M between '%s' and '%s')""" % (
            verify_workflow, start, end, start, end, verify_workflow, start, end, start, end)
        return self.cursor.execute(sql).fetchall()

    # 根据solutionRiskSerialID去查找拼串
    def query_parameterList(self, solutionRiskSerialID):
        sql = """select ParameterList 
		from WOR_DS_SolutionRiskInfo 
		where SolutionRiskSerialID = %s""" % (solutionRiskSerialID)
        return self.cursor.execute(sql).fetchall()

    # 查找NT对应的中位数版本和中位数值
    def query_NT_MedianValue(self, sampleSerialID, checkTypeID):
        sql = """select CheckValue, CheckValueOne, CheckValueTwo
		from WOR_DS_CheckGestationInfo
		where SampleSerialID = %s
		and CheckTypeID = %s""" % (sampleSerialID, checkTypeID)
        return self.cursor.execute(sql).fetchall()

    # 查询母版本的中位数版本号和中位数值
    def query_mather_medianValue(self, median_VerNo, test_itemID, gestation_week):
        sql = """select MedianValue, MedianVerNo
				from BSC_DS_GestationMedian 
				where GestationWeekType = 0 
				and MedianVerNo = %d
				and TestItemID = %s
				and GestationWeek = %s""" % (median_VerNo, test_itemID, gestation_week)
        return self.cursor.execute(sql).fetchall()

    # 特殊：查询母版本的双胞胎NT中位数版本值
    def query_NT_medianValue(self, medianVerNo, test_itemID, gestation_type, gestation_week1):
        sql = """select MedianValue, MedianVerNo
				from BSC_DS_GestationMedian 
				where GestationWeekType = 0 
				and MedianVerNo = %d
				and TestItemID = %s
				and GestationType = %d
				and GestationWeek = %s
		union
				select MedianValue, MedianVerNo
				from BSC_DS_HistoryMedian 
				where GestationWeekType = 0 
				and MedianVerNo = %d
				and TestItemID = %s
				and GestationType = %d
				and GestationWeek = %s""" % (medianVerNo, test_itemID, gestation_type, gestation_week1, medianVerNo, test_itemID, gestation_type, gestation_week1)
        return self.cursor.execute(sql).fetchall()

    # 查找对应的版本，标记物和孕周天数，孕周类型去找对应的中位数值
    def query_MedianValue(self, medianVerNo, test_itemID, gestation_type, gestation_week):
        sql = """select MedianValue, MedianVerNo
				from BSC_DS_GestationMedian 
				where GestationWeekType = 0 
				and MedianVerNo = %s
				and TestItemID = %s
				and GestationType = %d
				and GestationWeek = %s
		union 
				select MedianValue, MedianVerNo
				from BSC_DS_HistoryMedian 
				where GestationWeekType = 0 
				and MedianVerNo = %s
				and TestItemID = %s
				and GestationType = %d
				and GestationWeek = %s""" % (medianVerNo, test_itemID, gestation_type, gestation_week, medianVerNo, test_itemID, gestation_type, gestation_week)
        return self.cursor.execute(sql).fetchall()

    # 跟新WOR_DS_TestInfo表中的MedianValue和MedianVerNo
    def update_testInfo(self, mom_value, median_no, median_value, test_item_id, sampleSerialID):
        sql = """UPDATE WOR_DS_TestInfo 
		SET  ResultMOM = %s, MedianVerNo = %d, MedianValue = %s
		WHERE TestItemID = %d
		and SampleSerialID = %d""" % (mom_value, median_no, median_value, test_item_id, sampleSerialID)
        return self.cursor.execute(sql)

    # 根据sampleSerialID查询旧的中位数版本，中位数值
    def query_testInfo(self, sampleSerialID, test_item):
        sql = """select MedianVerNo, MedianValue, ResultMOM
		from WOR_DS_TestInfo 
		WHERE SampleSerialID = %d
		and TestItemID = % s""" % (sampleSerialID, test_item)
        return self.cursor.execute(sql).fetchall()

    # 当VerifyWorkFlow为0时，更新为1
    def update_VerifyWorkFlow(self, solutionRiskSerialID):
        sql = """UPDATE WOR_DS_SolutionRiskInfo 
		SET VerifyWorkFlow = 1
		WHERE SolutionRiskSerialID = %s
		and VerifyWorkFlow = 0""" % (solutionRiskSerialID)
        return self.cursor.execute(sql)

    # 查询风险计算时，阻断值是否带有符号
    def query_RiskEqualSign(self):
        sql = """SELECT ParameterValue
				FROM BSC_DS_Parameter
				WHERE ParameterStr = 'EvaluationAnnotation_RiskEqualSign'"""
        return self.cursor.execute(sql).fetchall()

    # 获取各个阻断值
    def query_all_cuff(self, solutionRiskSerialID):
        sql = """select DownsCuff, DownsGrayCuff,
	   					ONTDCuff, ONTDGrayCuff, ONTDCuffType,
	   					TrisomyCuff, TrisomyGrayCuff
				from WOR_DS_SolutionRiskInfo
				where SolutionRiskSerialID = %d""" % (solutionRiskSerialID)
        return self.cursor.execute(sql).fetchall()

    # 更新各个风险值、拼串、总体风险等，更新到WOR_DS_SolutionRiskInfo
    def updata_all_risk(self, DownsResult, ONTDResult, TrisomyResult, ChildBirthdayDateAgeRisk,
                        DownsResult1, DownsResult2, TrisomyResult1, TrisomyResult2,
                        ChildBirthdayDateAgeRiskTrisomy, ParameterList, OverallRisk, SolutionRiskSerialID):
        sql = """update WOR_DS_SolutionRiskInfo
		SET DownsResult = %s,
			ONTDResult = %s,
			TrisomyResult = %s,
			ChildBirthdayDateAgeRisk = %s,
			DownsResult1 = %s,
			DownsResult2 = %s,
			TrisomyResult1 = %s,
			TrisomyResult2 = %s,
			ChildBirthdayDateAgeRiskTrisomy = %s,
			ParameterList = '%s',
			OverallRisk = '%s'
		WHERE SolutionRiskSerialID = %s""" % (DownsResult, ONTDResult, TrisomyResult,
                                              ChildBirthdayDateAgeRisk, DownsResult1,
                                              DownsResult2, TrisomyResult1, TrisomyResult2,
                                              ChildBirthdayDateAgeRiskTrisomy, ParameterList,
                                              OverallRisk, SolutionRiskSerialID)
        return self.cursor.execute(sql)

    # 查询WOR_DS_SolutionRiskInfo的OverallRisk
    def query_over_all_risk(self, solutionRiskSerialID):
        sql = """select OverallRisk
				from WOR_DS_SolutionRiskInfo
				where SolutionRiskSerialID = %s""" % (solutionRiskSerialID)
        return self.cursor.execute(sql).fetchall()

    # 查询体重校正参数
    def query_weight_parameters(self):
        sql = """SELECT ParameterStr, ParameterValue, PVerNo, PVerDate, UseNumber, Description
                 FROM BSC_DS_Parameter
                 WHERE (ParameterStr LIKE '%TemplateForDowns_%weighttformula_%') 
                 OR (ParameterStr LIKE '%weighttype%') 
                 AND (ParameterStr NOT LIKE '%WeightCorrection%') 
                 AND (ParameterStr NOT LIKE '%TemplateForDowns_NT_Earlyweight%') """
        return self.cursor.execute(sql).fetchall()



# 当数据库中没有拼串时
    # 查询筛查方案
    def query_screening_plan(self, solutionRiskSerialID):
        sql = """select SolutionTypeID
                 from WOR_DS_SolutionRiskInfo
                 where SolutionRiskSerialID = '%s'""" % solutionRiskSerialID
        return self.cursor.execute(sql).fetchall()

    # 查询第一段拼串缺少的值
    def no_query_r11(self, solutionRiskSerialID):
        sql = """select TestItems, DownsCritical, 
                        TrisomyCritical, ONTDCritical,
                        ONTDCriticalType, PatuaCritical,
		                USELimit, USETwoTrisomyRisk
                 from BSC_DS_Solution
                 where SolutionID = (select SolutionID 
					                 from WOR_DS_SolutionRiskInfo
					                 where SolutionRiskSerialID = '%s')""" % solutionRiskSerialID
        return self.cursor.execute(sql).fetchall()

    # 查询孕妇的肤色
    def query_people_color(self, patientSerialID):
        sql = """select RaceType 
                 from WOR_DS_PatientInfo
                 where PatientSerialID = %s""" % patientSerialID
        return self.cursor.execute(sql).fetchall()

    # 查询预产期年龄
    def query_premature_age(self, sampleSerialID):
        sql = """select ChildBirthDateAge, Weight, SamplingDate,
                 GestationWeek, GestationDay
                 from WOR_DS_SampleInfo
                 where SampleSerialID = %s """ % sampleSerialID
        return self.cursor.execute(sql).fetchall()

    # 查询r16从31到36
    def query_r16_31_36(self, pregnantSerialID):
        sql = """select Diabetes, FetalNumber, IVF, SmokeHistory, DownsHistory
                 from WOR_DS_PregnantInfo
                 where PregnantSerialID = %s""" % pregnantSerialID
        return self.cursor.execute(sql).fetchall()

    # 查询CRL日孕周
    def query_CRL_weekday(self, sampleSerialID, CheckTypeID):
        sql = """select CheckDate
                 from WOR_DS_CheckGestationInfo
                 where SampleSerialID = '%s'
                 and CheckTypeID = '%s'""" % (sampleSerialID, CheckTypeID)
        return self.cursor.execute(sql).fetchall()

    # 获取标记物测量值
    def query_item_value(self, sampleSerialID, testItem):
        sql = """select Result
        		from WOR_DS_TestInfo 
        		WHERE SampleSerialID = %d
        		and TestItemID = % s""" % (sampleSerialID, testItem)
        return self.cursor.execute(sql).fetchall()

    # 获取中位数小数位数
    def query_median_points(self, testItem):
        sql = """SELECT DefaultMedianDecimal
                 FROM BSC_TestItem
                 where TestItemID = %s""" % testItem
        return self.cursor.execute(sql).fetchall()

# 当标记物为7号时，


# CONVERT (CHAR(10), BirthDate, 120) as  BirthDate,


if __name__ == "__main__":
    con = QueryData()
    con.connect("{SQL Server}", "DESKTOP-SM51UF2\\MOZZIE", "Mozzie", "john", "1234")

    test = datetime.date(con.query_premature_age(24)[0].TestDate).day
    con.query_CRL_weekday(24, 2)[0].CheckDate

#
# list = con.master_version_query()
# for i in list:
# 	print(i.date)
# 	def version_query(self):
# 		sql = sql = '''select MedianVerNo, TestItemID, GestationType, MedianVerDate from BSC_DS_MedianVerInfo'''
# 		return self.cursor.execute(sql).fetchall()

# # def connect(driver="{SQL Server}",
# # 			server = 'DESKTOP-SM51UF2\MOZZIE',
# # 			databaseName="Mozzie",
# # 			user="john",
# # 			password="1234"):
# # 	connect = pyodbc.connect(p_str="mozzie", autocommit=True, DRIVER=driver, SERVER=server, DATABASE=databaseName, UID=user, PWD=password)
# # 	return connect
# #
# # sql = '''select MedianVerNo, TestItemID, GestationType, MedianVerDate from BSC_DS_MedianVerInfo'''
# # connect().cursor().execute(sql).fetchall()
# query = QueryString()
# print(query.connect_to_sercer())

# conn = pyodbc.connect(DRIVER='{SQL Server}',
# 					  SERVER="DESKTOP-SM51UF2\MOZZIE",
# 					  DATABASE='Mozzie',
# 					  UID="john",
# 					  PWD="1234")
# cursor = conn.cursor()
# cursor.execute('''select * from BSC_DS_MedianVerInfo''')
# print(cursor.fetchall())
#
# conn.close()

# sql = "select @@version"
# print(cursor.execute(sql))
