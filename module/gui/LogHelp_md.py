# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from module.gui.LogHelp_ui import Ui_Form

class LogAnalysisHelp(QWidget):
    """
    LogAnalysis Help Documents for MarkDown
    """
    def __init__(self):
        # 继承父类
        super().__init__()
        # 初始化 GUI
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 调整界面
        self.setWindowTitle("Help Documents")