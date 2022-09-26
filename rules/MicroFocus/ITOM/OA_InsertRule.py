# -*- coding: utf-8 -*-

import re
from module.tools.InsertTools import ReadFileTemplate

class OAFiles(ReadFileTemplate):
    """
    MicroFocus ITOM OA 文件解析类
    """
    def __init__(self, TaskInfo):
        # 父类里包含 self.file 和 self.targetdb
        super().__init__(TaskInfo)
        # 处理的实际逻辑
        self.classifiles()

    def classifiles(self):
        """
        针对 OA 文件进行分类, 然后在做后续处理
        :return:
        """
        if re.findall("system\.txt", self.file, re.IGNORECASE):
            self.readfile_system()
        else:
            print("没有文件需要处理")

    def readfile_system(self):
        with open(self.file, mode="r", encoding="utf-8", errors="replace") as file:
            for line in file:
                print(line.strip())

if __name__ == '__main__':
    # 测试部分, 测试时请修改 file 的值
    file = r"C:\oa_data\System.txt"
    TaskInfo = {"file": file, "targetdb": "demo"}
    oa = OAFiles(TaskInfo)