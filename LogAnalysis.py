# -*- coding: utf-8 -*-

import os
from PySide6.QtWidgets import QApplication
from module.gui.LogAnalysis_md import LogAnalysisMain

if __name__ == '__main__':
    # 检查相关目录及文件是否存在
    if not os.path.exists("./log"):
        os.mkdir("./log")

    # 启动软件
    app = QApplication([])

    # 实例化并显示 LogAnalysis 主界面
    logMain = LogAnalysisMain()
    logMain.show()

    app.exec()
