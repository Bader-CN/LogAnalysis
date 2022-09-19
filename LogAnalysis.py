# -*- coding: utf-8 -*-

import os, time
from PySide6.QtWidgets import QApplication
from module.gui.LogAnalysis_md import LogAnalysisMain
from module.gui.LogImport_md import LogAnalysisImport
from module.bridge.customSignals import allSignals
from multiprocessing import Queue, Process

def mult_import_log(dict, id):
    print("多进程开始,id={}".format(str(id)))
    time.sleep(4)
    print("多进程结束,id={}".format(str(id)))

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
    def start_mult_task(dict):
        task1 = Process(target=mult_import_log, args=(dict, 1))
        task2 = Process(target=mult_import_log, args=(dict, 2))
        task3 = Process(target=mult_import_log, args=(dict, 3))
        task1.start()
        task2.start()
        task3.start()

    allSignals.need_want_data.connect(start_mult_task)
    #########################################################################

    # 显示主界面
    logMain.show()

    app.exec()
