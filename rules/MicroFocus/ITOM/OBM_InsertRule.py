# -*- coding: utf-8 -*-

import re
from datetime import datetime
from module.tools.InsertTools import ReadFileTemplate
from rules.MicroFocus.ITOM.OBM_SQLTable import FileHash
if __name__ != "__main__":
    from module.tools.AppDebug import MultSQLLogger

class OBMFiles(ReadFileTemplate):
    """
    MicroFocus ITOM OBM 文件解析类
    """
    def __init__(self, TaskInfo, QData=None):
        # 继承父类的方法和属性
        super().__init__()
        # 从 TaskInfo 中获取相关数据
        self.TaskInfo = TaskInfo
        self.file = self.TaskInfo.get("file")
        # 模块模式下, 继续获取下列信息
        if __name__ != "__main__":
            self.targetdb = self.TaskInfo.get("targetdb")
            self.company = self.TaskInfo.get("company")
            self.productline = self.TaskInfo.get("productline")
            self.product = self.TaskInfo.get("product")
            self.total = self.TaskInfo.get("total")
        # 处理的实际逻辑
        data = self.classifiles()
        # 将处理完成的数据放到队列中
        if __name__ != "__main__":
            QData.put(data)

    def classifiles(self):
        """
        针对 OBM 文件进行分类, 然后在做后续处理
        :return:
        """
        if re.findall("opr-gateway\.log|opr-scripting-host\.log|opr-configserver\.log|opr-svcdiscserver\.log|opr-heartbeat\.log|opr-backend\.log|opr-ciresolver\.log|scripts\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type1()
        elif re.findall("opr-gateway-flowtrace\.log|opr-flowtrace-backend\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type2()
        elif re.findall("opr-webapp\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type3()
        elif re.findall("opr-ws-response\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type4()
        elif re.findall("user_stats_log_filter\.log|login\.log|nanny_all\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type5()
        elif re.findall("opr-svcdiscserver-citrace\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type6()
        elif re.findall("pmi\.log|bvd\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type7()
        elif re.findall("downtime\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type8()
        elif re.findall("opr-clis\.log|bus\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type9()
        elif re.findall("cmdb\.reconciliation\.datain\.merged.*log", self.file, re.IGNORECASE):
            return self.readlog_obm_rtsm1()
        elif re.findall("cmdb\.reconciliation\.datain\.ignored.*log", self.file, re.IGNORECASE):
            return self.readlog_obm_rtsm2()
        elif re.findall("cmdb\.reconciliation\.error.*log", self.file, re.IGNORECASE):
            return self.readlog_obm_rtsm3()
        elif re.findall("UserActions.servlets\.log", self.file, re.IGNORECASE):
            return self.readlog_UserActions_Servlets()
        elif re.findall("wrapper\.log", self.file, re.IGNORECASE):
            return self.readlog_wrapper()
        elif re.findall("jvm_statistics\.log", self.file, re.IGNORECASE):
            return self.readlog_jvm_statistics()
        elif re.findall("opr-checker-xml\.txt", self.file, re.IGNORECASE):
            return self.readcfg_opr_checker()
        elif re.findall("OvSvcDiscServer\.log", self.file, re.IGNORECASE):
            return self.readlog_ovsvcdiscserver()

    def readlog_obm_type1(self):
        """
        OBM logs
        # opr-gateway.log
        # opr-scripting-host.log
        # opr-configserver.log
        # opr-svcdiscserver.log
        # opr-heartbeat.log
        # opr-backend.log
        # opr-ciresolver.log
        # scripts.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            log_time = self.get_logtime(line.split("[", 1)[0].strip())
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split("[")[0].strip())
                    log_level = log_data[0].split(" ", 4)[3]
                    log_comp = log_data[0].split(" ", 4)[4].split("-", 1)[0].strip()
                    # 针对 opr-backend.log 的额外处理
                    if log_level not in ["TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"]:
                        log_level = log_data[0].split("] ", 1)[-1].strip().split(" ", 1)[0]
                        log_comp = log_data[0].split("] ", 1)[-1].strip().split(" - ", 1)[0].strip().split(" ", 1)[-1]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            #
            if re.findall("opr-gateway\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_Gateway as OBMTable
            elif re.findall("opr-scripting-host\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_Scripting_Host as OBMTable
            elif re.findall("opr-configserver\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_ConfigServer as OBMTable
            elif re.findall("opr-svcdiscserver\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_SvcDiscserver as OBMTable
            elif re.findall("opr-heartbeat\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_HeartBeat as OBMTable
            elif re.findall("opr-backend\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_Backend as OBMTable
            elif re.findall("opr-ciresolver\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_CIResolver as OBMTable
            elif re.findall("scripts\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import Scripts as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_type2(self):
        """
        OBM logs
        # opr-gateway-flowtrace.log
        # opr-flowtrace-backend.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                str_time = line.split(" ", 2)[0].strip() + " " + line.split(" ", 2)[1].strip()
            except:
                str_time = "Null"
            log_time = self.get_logtime(str_time)
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" ", 2)[0].strip() + " " + log_data[0].split(" ", 2)[1].strip())
                    log_level = log_data[0].split(" ", 3)[2].strip()
                    log_comp = log_data[0].split(" ", 3)[-1].split(": ", 1)[0].strip()

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(": ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":

            if re.findall("opr-gateway-flowtrace\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_Gateway_Flowtrace as OBMTable
            if re.findall("opr-flowtrace-backend\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_Backend_Flowtrace as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_type3(self):
        """
        OBM logs
        # opr-webapp.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            log_time = self.get_logtime(line.split("[", 1)[0].strip())
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split("[")[0].strip())
                    log_level = log_data[0].split("] ", 1)[-1].split(" ", 1)[0]
                    log_comp = log_data[0].split("] ", 1)[-1].split(" ", 1)[-1].split(" - ", 1)[0]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            #
            if re.findall("opr-webapp\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_WebApp as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_type4(self):
        """
        OBM logs
        # opr-ws-response.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split(" ", 3)[0].strip() + " " + line.split(" ", 3)[1].strip())
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" ", 3)[0].strip() + " " + log_data[0].split(" ", 3)[1].strip())
                    log_level = log_data[0].split(" - ", 1)[0].split(" ")[-1]
                    log_comp = log_data[0].split(" - ", 1)[-1].split(":", 1)[0]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 1)[-1].split(":", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            #
            if re.findall("opr-ws-response\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_WS_Response as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_type5(self):
        """
        OBM logs
        # user_stats_log_filter.log
        # login.log
        # nanny_all.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split(" ", 3)[0].strip() + " " + line.split(" ", 3)[1].strip())
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" ", 3)[0].strip() + " " + log_data[0].split(" ", 3)[1].strip())
                    log_level = log_data[0].split(" - ", 1)[0].strip().split(" ")[-1]
                    log_comp = "[" + log_data[0].split(" [", 1)[-1].split(") ", 1)[0] + ")"

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":

            if re.findall("user_stats_log_filter\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import User_Stats_Log_Filter as OBMTable
            elif re.findall("login\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import Login as OBMTable
            elif re.findall("nanny_all\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import Nanny_All as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_type6(self):
        """
        OBM logs
        # opr-svcdiscserver-citrace.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split(" ", 3)[0].strip() + " " + line.split(" ", 3)[1].strip())
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" ", 3)[0].strip() + " " + log_data[0].split(" ", 3)[1].strip())
                    log_level = log_data[0].split(" - ", 1)[0].split(" ", 2)[-1].strip()
                    log_comp = log_data[0].split(" - ", 1)[-1].split(":", 1)[0]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            #
            if re.findall("opr-svcdiscserver-citrace\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_SvcDiscserver_CITrace as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_type7(self):
        """
        OBM logs
        # pmi.log
        # bvd.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split("[", 1)[0].strip())
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split("[", 1)[0].strip())
                    log_level = log_data[0].split("]", 1)[-1].split(":", 1)[0].strip()
                    log_comp = log_data[0].split(" -> ", 1)[0].split("]", 1)[-1].split(": ", 1)[-1]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" -> ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            #
            if re.findall("pmi\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import PMI as OBMTable
            elif re.findall("bvd\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import BVD as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_type8(self):
        """
        OBM logs
        # downtime.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split(" ", 3)[0].strip() + " " + line.split(" ", 3)[1].strip())
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" ", 3)[0].strip() + " " + log_data[0].split(" ", 3)[1].strip())
                    log_level = log_data[0].split(" - ", 1)[0].strip().split(" ")[-1]
                    log_comp = "["+ log_data[0].split(" [", 1)[-1].split(") ", 1)[0] + ")"

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            #
            if re.findall("downtime\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import DownTime as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_type9(self):
        """
        OBM Logs
        # opr-clis.log
        # bus.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split("[", 1)[0].strip())
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split("[", 1)[0].strip())
                    log_level = log_data[0].split("]", 1)[-1].strip().split(" ", 1)[0]
                    log_comp = log_data[0].split(" - ")[0].split(" ")[-1]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont, })
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":

            if re.findall("opr-clis\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_CLIS as OBMTable
            elif re.findall("bus\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import BUS as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_rtsm1(self):
        """
        OBM RTSM.sql Logs
        # cmdb.reconciliation.datain.merged.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split(" ", 3)[0] + " " + line.split(" ", 3)[1])
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" ", 3)[0] + " " + log_data[0].split(" ", 3)[1])
                    log_level = log_data[0].split(" ", 4)[3].strip()
                    log_comp = re.findall("\[.*\]", log_data[0], re.IGNORECASE)[0]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 2)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont, })
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            if re.findall("cmdb\.reconciliation\.datain\.merged.*log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import CMDB_Reconciliation_Datain_Merged as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_rtsm2(self):
        """
        OBM RTSM.sql Logs
        # cmdb.reconciliation.datain.ignored.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split(" ", 3)[0] + " " + line.split(" ", 3)[1])
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" ", 3)[0] + " " + log_data[0].split(" ", 3)[1])
                    log_level = log_data[0].split(" ", 4)[3].strip()
                    log_comp = re.findall("\[.*\]", log_data[0], re.IGNORECASE)[0]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(" - ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont, })
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            if re.findall("cmdb\.reconciliation\.datain\.ignored.*log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import CMDB_Reconciliation_Datain_Ignored as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_obm_rtsm3(self):
        """
        OBM RTSM.sql Logs
        # cmdb.reconciliation.error.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split(" ", 3)[0] + " " + line.split(" ", 3)[1])
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" ", 3)[0] + " " + log_data[0].split(" ", 3)[1])
                    log_level = log_data[0].split(" ", 4)[3].strip()
                    log_comp = "[" + log_data[0].split(": ", 1)[0].split("[", 1)[-1]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(": ", 1)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont, })
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            if re.findall("cmdb\.reconciliation\.error.*log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import CMDB_Reconciliation_Error as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_UserActions_Servlets(self):
        """
        OBM UserActions.servlets.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split("|", 1)[-1].split("|", 1)[0])
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split("|", 1)[-1].split("|", 1)[0])
                    # UserActions.servlets.log 没有等级关键字, 直接根据经验抓取
                    if re.findall("FAILED", log_data[0], re.IGNORECASE):
                        log_level = "ERROR"
                    else:
                        log_level = "INFO"
                    log_comp = log_data[0].split("|", 5)[0] + "_" + log_data[0].split("|", 5)[2] + "_" + log_data[0].split("|", 5)[3]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split("|", 2)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            #
            if re.findall("UserActions.servlets\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import UserActions_Servlets as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_wrapper(self):
        """
        OBM wrapper.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split("|", 3)[-2].strip())
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split("|", 3)[-2].strip())
                    log_level = log_data[0].split("|", 1)[0].strip()
                    log_comp = log_data[0].split("|", 2)[1]

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split("|", 3)[-1].strip()
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":

            if re.findall("wrapper\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import Wrapper as OBMTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_jvm_statistics(self):
        """
        OBM jvm_statistics.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                log_time = self.get_logtime(line.split(" - ", 1)[0].strip().split(" ")[0] + " " + line.split(" - ", 1)[0].strip().split(" ")[1])
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    log_time = self.get_logtime(log_data[0].split(" - ", 1)[0].strip().split(" ")[0] + " " + log_data[0].split(" - ", 1)[0].strip().split(" ")[1])
                    heap_info = log_data[0].split("- HEAP -", 1)[-1].split(";", 1)[0].strip()
                    heap_used = heap_info.split(",")[0].split(":")[-1].strip()
                    heap_commit = heap_info.split(",")[1].split(":")[-1].strip()
                    heap_max = heap_info.split(",")[2].split(":")[-1].strip()
                    heap_free = heap_info.split(":")[-1].split("]")[0].strip()
                    non_heap_info = log_data[0].split("NON-HEAP -", 1)[-1].split(";", 1)[0].strip()
                    non_heap_used = non_heap_info.split(",")[0].split(":")[-1].strip()
                    non_heap_commit = non_heap_info.split(",")[1].split(":")[-1].strip()
                    non_heap_max = non_heap_info.split(",")[2].split(":")[-1].strip()
                    non_heap_free = non_heap_info.split(":")[-1].split("]")[0].strip()

                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "heap_used": heap_used,
                        "heap_commit": heap_commit,
                        "heap_max": heap_max,
                        "heap_free": heap_free,
                        "non_heap_used": non_heap_used,
                        "non_heap_commit": non_heap_commit,
                        "non_heap_max": non_heap_max,
                        "non_heap_free": non_heap_free,
                    })
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            from rules.MicroFocus.ITOM.OBM_SQLTable import JVM_Statistics as OBMTable
            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    heap_used=data.get("heap_used"),
                    heap_commit=data.get("heap_commit"),
                    heap_max=data.get("heap_max"),
                    heap_free=data.get("heap_free"),
                    non_heap_used=data.get("non_heap_used"),
                    non_heap_commit=data.get("non_heap_commit"),
                    non_heap_max=data.get("non_heap_max"),
                    non_heap_free=data.get("non_heap_free"),
                ))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_ovsvcdiscserver(self):
        """
        OBM logs
        # OvSvcDiscServer.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            try:
                date = line.split("]")[0].split("[")[-1].split(" ")
                log_time = self.get_logtime(date[0] + " " + date[1] + " " + date[2] + " " + date[3] + " " + date[5])
            except:
                log_time = "Null"
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    logdate = log_data[0].split("]")[0].split("[")[-1].split(" ")
                    log_time = self.get_logtime(logdate[0] + " " + logdate[1] + " " + logdate[2] + " " + logdate[3] + " " + logdate[5])
                    log_level = "INFO"
                    log_comp = "[" + log_data[0].split("] ", 1)[0].split("[", 2)[-1] + "]"

                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split("] ", 1)[-1].strip()
                    if re.findall("error|Exception", log_cont, re.IGNORECASE):
                        log_level = "ERROR"
                    # 将字典数据加入到 FList 中
                    FList.append({
                        "log_line": log_line,
                        "log_time": log_time,
                        "log_level": log_level,
                        "log_comp": log_comp,
                        "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            from rules.MicroFocus.ITOM.OBM_SQLTable import OvSvcDiscServer as OBMTable
            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OBMTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readcfg_opr_checker(self):
        """
        OBM opr-checker-xml.txt 文件解析函数
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        SList = []
        hostname = "Null"
        domain = "Null"
        os = "Null"
        memory = "Null"
        obm_version = "Null"
        obm_ipaddress = "Null"
        obm_install_patch = "Null"
        obm_install_hotfix = "Null"
        ipaddress = []
        obm_patch = []
        obm_hotfx = []
        try:
            # 读取相关数据
            with open(self.file, mode="r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if re.findall("<hostname>(.*?)</hostname>", line):
                        hostname = re.findall("<hostname>(.*?)</hostname>", line)[0]
                    elif re.findall("<domain>(.*?)</domain>", line):
                        domain = re.findall("<domain>(.*?)</domain>", line)[0]
                    elif re.findall("<os>(.*?)</os>", line):
                        os = re.findall("<os>(.*?)</os>", line)[0]
                    elif re.findall("<physical_memory>(.*?)</physical_memory>", line):
                        memory = str(re.findall("<physical_memory>(.*?)</physical_memory>", line)[0])
                    elif re.findall("<ip_address>(.*?)</ip_address>", line):
                        ipaddress.append(re.findall("<ip_address>(.*?)</ip_address>", line)[0])
                    elif re.findall("<OfficialRelease>(.*?)</OfficialRelease>", line):
                        obm_version = re.findall("<OfficialRelease>(.*?)</OfficialRelease>", line)[0]
                    elif re.findall("<Patch>(.*?)</Patch>", line):
                        obm_patch.append(re.findall("<Patch>(.*?)</Patch>", line)[0])
                    elif re.findall("<Hotfix>(.*?)</Hotfix>", line):
                        obm_hotfx.append(re.findall("<Hotfix>(.*?)</Hotfix>", line)[0])

            # 整理相关数据
            if len(ipaddress) != 0:
                obm_ipaddress = ""
                for ip in ipaddress:
                    obm_ipaddress += ip + "\n"
                obm_ipaddress = obm_ipaddress[:-1]

            if len(obm_patch) != 0:
                obm_install_patch = ""
                for patch in obm_patch:
                    obm_install_patch += patch + "\n"
                obm_install_patch = obm_install_patch[:-1]

            if len(obm_hotfx) != 0:
                obm_install_hotfix = ""
                for hotfix in obm_hotfx:
                    obm_install_hotfix += hotfix + "\n"
                obm_install_hotfix = obm_install_hotfix[:-1]


            # 模块模式下, 将数据转换为 SQLAlchemy 类型的数据类型, 并保存在 SList 中
            if __name__ != "__main__":
                from rules.MicroFocus.ITOM.OBM_SQLTable import OBM_Summary
                file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
                SList.append(OBM_Summary(file_id=file_id, key=hostname + "." + "OS", value=os))
                SList.append(OBM_Summary(file_id=file_id, key=hostname + "." + "Version", value=obm_version))
                SList.append(OBM_Summary(file_id=file_id, key=hostname + "." + "Memory", value = memory))
                SList.append(OBM_Summary(file_id=file_id, key=hostname + "." + "IPs", value = obm_ipaddress))
                SList.append(OBM_Summary(file_id=file_id, key=hostname + "." + "Patchs", value=obm_install_patch))
                SList.append(OBM_Summary(file_id=file_id, key=hostname + "." + "Hotfix", value=obm_install_hotfix))
        except Exception as e:
            # 模块模式
            if __name__ != "__main__":
                MultSQLLogger.error(e)
            # 测试模式
            else:
                print(e)

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印获取的数据
        else:
            print("====== FQDN ======")
            print(hostname + domain)
            print("====== OS ======")
            print(os)
            print("====== Memory ======")
            print(memory)
            print("====== IPs ======")
            print(obm_ipaddress)
            print("====== OBM Version ======")
            print(obm_version)
            print("====== OBM Patchs ======")
            print(obm_install_patch)
            print("====== OBM Hotfix ======")
            print(obm_install_hotfix)

if __name__ == "__main__":
    # 读取测试文件
    file = r"D:\ucmdb\runtime\log\cmdb.reconciliation.error.log"
    test = OBMFiles({"file": file})
