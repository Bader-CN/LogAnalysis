# -*- coding: utf-8 -*-

from module.tools.InsertTools import ReadFile

class OAFiles(ReadFile):
    """
    MicroFocus ITOM OA 文件解析类
    """
    def __int__(self, TaskInfo):
        pass


if __name__ == '__main__':
    # 测试部分, 测试时请修改 file 的值
    file = r"c:\demo"
    TaskInfo = {"file": file, "targetdb": "demo"}

    oa = OAFiles(TaskInfo)