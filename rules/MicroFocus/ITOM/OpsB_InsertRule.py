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
        self.blkline = [
            '""',
            '}\n',
        ]
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
        if re.findall("itomdipulsar-bookkeeper.*\.log|itomdipulsar-zookeeper.*\.log|itomdipulsar-broker.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_pulsar_type1()

    def readlog_opsb_pulsar_type1(self):
        """
        OpsB logs
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
            # 设置判断的初始条件
            is_Start = False                            # 特殊条件, 可以将 is_Start 变更为 True
            log_time_str = "Null"
            log_content_str = line.split(",", 5)[-1]    # 日志都可以用逗号分割为5段, 根据最后一段来判断是否是日志的开头
            # 匹配: "time=""2023-01-20T12:49:05Z"", T 是分隔符; Z 是 UTC
            if re.findall("time=.*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", log_content_str):
                log_time_str = line.split(",", 1)[0][:-8]
            # 匹配: "2023-01-20T12:19:09,768"
            elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3}", log_content_str):
                log_time_str = line.split(",", 1)[0][:-8]
            # 匹配：12:18:36.944 [main]
            elif re.findall("\d{2}:\d{2}:\d{2}\.\d{3} \[", log_content_str):
                log_time_str = line.split(",", 1)[0][:-8]
            # 计算日志中的时间
            log_time = self.get_logtime(log_time_str)
            # 特殊条件
            if re.findall("Adding config|Applying config", log_content_str, re.IGNORECASE):
                is_Start = True
            # 在非时间的内容中, 如果该行包括 "Exception", "at ", " more", "Caused by" 这类字段, 则判断为多行, 其余为单行
            if is_Start == False:
                is_Match = False
                for key in ["Exception", "at ", " more", "Caused by", '"  ""', '"    ""', '"  },"']:
                    if key in log_content_str:
                            is_Start = False
                            is_Match = True
                if is_Match == False:
                        is_Start = True
            # 判断该行是否是日志的开头
            if log_time != "Null" or is_Start == True:
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
                    log_time = self.get_logtime(log_data[0].split(",")[0][:-8].strip())
                    # 日志等级
                    if re.findall("Adding config|Applying config|Updating config", log_data[0], re.IGNORECASE):
                        log_level = "Config"
                    elif re.findall("level=.*msg=.*", log_data[0], re.IGNORECASE):
                        log_level = log_data[0].split(",", 5)[-1].split("level=")[-1].split(" msg=", 1)[0].upper().strip()
                    elif re.findall("- #.*: ", log_data[0], re.IGNORECASE):
                        log_level = log_data[0].split(",", 5)[-1].split("- #", 1)[-1].split(":", 1)[0].upper().strip()
                    elif re.findall("\[(.*?)\] .*", log_data[0], re.IGNORECASE):
                        log_level = log_data[0].split(",", 5)[-1].split("]", 1)[-1].strip().split(" ", 1)[0].strip()
                    else:
                        log_level = "INFO"
                        keywords = ["Can't", "Cannot", "Warning", "Failed", "Exception"]
                        for key in keywords:
                            if key in log_data[0]:
                                log_level = "ERROR"
                    if log_level == "WARNING":
                        log_level = "WARN"
                    # 日志组件
                    log_comp = log_data[0].split(",")[2] + "_" + log_data[0].split(",")[3] + "_" + log_data[0].split(",")[4]
                    # 日志内容
                    log_cont = ""
                    for line in log_data:
                        log_cont += line.split(",", 5)[-1] + "\n"
                    if re.findall("msg=", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split("msg=", 1)[-1].strip()
                    elif re.findall("\d{2}:\d{2}:\d{2}\.\d{3} \[(.*?)\]", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split(re.findall("\d{2}:\d{2}:\d{2}\.\d{3}", log_cont, re.IGNORECASE)[0], 1)[-1].strip()
                    elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3} \[(.*?)\]", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split(re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}", log_cont, re.IGNORECASE)[0], 1)[-1].strip()
                    # 检查黑名单, 如果不在, 则将数据放入 FList 中
                    is_Black = False
                    for blk in self.blkline:
                        if blk == log_cont:
                            is_Black = True
                    if is_Black == False:
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
            elif re.findall("itomdipulsar-broker.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_Broker as OpsBTable

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
    file = r"D:\opsb_test_log\itomdipulsar-bookkeeper-test-file.log"
    test = OpsBFiles({"file": file})