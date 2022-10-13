# -*- coding: utf-8 -*-

import re, sys
from datetime import datetime
from xml.etree import ElementTree as ET
from module.tools.InsertTools import ReadFileTemplate
from rules.MicroFocus.ITOM.OA_SQLTable import FileHash
if __name__ != "__main__":
    from module.tools.AppDebug import MultSQLLogger

class OAFiles(ReadFileTemplate):
    """
    MicroFocus ITOM OA 文件解析类
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
        # 如果匹配到此内容, 则改行不做任何处理
        self.blkline = [
            "<rolled=\d>",
        ]
        # 处理的实际逻辑
        data = self.classifiles()
        # 将处理完成的数据放到队列中
        if __name__ != "__main__":
            QData.put(data)

    def classifiles(self):
        """
        针对 OA 文件进行分类, 然后在做后续处理
        :return:
        """
        # 针对 System.txt, 则调用 readlog_system 方法
        if re.findall("system\.txt", self.file, re.IGNORECASE):
            return self.readlog_system()
        # 针对 agent.log_<日期>, 则调用 readlog_agentlog 方法
        elif re.findall("agent\.log_\d+-\d+-\d+_\d+\.\d+", self.file, re.IGNORECASE):
            return self.readlog_agentlog()
        # 针对 <数字>_header.xml, 则调用 readcfg_policy 方法
        elif re.findall("\w{8}-\w{4}-\w{4}-\w{4}-\w{12}_header\.xml", self.file, re.IGNORECASE):
            return self.readcfg_policy()

    def readlog_system(self):
        """
        OA System.txt 文件解析函数
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            # 初始化变量
            num_line = 0
            DList = []
            SList = []
            # 读取文件的每一行
            for line in file:
                num_line += 1
                line = line.strip()
                # 验证该行是否符合处理条件
                for blk in self.blkline:
                    # 如果该行不在黑名单里, 并且长度不为 0, 则处理该行信息
                    if re.findall(blk, line) == [] and len(line) != 0:
                        try:
                            # 如果有 INF:/WRN:/ERR:, 则说明是事件的开头
                            if len(re.findall("INF:|WRN:|ERR:", line)) > 0:
                                DList.append({
                                    "log_line": num_line,
                                    "log_time": self.get_logtime(line.split(': ',4)[2].strip()),
                                    "log_level": line.split(': ', 4)[1].strip(),
                                    "log_comp": line.split(': ', 4)[3].strip(),
                                    "log_cont": line.split(': ', 4)[4].strip(),
                                })
                            # 否则, 该行就是上一个事件的内容
                            else:
                                DList[-1]["log_cont"] = DList[-1]["log_cont"] + "\n" + line
                        except Exception as e:
                            # 模块模式
                            if __name__ != "__main__":
                                MultSQLLogger.error(e)
                                MultSQLLogger.debug(line)
                            # 测试模式
                            else:
                                print("第{}行出现错误:{}".format(str(num_line), e))

            # 模块模式下: 将 DList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
            if __name__ != "__main__":
                from rules.MicroFocus.ITOM.OA_SQLTable import System
                file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
                for data in DList:
                    SList.append(System(
                        file_id = file_id,
                        log_line = data.get("log_line"),
                        log_time = datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                        log_level = data.get("log_level"),
                        log_comp = data.get("log_comp"),
                        log_cont = data.get("log_cont")))
            # 测试模式下: 打印 DList 中的每一项数据
            else:
                for data in DList:
                    print(data)

        # 模块模式下: 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo

if __name__ == "__main__":
    # 读取测试文件
    file = r"C:\oa_data\System.txt"
    test = OAFiles({"file": file})