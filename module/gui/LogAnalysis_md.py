# -*- coding: utf-8 -*-

from PySide6.QtCore import QDateTime
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

        # 设置时间
        self.set_start_end_time()

    # 调整软件界面
    def set_start_end_time(self):
        """
        软件启动时, 设置 Start/End Time 的显示时间
        :return:
        """
        self.ui.date_start_time.setDateTime(QDateTime.addDays(QDateTime.currentDateTime(), -30))
        self.ui.date_end_time.setDateTime(QDateTime.currentDateTime())