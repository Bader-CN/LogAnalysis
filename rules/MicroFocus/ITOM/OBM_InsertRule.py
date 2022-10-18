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
        if re.findall("opr-gateway\.log|opr-scripting-host\.log|opr-configserver\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type1()
        elif re.findall("opr-gateway-flowtrace\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type2()
        elif re.findall("opr-webapp\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type3()

    def readlog_obm_type1(self):
        """
        OBM logs
        # opr-gateway.log
        # opr-scripting-host.log
        # opr-configserver.log
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
            #
            if re.findall("opr-gateway-flowtrace\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OBM_SQLTable import OPR_Gateway_Flowtrace as OBMTable

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

if __name__ == "__main__":
    # 读取测试文件
    file = r"C:\OBMLogs\opr-webapp.log"
    test = OBMFiles({"file": file})
