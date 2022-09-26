# -*- coding: utf-8 -*-

from module.tools.InsertTools import ReadFile

class OAFiles(ReadFile):
    """
    MicroFocus ITOM OA 文件解析类
    """
    def __int__(self, TaskInfo):
        pass


if __name__ == '__main__':
    TaskInfo = {"file": "c:\\demo", "targetdb": "demo"}
    oa1 = OAFiles(TaskInfo)
    print(oa1.file)
    print(oa1.get_logtime("2022-02-03 01:01:11"))