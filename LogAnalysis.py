# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QApplication
from module.gui.LogAnalysis_md import LogAnalysisMain

if __name__ == '__main__':
    app = QApplication([])

    # 实例化并显示 LogAnalysis 主界面
    logMain = LogAnalysisMain()
    logMain.show()

    app.exec()
