# -*- coding: utf-8 -*-

import re
from datetime import datetime
from xml.etree import ElementTree as ET
from module.tools.InsertTools import ReadFileTemplate
from rules.MicroFocus.ITOM.OA_SQLTable import FileHash
# 测试时注释掉 from module.tools.AppDebug import MultSQLLogger
from module.tools.AppDebug import MultSQLLogger

class OAFiles(ReadFileTemplate):
    """
    MicroFocus ITOM OA 文件解析类
    """
    def __init__(self, TaskInfo, QData=None):
        super().__init__()
        self.TaskInfo = TaskInfo
        self.file = self.TaskInfo.get("file")
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

        # 测试时请注释掉
        QData.put(data)

    def classifiles(self):
        """
        针对 OA 文件进行分类, 然后在做后续处理
        :return:
        """
        if re.findall("system\.txt", self.file, re.IGNORECASE):
            return self.readlog_system()
        elif re.findall("\w{8}-\w{4}-\w{4}-\w{4}-\w{12}_header\.xml", self.file, re.IGNORECASE):
            return self.readcfg_policy()

    def readlog_system(self):
        """
        OA System.txt 文件解析函数
        :return: TaskInfo["data"] = SList
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
                        # 如果有 INF:/WRN:/ERR:, 则说明是事件的开头
                        try:
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
                            # 测试时请注释掉这段内容
                            MultSQLLogger.warning(e)
                            MultSQLLogger.debug(line)

            # 将 DList 转换为 SQLAlchemy 类型的数据类型, 并保存在 SList 中
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

        # 测试代码
        # for data in DList:
        #     print(data)

        # 将结果数据返回
        self.TaskInfo["data"] = SList
        return self.TaskInfo

    def readcfg_policy(self):
        """
        OA System.txt 文件解析函数
        :return: TaskInfo["data"] = SList
        """
        # https://python3-cookbook.readthedocs.io/zh_CN/latest/c06/p06_parse_modify_rewrite_xml.html
        # https://python3-cookbook.readthedocs.io/zh_CN/latest/c06/p07_parse_xml_documents_with_namespaces.html
        # https://www.cnblogs.com/bigtreei/p/13361578.html

        SList = []
        try:
            tree = ET.parse(self.file)
            root = tree.getroot()
            namespace = re.findall('\{.*\}', root.tag)[0]
            # 获取 Policy XML 文件中的数据
            ply_name = root.find('{}policy'.format(namespace)).find("{}name".format(namespace)).text
            ply_version = root.find('{}policy'.format(namespace)).find("{}version".format(namespace)).text
            ply_status = root.find('{}policy'.format(namespace)).find("{}status".format(namespace)).text
            ply_type = root.find('{}policytype'.format(namespace)).find("{}name".format(namespace)).text
            try:
                with open(self.file[:len(self.file) - len("header.xml")] + "data", "r", encoding="utf-8", errors="replace") as file:
                    ply_data = file.read()
            except:
                ply_data = "Null"

            # 将数据转换为 SQLAlchemy 类型的数据类型, 并保存在 SList 中
            from rules.MicroFocus.ITOM.OA_SQLTable import Policy
            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            SList.append(
                Policy(
                    file_id = file_id,
                    ply_name = ply_name,
                    ply_version = ply_version,
                    ply_status = ply_status,
                    ply_type = ply_type,
                    ply_data = ply_data))
        except Exception as e:
            MultSQLLogger.warning(e)

        # 将结果数据返回
        self.TaskInfo["data"] = SList
        return self.TaskInfo

if __name__ == '__main__':
    # 测试部分, 测试时请修改 file 的值
    file = r"C:\oa_data\policies\le\bedbd00e-29a3-473b-9ce8-9306e195d69e_header.xml"
    TaskInfo = {"file": file, "targetdb": "demo", "company": "company", "productline": "productline", "product": "product"}
    oa = OAFiles(TaskInfo)