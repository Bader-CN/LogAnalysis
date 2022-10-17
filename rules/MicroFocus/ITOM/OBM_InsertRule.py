# -*- coding: utf-8 -*-

import re
from datetime import datetime
from xml.etree import ElementTree as ET
from module.tools.InsertTools import ReadFileTemplate
from rules.MicroFocus.ITOM.OA_SQLTable import FileHash
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
        if re.findall("opr-gateway\.log", self.file, re.IGNORECASE):
            return self.readlog_obm_type1()

    def readlog_obm_type1(self):
        """
        OBM logs
        # opr-gateway.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 基于 IList 切分完成后的数据
        SList = []
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
                FList.append({"log_line":idx_list[0]+1, "log_data":DList[idx_list[0]:idx_list[1]]})
                idx_list.pop(0)

        for data in FList:
            print(data)


if __name__ == "__main__":
    # 读取测试文件
    file = r"C:\opr-gateway.log"
    test = OBMFiles({"file": file})
