# -*- coding: utf-8 -*-

import re
from module.tools.InsertTools import ReadFileTemplate

class OAFiles(ReadFileTemplate):
    """
    MicroFocus ITOM OA 文件解析类
    """
    def __init__(self, TaskInfo):
        # 继承父类里的 self.file 和 self.targetdb
        super().__init__(TaskInfo)
        # 如果匹配到此内容, 则改行不做任何处理
        self.blkline = [
            "<rolled=0>",
        ]
        # 处理的实际逻辑
        data = self.classifiles()

    def classifiles(self):
        """
        针对 OA 文件进行分类, 然后在做后续处理
        :return:
        """
        if re.findall("system\.txt", self.file, re.IGNORECASE):
            return self.readfile_system()

    def readfile_system(self):
        """
        OA System.txt 文件解析函数
        :return: {"targetdb":self.targetdb, "file":self.file, "data":DList}
        """
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            # 初始化变量
            num_line = 0
            DList = []
            # 读取文件的每一行
            for line in file:
                num_line += 1
                line = line.strip()
                # 验证该行是否符合处理条件
                for blk in self.blkline:
                    # 如果该行不在黑名单里, 并且长度不为 0, 则处理该行信息
                    if re.findall(blk, line) == [] and len(line) != 0:
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

        # 测试数据
        # for data in DList:
        #     print(data)

        # 将结果数据返回
        return {"targetdb":self.targetdb, "file":self.file, "data":DList}

if __name__ == '__main__':
    # 测试部分, 测试时请修改 file 的值
    file = r"C:\oa_data\System.txt"
    TaskInfo = {"file": file, "targetdb": "demo"}
    oa = OAFiles(TaskInfo)