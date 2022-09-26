# -*- coding: utf-8 -*-

import re
from module.tools.InsertTools import ReadFileTemplate

class OAFiles(ReadFileTemplate):
    """
    MicroFocus ITOM OA 文件解析类
    """
    def __int__(self, TaskInfo):
        pass

    def classifiles(self):
        """
        针对 OA 文件进行分类, 然后在做后续处理
        :return:
        """
        if re.findall("system\.txt", self.file, re.IGNORECASE):
            pass

    def readfile_system(self):
        pass


if __name__ == '__main__':
    # 测试部分, 测试时请修改 file 的值
    file = r"c:\demo"
    TaskInfo = {"file": file, "targetdb": "demo"}

    oa = OAFiles(TaskInfo)