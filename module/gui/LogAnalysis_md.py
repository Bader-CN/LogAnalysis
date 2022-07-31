# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow
from module.gui.LogAnalysis_ui import Ui_MainWindow


class LogAnalysisMain(QMainWindow):
    """
    LogAnalysis main window settings
    """
    def __init__(self):
        # 继承 QMainWindow 父类
        super().__init__()
        # 导入自定义界面 (module.gui.LogAnalysis_ui.Ui_MainWindow)
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)
