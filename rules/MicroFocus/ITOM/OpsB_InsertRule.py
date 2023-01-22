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
        # 针对 itomdipulsar-bookkeeper-<ID>_<Helm_Deploy_Name>_itomdipulsar-bookkeeper-***.log 类型的日志
        if re.findall("itomdipulsar-bookkeeper-\d_.*_itomdipulsar-bookkeeper-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_itomdipulsar_bookkeeper()
        # 其余 itomdipulsar-bookkeeper 相关日志的通用方法
        elif re.findall("itomdipulsar-bookkeeper.*\.log|itomdipulsar-zookeeper.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()

    def readlog_opsb_type1(self):
        """
        OpsB logs
        # itomdipulsar-bookkeeper-<ID>_<Helm_Deploy_Name>_***.log
        # itomdipulsar-zookeeper-<ID>_<Helm_Deploy_Name>_***.log
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
            log_time_str = line.split(",", 5)[-1]
            # 对时间字符串做进一步处理
            if re.findall("time=.*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", log_time_str):
                # 匹配: "time=""2023-01-20T12:49:05Z"",
                # T 是分隔符; Z 是 UTC
                log_time_str = line.split(",", 1)[0][:-8]
            elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3}", log_time_str):
                # 匹配: "2023-01-20T12:19:09,768",
                log_time_str = line.split(",", 1)[0][:-8]
            elif re.findall("\d{2}:\d{2}:\d{2}\.\d{3} \[", log_time_str):
                # 匹配：12:18:36.944 [main]
                log_time_str = line.split(",", 1)[0][:-8]
            # 根据时间字符串计算时间
            log_time = self.get_logtime(log_time_str)
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
                    log_time = self.get_logtime(log_data[0].split(",")[0][:-8].strip())
                    # 针对日志等级的处理
                    log_level = log_data[0].split(",", 5)[-1].split("level=")[-1].split(" msg=", 1)[0].upper()
                    if log_level == "WARNING":
                        log_level = "WARN"
                    if log_level not in ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]:
                        content = log_data[0].split(",", 5)[-1].strip()
                        for level in [" TRACE ", " DEBUG ", " INFO ", "#INFO:", " WARN ", " ERROR ", " CRITICAL "]:
                            if level in content:
                                if level == "#INFO:":
                                    log_level = "INFO"
                                else:
                                    log_level = level.strip()
                    # 针对日志组件的处理
                    log_comp = log_data[0].split(",")[2] + "_" + log_data[0].split(",")[3] + "_" + log_data[0].split(",")[4]
                    # 针对日志内容的处理
                    log_cont = ""
                    for line in log_data:
                        log_cont += line.split(",", 5)[-1] + "\n"
                    log_cont = log_cont.split(",", 5)[-1].split("msg=", 1)[-1].strip()
                    # 针对日志内容开头为 "date [***] <LogLevel> 的特殊处理
                    if re.findall("\d{2}:\d{2}:\d{2}\.\d{3} \[.*?\] (.*?) ", log_cont):
                        split_str = re.findall("\d{2}:\d{2}:\d{2}\.\d{3} \[.*?\] (.*?) ", log_cont)[0]
                        log_cont = log_cont.split(split_str, 1)[-1].strip()
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
            if re.findall("itomdipulsar-bookkeeper.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_BookKeeper as OpsBTable
            elif re.findall("itomdipulsar-zookeeper.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_Zookeeper as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OpsBTable(
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

    def readlog_opsb_itomdipulsar_bookkeeper(self):
        """
        OpsB logs
        # itomdipulsar-bookkeeper-<ID>_<Helm_Deploy_Name>_itomdipulsar-bookkeeper-***.log
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
            log_time_str = line.split(",", 5)[-1]
            # 对时间字符串做进一步处理
            if re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3}", log_time_str):
                # 匹配: "2023-01-20T12:19:09,768",
                log_time_str = line.split(",", 1)[0][:-8]
            # 根据时间字符串计算时间
            log_time = self.get_logtime(log_time_str)
            # 针对 itomdipulsar-bookkeeper-<ID>_<Helm_Deploy_Name>_itomdipulsar-bookkeeper-***.log 这种类型的日志, 判断开头的条件需要额外追加
            if log_time != "Null" or re.findall("Applying config", line.split(",", 5)[-1], re.IGNORECASE):
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
                    log_time = self.get_logtime(log_data[0].split(",")[0][:-8].strip())
                    # 针对日志等级的处理
                    log_level = "Null"
                    for level in ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "Applying config"]:
                        if level in log_data[0]:
                            log_level = level
                            if level == "Applying config":
                                log_level = "Config"
                    # 针对日志组件的处理
                    log_comp = log_data[0].split(",")[2] + "_" + log_data[0].split(",")[3] + "_" + log_data[0].split(",")[4]
                    # 针对日志内容的处理
                    log_cont = ""
                    for line in log_data:
                        log_cont += line.split(",", 5)[-1] + "\n"
                    # 格式: 2023-01-20T15:50:12,874 [db-storage-cleanup-11-1]
                    if re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3} \[(.*?)\]", log_cont):
                        log_cont = "[" + log_cont.split("[", 1)[-1]
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
            if re.findall("itomdipulsar-bookkeeper.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_BookKeeper as OpsBTable
            elif re.findall("itomdipulsar-zookeeper.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_Zookeeper as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OpsBTable(
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
    file = r"D:\opsb_test_log\opsbfiles\itomdipulsar-bookkeeper-0_helm-opsb_itomdipulsar-bookkeeper-2d84fe104577f433d188651e2d9d0a4e87f6964d6faa35b37ac52e4f62cd042d.log.20230120.log"
    test = OpsBFiles({"file": file})