# -*- coding: utf-8 -*-

import os, time
from PySide6.QtWidgets import QApplication
from module.gui.LogAnalysis_md import LogAnalysisMain
from module.gui.LogImport_md import LogAnalysisImport
from module.bridge.customSignals import allSignals
from multiprocessing import Queue, Process

def logfile_to_sql(dict, queue_task, queue_data):
    for i in range(100):
        print("多进程正在运行")
        time.sleep(1)

if __name__ == '__main__':
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
    queue_task = Queue()    # 向子进程发布任务
    queue_data = Queue()    # 子进程处理完成的数据
    queue_sign = Queue()    # 向子进程发送结束信号

    def taskImportlog(dict):
        task1 = Process(target=logfile_to_sql, args=(dict, queue_task, queue_data), name="Log1", daemon=True)
        task2 = Process(target=logfile_to_sql, args=(dict, queue_task, queue_data), name="Log2", daemon=True)
        task3 = Process(target=logfile_to_sql, args=(dict, queue_task, queue_data), name="Log3", daemon=True)
        task1.start()
        task2.start()
        task3.start()

    allSignals.need_want_data.connect(taskImportlog)
    #########################################################################

    # 显示主界面
    logMain.show()

    app.exec()
