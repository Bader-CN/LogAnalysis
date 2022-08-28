# -*- coding: utf-8 -*-

import os
from PySide6.QtWidgets import QApplication
from module.gui.LogAnalysis_md import LogAnalysisMain
from module.gui.LogImport_md import LogAnalysisImport

if __name__ == '__main__':
    # 检查相关目录及文件是否存在
    if not os.path.exists("./log"):
        os.mkdir("./log")
    if not os.path.exists("./data/database"):
        os.mkdir("./data/database")
    if not os.path.exists("./data/template"):
        os.mkdir("./data/template")

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

    # 显示主界面
    logMain.show()

    app.exec()
