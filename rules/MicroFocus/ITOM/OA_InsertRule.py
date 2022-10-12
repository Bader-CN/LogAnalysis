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

        elif re.findall("agent\.log_\d+-\d+-\d+_\d+\.\d+", self.file, re.IGNORECASE):
            return self.readlog_agentlog()

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

    def readlog_agentlog(self):
        """
        OA agent.log_<日期> 文件
        :return:
        """
        # 去掉不需要索引的行后的文件数据列表
        DList = []
        # 临时字典
        TDict = {}
        # 转换完 SQL 语句后的数据
        SList = []
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file.readlines():
                line = line.strip()
                if "==>" not in line and line != "":
                    DList.append(line)

        # 初始化需要获取的数据
        os_name = ""
        os_type = ""
        oa_status = ""
        oa_hotfix = ""
        oa_version = ""
        oa_confget = ""

        # 获取所需要的数据段
        for line in DList:
            if "osname=" in line and os_name == "":
                os_name = line.split('=')[-1]
                TDict["os_name"] = os_name

            elif "ostype=" in line and os_type == "":
                os_type = line.split('=')[-1]
                TDict["os_type"] = os_type

            elif "agtversion=" in line and oa_version == "":
                oa_version = line.split('=')[-1]
                TDict["oa_version"] = oa_version

            # 针对 ovconfget 需要处理 两部分数据
            elif "Cmd executed : /opt/OV/bin/ovconfget" == line:
                idx_ovconfget_str = DList.index(line)
                try:
                    idx_ovconfget_end = DList.index("****************************************", idx_ovconfget_str+2)
                except:
                    idx_ovconfget_end = -1
                # 第一部分, ovconfget 的整理内容
                for conf_line in DList[idx_ovconfget_str:idx_ovconfget_end]:
                    if oa_confget == "":
                        oa_confget = conf_line
                    else:
                        oa_confget = oa_confget + "\n" + conf_line
                TDict["oa_confget"] = oa_confget

                # 第二部分, ovconfget 的每项数值
                from rules.MicroFocus.ITOM.OA_SQLTable import Config
                file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
                OAConfList = DList[idx_ovconfget_str+2:idx_ovconfget_end]
                section = ""
                for line in OAConfList:
                    if line[0] == "[" and line[-1] == "]":
                        section = line
                    else:
                        conf = "{}.{}".format(section, line)
                        oaconf = conf.split("=", 1)
                        SList.append(Config(
                            file_id=file_id,
                            key=oaconf[0],
                            value=oaconf[-1],
                        ))

            elif "Cmd executed : /opt/OV/bin/ovc -status -level 8" == line:
                idx_oa_status_str = DList.index(line)
                idx_oa_status_end = DList.index("Checksum and what string details of the agent and lcore binaries", idx_oa_status_str)
                for status in DList[idx_oa_status_str : idx_oa_status_end]:
                    if oa_status == "":
                        oa_status = status
                    else:
                        oa_status = oa_status + "\n" + status
                TDict["oa_status"] = oa_status

            elif "Cmd executed : /opt/OV/bin/ovdeploy -inv -inclbdl -includeupdates" == line:
                idx_oa_hotfix_str = DList.index(line)
                idx_oa_hotfix_end = DList.index("****************************************", idx_oa_hotfix_str + 2)
                for hotfix in DList[idx_oa_hotfix_str : idx_oa_hotfix_end]:
                    if oa_hotfix == "":
                        oa_hotfix = hotfix
                    else:
                        oa_hotfix = oa_hotfix + "\n" + hotfix
                TDict["oa_hotfix"] = oa_hotfix

        # 将数据转换为 SQLAlchemy 类型的数据类型, 并保存在 SList 中
        from rules.MicroFocus.ITOM.OA_SQLTable import Summary
        file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
        for key, value in TDict.items():
            SList.append(
                Summary(
                    file_id=file_id,
                    key=key,
                    value=value,))

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
    file = r"C:\oa_data\agent.log_2022-04-14_09.11"
    TaskInfo = {"file": file, "targetdb": "demo", "company": "company", "productline": "productline", "product": "product"}
    oa = OAFiles(TaskInfo)