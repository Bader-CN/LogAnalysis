# -*- coding: utf-8 -*-

import re
import os
import time
from datetime import datetime
from module.tools.InsertTools import ReadFileTemplate
from rules.RedHat.LinuxSystem.Syslog_SQLTable import FileHash
if __name__ != "__main__":
    from module.tools.AppDebug import MultSQLLogger

class SyslogFiles(ReadFileTemplate):
    """
    Syslog for Linux log files class
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
        ]
        # 处理的实际逻辑
        data = self.classifiles()
        # 将处理完成的数据放到队列中
        if __name__ != "__main__":
            QData.put(data)

    def classifiles(self):
        """
        针对 Syslog 文件进行分类, 然后在做后续处理
        :return:
        """
        # /var/log/messages
        if re.findall("messages", self.file, re.IGNORECASE):
            return self.syslog_type1()

    def syslog_type1(self):
        """
        Syslog logs:
        # /var/log/messages
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
        ctime_y = time.localtime(os.path.getctime(self.file))[0]    # 文件创建的时间, 仅获取年份
        mtime_y = time.localtime(os.path.getmtime(self.file))[0]    # 文件修改的时间, 仅获取年份
        cross_y = False # 是否跨年, 默认不跨年, 即 ctime_y == mtime_y

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding=self.encoding, errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            log_time = self.get_logtime(line.split(":", 2)[0] + ":" + line.split(":", 2)[1] + ":" + line.split(":", 2)[2].split(" ", 1)[0])
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
                    log_time = self.get_logtime(log_data[0].split(":", 2)[0] + ":" + log_data[0].split(":", 2)[1] + ":" + log_data[0].split(":", 2)[2].split(" ", 1)[0])
                    # 由于 /var/log/messages 的日期格式可能没有年份, 所以要基于文件的创建/修改时间来判断年份
                    if log_time.split("-", 1)[0] == "1900":
                        if ctime_y == mtime_y:
                            log_time = str(ctime_y) + "-" + log_time.split("-", 1)[-1]
                        else:
                            # 如果首次发现跨年
                            if cross_y == False and log_time.split("-")[1] == "01" and log_time.split("-")[2] == "01":
                                cross_y = True
                                log_time = str(mtime_y) + "-" + log_time.split("-", 1)[-1]
                            # 后续都按照修改时间来修改
                            elif cross_y == True:
                                log_time = str(mtime_y) + "-" + log_time.split("-", 1)[-1]
                            # 未跨年的部分
                            else:
                                log_time = str(ctime_y) + "-" + log_time.split("-", 1)[-1]
                    # 日志组件部分
                    log_comp = log_data[0].split(":", 2)[-1].split(" ", 1)[-1].split(":", 1)[0]
                    log_cont = ""
                    for line in log_data:
                        log_cont += line + "\n"
                    log_cont = log_cont.split(log_comp, 1)[-1].strip()
                    if log_cont[0] == ":":
                        log_cont = log_cont[1:].strip()
                    # 针对 Syslog 日志等级做额外处理
                    log_level = "INFO"
                    if re.findall("error|failed|can't|cannot|can not", log_cont, re.IGNORECASE):
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
            # 根据不同的 Syslog 文件来加载不同的 SQLAlchemy 表
            if re.findall("messages", self.file, re.IGNORECASE):
                from rules.RedHat.LinuxSystem.Syslog_SQLTable import Syslog_Messages as SyslogTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(SyslogTable(
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

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo

if __name__ == "__main__":
    # 读取测试文件
    file = r"../../../test/redhat_syslog/messages"
    test = SyslogFiles({"file": file})