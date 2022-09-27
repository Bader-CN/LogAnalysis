# -*- coding: utf-8 -*-

import os
from PySide6.QtWidgets import QApplication
from module.gui.LogAnalysis_md import LogAnalysisMain
from module.gui.LogImport_md import LogAnalysisImport
from module.bridge.customSignals import allSignals
from module.bridge.customQueues import QTask
from module.bridge.customQueues import QData
from module.tools.AppDebug import AppMainLogger
from module.tools.AppDebug import MultSQLLogger
from multiprocessing import Process, freeze_support

def logfile_to_sql(QTask, QData):
    """
    根据 QTask 里的信息读取指定文件, 并将生成的数据回传到主进程
    :param QTask: 获取 TaskInfo 的 Queue
    :param QData: 回传数据的 Queue
    :return:
    """
    while True:
        TaskInfo = QTask.get()
        # 如果接收的信号是 Stop
        if TaskInfo.get("Signal") == "Stop":
            MultSQLLogger.info("Received signal -> Stop, process will exit.")
            exit(0)
        # 如果不是 Stop, 那么就开始处理数据
        else:
            if TaskInfo.get("company") == "MicroFocus" and TaskInfo.get("productline") == "ITOM" and TaskInfo.get("product") == "Operations Agent(OA)":
                from rules.MicroFocus.ITOM import OA_InsertRule
                OA_InsertRule.OAFiles(TaskInfo, QData)

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
        """
        将预处理任务按照文件进一步拆分, 并将拆分的任务传递给多进程开始处理
        :param dict: {targetdb, path, pathtype, company, productline, product, processes, files}
        :return:
        """
        AppMainLogger.debug("TaskDict: {}".format(str(dict)))
        fileslist = dict.get("files")
        processes = int(dict.get("processes"))
        # 如果文件数小于进程数, 则按照文件数启动多进程
        if processes > len(fileslist):
            processes = len(fileslist)
        # 基于文件生成多进程的任务列表, 每一个任务都是一个字典, 包含具体的任务信息
        tasks = []
        for file in fileslist:
            task = {
                "file": file,
                "targetdb": dict.get("targetdb"),
                "company": dict.get("company"),
                "productline": dict.get("productline"),
                "product": dict.get("product"),
            }
            tasks.append(task)
        # 将任务信息放入 QTask 中
        for task in tasks:
            QTask.put(task)
        # 启动多进程
        for p in range(processes):
            p = Process(target=logfile_to_sql, args=(QTask, QData), daemon=True)
            p.start()
        # 输入结束信号
        for p in range(processes):
            QTask.put({"Signal":"Stop"})

    allSignals.need_want_data.connect(taskImportlog)
    #########################################################################

    # 显示主界面
    logMain.show()

    app.exec()
