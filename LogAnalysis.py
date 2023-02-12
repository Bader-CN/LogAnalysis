# -*- coding: utf-8 -*-

import os
# 检查相关目录及文件是否存在, 如果不存在, 则创建相关目录和文件
if not os.path.exists("config.cfg"):
    with open("config.cfg", mode="w", encoding="utf-8") as f:
        f.write((
            "[App_Display]"
            "# value: 'Auto' or 'zh_CN' or 'en_US'\n"
            "App_Language = Auto\n\n"

            "[App_Optimiz]\n"
            "# Maximum number of processes that read files\n"
            "# value: must > 0 or 'Auto'\n"
            "Max_Processes = Auto\n"
            "# Maximum number of bytes of data read every time for hash, default is 8192 bytes\n"
            "Max_Hashsizes = 8192\n"
            "# Hash algorithm used to verify files, value can md5, sha1, sha224, sha256, sha384, sha512\n"
            "Hash_Method = md5\n\n"

            "[App_Logging]\n"
            "# value: DEBUG, INFO, WARNING, ERROR, CRITICAL\n"
            "App_Console_Level = WARNING\n"
            "App_Main_Level = WARNING\n"
            "App_MultSQL_Level = WARNING\n"
        ))

if not os.path.exists("./log"):
    os.mkdir("./log")
if not os.path.exists("./data/database"):
    os.makedirs("./data/database")
if not os.path.exists("./data/template"):
    os.makedirs("./data/template")

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QTextDocument
from module.gui.LogAnalysis_md import LogAnalysisMain
from module.gui.LogImport_md import LogAnalysisImport
from module.gui.LogHelp_md import LogAnalysisHelp
from module.gui.SelectCont_md import CellContUI
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
            MultSQLLogger.debug("Received signal -> Stop, process will exit.")
            exit(0)
        # 如果不是 Stop, 那么就开始处理数据
        else:
            if TaskInfo.get("company") == "MicroFocus" and TaskInfo.get("productline") == "ITOM" and TaskInfo.get("product") == "Operations Agent(OA)":
                from rules.MicroFocus.ITOM import OA_InsertRule
                OA_InsertRule.OAFiles(TaskInfo, QData)
            elif TaskInfo.get("company") == "MicroFocus" and TaskInfo.get("productline") == "ITOM" and TaskInfo.get("product") == "Operations Bridge Manager(OBM)":
                from rules.MicroFocus.ITOM import OBM_InsertRule
                OBM_InsertRule.OBMFiles(TaskInfo, QData)
            elif TaskInfo.get("company") == "MicroFocus" and TaskInfo.get("productline") == "ITOM" and TaskInfo.get("product") == "Operations Bridge Suite(OpsB)":
                from rules.MicroFocus.ITOM import OpsB_InsertRule
                OpsB_InsertRule.OpsBFiles(TaskInfo, QData)
            elif TaskInfo.get("company") == "RedHat" and TaskInfo.get("productline") == "RedHat Linux System" and TaskInfo.get("product") == "Syslog for Linux":
                from rules.RedHat.LinuxSystem import Syslog_InsertRule
                Syslog_InsertRule.SyslogFiles(TaskInfo, QData)

if __name__ == '__main__':
    try:
        # 解决 Windows 多进程异常的问题
        freeze_support()
        # 启动软件
        app = QApplication([])
        # 实例化 LogAnalysis 主界面并设置标题
        logMain = LogAnalysisMain()
        logMain.setWindowTitle("LogAnalysis v1.3.0 Beta")
        # 实例化 LogAnalysis Help 界面
        logHelp = LogAnalysisHelp()
        # 实例化 LogAnalysis Import 界面
        logImport = LogAnalysisImport()
        # 实例化 LogAnalysis Select Content 界面
        logSltCont = CellContUI()

        # 当 LogAnalysis 主界面点击 Import 按钮时, 将会弹出 LogAnalysis Import 界面
        def showlogImportUI():
            logImport.show()
        logMain.ui.btn_import.clicked.connect(showlogImportUI)

        # 当 LogAnalysis 主界面点击 Help 按钮时, 将会弹出 LogAnalysis Help 界面
        def showlogHelpUI():
            import markdown2
            html = markdown2.markdown_path("./help/mddoc/demo.md", encoding="utf8", extras=["fenced-code-blocks"])
            # html = markdown2.markdown(md_txt, extras=["fenced-code-blocks"])
            logHelp.ui.mdview.setHtml(html)
            logHelp.show()
        allSignals.open_help_docs.connect(showlogHelpUI)

        # 当 LogAnalysis 主界面里双击查询结果的单元格时, 弹出 LogAnalysis Select Content 界面
        def showlogSltContUI(content):
            logSltCont.ui.line_search.setText(logMain.ui.line_search.text())
            logSltCont.showContent(content)
        allSignals.select_cell_data.connect(showlogSltContUI)

        # 多进程部分 #########################################################################
        def taskImportlog(dict):
            """
            将预处理任务按照文件进一步拆分, 并将拆分的任务传递给多进程开始处理
            :param dict: {targetdb, path, pathtype, company, productline, product, processes, files}
            :return:
            """
            AppMainLogger.info("TaskDict: {}".format(str(dict)))
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
                    "total": len(fileslist),
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

        # 利用自定义的信号去执行槽函数 taskImportlog
        allSignals.need_want_data.connect(taskImportlog)
        #######################################################################################

        # 显示主界面
        logMain.show()
        app.exec()
    except Exception as e:
        AppMainLogger.error(e)
