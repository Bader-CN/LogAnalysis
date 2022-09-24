# -*- coding: utf-8 -*-

import os, time
from PySide6.QtWidgets import QApplication
from module.gui.LogAnalysis_md import LogAnalysisMain
from module.gui.LogImport_md import LogAnalysisImport
from module.bridge.customSignals import allSignals
from module.bridge.customQueues import QTask
from module.bridge.customQueues import QData
from multiprocessing import Process, freeze_support

def logfile_to_sql(TaskInfo, QTask, QData):
    """
    根据 TaskDict 里的信息读取指定文件, 并将生成的数据回传到主进程
    :param TaskInfo: 任务数据, 包含规则和指定文件
    :param QTask: 获取 TaskInfo 的 Queue
    :param QData: 回传数据的 Queue
    :return:
    """
    pass

if __name__ == '__main__':
    # 解决 Windows 多进程异常的问题
    freeze_support()

    # 检查相关目录及文件是否存在
    if not os.path.exists("./log"):
        os.mkdir("./log")
    if not os.path.exists("./data/database"):
        os.makedirs("./data/database")
    if not os.path.exists("./data/template"):
        os.makedirs("./data/template")

    # 启动软件
    app = QApplication([])

    # 实例化 LogAnalysis 主界面
    logMain = LogAnalysisMain()
    # 实例化 LogAnalysis Import 界面
    logImport = LogAnalysisImport()

    # 当 LogAnalysis 主界面点击 Import 按钮时, 将会弹出 LogAnalysis Import 界面
    def showlogImportUI():
        logImport.show()
    logMain.ui.btn_import.clicked.connect(showlogImportUI)

    # 多进程部分
    #########################################################################
    def taskImportlog(dict):
        task1 = Process(target=logfile_to_sql, args=(dict, QTask, QData), daemon=True)
        task2 = Process(target=logfile_to_sql, args=(dict, QTask, QData), daemon=True)
        task3 = Process(target=logfile_to_sql, args=(dict, QTask, QData), daemon=True)
        task1.start()
        # task2.start()
        # task3.start()

    allSignals.need_want_data.connect(taskImportlog)
    #########################################################################

    # 显示主界面
    logMain.show()

    app.exec()
