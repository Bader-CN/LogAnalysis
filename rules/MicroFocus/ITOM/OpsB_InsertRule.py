# -*- coding: utf-8 -*-

import re
from datetime import datetime
from module.tools.InsertTools import ReadFileTemplate
from rules.MicroFocus.ITOM.OpsB_SQLTable import FileHash
if __name__ != "__main__":
    from module.tools.AppDebug import MultSQLLogger

class OpsBFiles(ReadFileTemplate):
    """
    MicroFocus ITOM OpsB 文件解析类
    """
    def __init__(self, TaskInfo, QData=None):
        # 继承父类的方法和属性
        super().__init__()
        # 从 TaskInfo 中获取相关数据
        self.TaskInfo = TaskInfo
        self.file = self.TaskInfo.get("file")
        self.encoding = self.get_file_encoding(self.file)
        # 模块模式下, 继续获取下列信息
        if __name__ != "__main__":
            self.targetdb = self.TaskInfo.get("targetdb")
            self.company = self.TaskInfo.get("company")
            self.productline = self.TaskInfo.get("productline")
            self.product = self.TaskInfo.get("product")
            self.total = self.TaskInfo.get("total")
        # 如果匹配到此内容, 则改行不做任何处理
        self.blkline = []
        # 处理的实际逻辑
        data = self.classifiles()
        # 将处理完成的数据放到队列中
        if __name__ != "__main__":
            QData.put(data)

    def classifiles(self):
        """
        针对 OpsB 文件进行分类, 然后在做后续处理
        :return:
        """
        if re.findall("administration\.log|administration-audit\.log|dataaccess\.log|metadata-server-app\.log|taskcontroller\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_itom_di_type1()
        elif re.findall("aggregate\.log|csv-direct-load\.log|forecast\.log|perl-task\.log|taskexecutor\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_itom_di_type2()
        elif re.findall("receiver-itom-di-receiver-dpl.*\.log|receiver-out\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_itom_di_type3()
        elif re.findall("scheduler\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_itom_di_type4()
        elif re.findall("idm-loader\.log|idm-service\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_itom_idm_type1()

    def readlog_opsb_itom_di_type1(self):
        """
        # administration.log
        # administration-audit.log
        # dataaccess.log
        # metadata-server-app.log
        # taskcontroller.log
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
        with open(self.file, mode="r", encoding=self.encoding, errors="replace") as file:
            for line in file:
                DList.append(line.strip())

        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            # 判断该行是否是日志的开头
            try:
                log_time_str = line.split(" ", 2)[0] + " " + line.split(" ", 2)[1]
                log_time = self.get_logtime(log_time_str)
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
                    # 日志时间
                    log_time = self.get_logtime(log_data[0].split(" ", 2)[0] + " " + log_data[0].split(" ", 2)[1])
                    # 日志等级
                    log_level = log_data[0].split(" ")[3].strip()
                    if log_level not in ["INFO", "WARN", "ERROR", "DEBUG"]:
                        log_level = log_data[0].split(" ")[2].strip()
                    # 日志组件
                    log_comp = re.findall("\[.*?]", log_data[0], re.IGNORECASE)[0]
                    # 日志内容
                    log_cont = ""
                    for line in log_data:
                        if line.strip() not in self.blkline:
                            log_cont += line + "\n"
                    log_cont = log_cont.split(log_comp, 1)[-1][1:].strip()

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
            # 针对文件做进一步分析, 来判断加载哪一个 SQL 表
            if re.findall("administration\.log|administration-audit\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Administration as OpsBTable
            elif re.findall("dataaccess\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Data_Access_DPL as OpsBTable
            elif re.findall("metadata-server-app\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Metadata_Server as OpsBTable
            elif re.findall("taskcontroller\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Postload_TaskController as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                try:
                    SList.append(OpsBTable(
                        file_id=file_id,
                        log_line=data.get("log_line"),
                        log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                        log_level=data.get("log_level"),
                        log_comp=data.get("log_comp"),
                        log_cont=data.get("log_cont")))
                except Exception as e:
                    MultSQLLogger.error(e)
                    MultSQLLogger.error("Faild File: " + self.file)
                    MultSQLLogger.error("Faild Line: " + line)

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_opsb_itom_di_type2(self):
        """
        # aggregate.log
        # csv-direct-load.log
        # forecast.log
        # perl-task.log
        # taskexecutor.log
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
        with open(self.file, mode="r", encoding=self.encoding, errors="replace") as file:
            for line in file:
                DList.append(line.strip())

        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            # 判断该行是否是日志的开头
            try:
                log_time_str = line.split(" ", 2)[0] + " " + line.split(" ", 2)[1]
                log_time = self.get_logtime(log_time_str)
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
                    # 日志时间
                    log_time = self.get_logtime(log_data[0].split(" ", 2)[0] + " " + log_data[0].split(" ", 2)[1])
                    # 日志等级
                    log_level = "Null"
                    for level in ["INFO", "WARN", "ERROR", "DEBUG"]:
                        if level in log_data[0]:
                            log_level = level
                            break
                    if log_level == "Null":
                        log_level = "INFO"
                    # 日志组件
                    if re.findall("\[TFID.*TID.*RID.*?\]", log_data[0], re.IGNORECASE):
                        log_comp = re.findall("\[TFID.*TID.*RID.*?\]", log_data[0], re.IGNORECASE)[0]
                    else:
                        log_comp = re.findall("\[.*?]", log_data[0], re.IGNORECASE)[0]
                    # 日志内容
                    log_cont = ""
                    for line in log_data:
                        if line.strip() not in self.blkline:
                            log_cont += line + "\n"
                    log_cont = log_cont.split("]- ", 1)[-1].strip()

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
                        print(log_line, log_data[0])
                        break
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            # 针对文件做进一步分析, 来判断加载哪一个 SQL 表
            if re.findall("aggregate\.log|csv-direct-load\.log|forecast\.log|perl-task\.log|taskexecutor\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Postload_TaskExecutor as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                try:
                    SList.append(OpsBTable(
                        file_id=file_id,
                        log_line=data.get("log_line"),
                        log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                        log_level=data.get("log_level"),
                        log_comp=data.get("log_comp"),
                        log_cont=data.get("log_cont")))
                except Exception as e:
                    MultSQLLogger.error(e)
                    MultSQLLogger.error("Faild File: " + self.file)
                    MultSQLLogger.error("Faild Line: " + line)

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_opsb_itom_di_type3(self):
        """
        # receiver-itom-di-receiver-dpl.*.log
        # receiver-out.log
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
        with open(self.file, mode="r", encoding=self.encoding, errors="replace") as file:
            for line in file:
                DList.append(line.strip())

        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            # 判断该行是否是日志的开头
            try:
                log_time_str = line.split(" ", 2)[0] + " " + line.split(" ", 2)[1]
                log_time = self.get_logtime(log_time_str)
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
                    # 日志时间
                    log_time = self.get_logtime(log_data[0].split(" ", 2)[0] + " " + log_data[0].split(" ", 2)[1])
                    # 日志等级
                    log_level = log_data[0].split(" ")[3].strip()
                    if log_level not in ["INFO", "WARN", "ERROR", "DEBUG"]:
                        log_level = log_data[0].split(" ")[2].strip()
                    # 日志组件
                    log_comp = re.findall("\[.*?]", log_data[0], re.IGNORECASE)[0]
                    # 日志内容
                    log_cont = ""
                    for line in log_data:
                        if line.strip() not in self.blkline:
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
            # 针对文件做进一步分析, 来判断加载哪一个 SQL 表
            if re.findall("receiver-itom-di-receiver-dpl.*\.log|receiver-out\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Receiver_DPL as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                try:
                    SList.append(OpsBTable(
                        file_id=file_id,
                        log_line=data.get("log_line"),
                        log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                        log_level=data.get("log_level"),
                        log_comp=data.get("log_comp"),
                        log_cont=data.get("log_cont")))
                except Exception as e:
                    MultSQLLogger.error(e)
                    MultSQLLogger.error("Faild File: " + self.file)
                    MultSQLLogger.error("Faild Line: " + line)

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_opsb_itom_di_type4(self):
        """
        # scheduler.log
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
        with open(self.file, mode="r", encoding=self.encoding, errors="replace") as file:
            for line in file:
                DList.append(line.strip())

        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            # 判断该行是否是日志的开头
            try:
                log_time_str = line.split(" ", 2)[0] + " " + line.split(" ", 2)[1]
                log_time = self.get_logtime(log_time_str)
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
                    # 日志时间
                    log_time = self.get_logtime(log_data[0].split(" ", 2)[0] + " " + log_data[0].split(" ", 2)[1])
                    # 日志等级
                    log_level = log_data[0].split(" ")[3].strip()
                    if log_level not in ["INFO", "WARN", "ERROR", "DEBUG"]:
                        log_level = log_data[0].split(" ")[2].strip()
                    # 日志组件
                    log_comp = re.findall("\[.*?]", log_data[0], re.IGNORECASE)[0]
                    # 日志内容
                    log_cont = ""
                    for line in log_data:
                        if line.strip() not in self.blkline:
                            log_cont += line + "\n"
                    log_cont = log_cont.split("---", 1)[-1].strip()

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
            # 针对文件做进一步分析, 来判断加载哪一个 SQL 表
            if re.findall("scheduler\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Scheduler_UDX as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                try:
                    SList.append(OpsBTable(
                        file_id=file_id,
                        log_line=data.get("log_line"),
                        log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                        log_level=data.get("log_level"),
                        log_comp=data.get("log_comp"),
                        log_cont=data.get("log_cont")))
                except Exception as e:
                    MultSQLLogger.error(e)
                    MultSQLLogger.error("Faild File: " + self.file)
                    MultSQLLogger.error("Faild Line: " + line)

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_opsb_itom_idm_type1(self):
        """
        # idm-loader.log
        # idm-service.log
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
        with open(self.file, mode="r", encoding=self.encoding, errors="replace") as file:
            for line in file:
                DList.append(line.strip())

        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            # 判断该行是否是日志的开头
            try:
                log_time_str = line.split(" ", 2)[0].split("+")[0]
                log_time = self.get_logtime(log_time_str)
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
                    # 日志时间
                    log_time = self.get_logtime(log_data[0].split(" ", 2)[0].split("+")[0])
                    # 日志等级
                    log_level = "Null"
                    for level in ["INFO", "WARN", "ERROR", "DEBUG"]:
                        if level in log_data[0]:
                            log_level = level
                            break
                    if log_level == "Null":
                        log_level = "INFO"
                    # 日志组件
                    log_comp = re.findall("\[.*?] -", log_data[0], re.IGNORECASE)[0][:-4].strip()
                    # 日志内容
                    log_cont = ""
                    for line in log_data:
                        if line.strip() not in self.blkline:
                            log_cont += line + "\n"
                    log_cont = log_cont.split("] -", 1)[-1].strip()

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
            # 针对文件做进一步分析, 来判断加载哪一个 SQL 表
            if re.findall("idm-loader\.log|idm-service\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_IDM as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                try:
                    SList.append(OpsBTable(
                        file_id=file_id,
                        log_line=data.get("log_line"),
                        log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                        log_level=data.get("log_level"),
                        log_comp=data.get("log_comp"),
                        log_cont=data.get("log_cont")))
                except Exception as e:
                    MultSQLLogger.error(e)
                    MultSQLLogger.error("Faild File: " + self.file)
                    MultSQLLogger.error("Faild Line: " + line)

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
    file = r"C:\Projects\GitHub\LogAnalysis\test\opsb_log\idm\helm-opsb__itom-idm-68bb5fc59d-7bbkn__itom-idm__vm-opsb.home.local\idm-loader.log"
    test = OpsBFiles({"file": file})