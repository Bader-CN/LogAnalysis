# -*- coding: utf-8 -*-

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow
from module.gui.LogAnalysis_ui import Ui_MainWindow
from module.tools.AppSettings import ReadConfig
from module.tools.AppDebug import AppMainLogger


class LogAnalysisMain(QMainWindow):
    """
    LogAnalysis main window settings
    """
    Language_zh_CN = {
        "Start Time": "开始时间",
        "End Time": "结束时间",
        "New": "新建",
        "Import": "导入",
        "Export": "导出",
        "Help": "帮助",
        "Query": "查询",
        "Enable Regrxp": "正则表达式",
        "Inclube Component": "包括组件",
        "Database": "数据",
        "Template": "模板",
    }

    def __init__(self):
        AppMainLogger.debug("Start initing AppGUI")
        # 继承 QMainWindow 父类
        super().__init__()
        # 导入自定义界面 (module.gui.LogAnalysis_ui.Ui_MainWindow)
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)
        AppMainLogger.debug("End initing AppGUI")

        # 调整软件界面
        self.setui_start_end_time()
        self.setui_language()

    # 调整软件界面
    def setui_start_end_time(self):
        """
        软件启动时, 设置 Start/End Time 的显示时间
        :return:
        """
        AppMainLogger.debug("Start setting setDateTime")
        self.ui.date_start_time.setDateTime(QDateTime.addDays(QDateTime.currentDateTime(), -30))
        self.ui.date_end_time.setDateTime(QDateTime.currentDateTime())
        AppMainLogger.debug("End setting setDateTime")

    # 调整显示语言
    def setui_language(self):
        """
        根据配置文件来显示软件语言
        :return:
        """
        if ReadConfig.get_language() == "zh_CN":
            AppMainLogger.debug("Start setting AppGUI to Chinese(zh_CN)")
            self.setui_zh_CN()
            AppMainLogger.debug("End setting AppGUI to Chinese(zh_CN)")

    def setui_zh_CN(self):
        """
        将软件界面设置为中文
        :return:
        """
        self.ui.label_start_time.setText(self.Language_zh_CN.get("Start Time"))
        self.ui.label_end_time.setText(self.Language_zh_CN.get("End Time"))
        self.ui.btn_new.setText(self.Language_zh_CN.get("New"))
        self.ui.btn_import.setText(self.Language_zh_CN.get("Import"))
        self.ui.btn_export.setText(self.Language_zh_CN.get("Export"))
        self.ui.btn_help.setText(self.Language_zh_CN.get("Help"))
        self.ui.btn_query.setText(self.Language_zh_CN.get("Query"))
        self.ui.chk_regexp.setText(self.Language_zh_CN.get("Enable Regrxp"))
        self.ui.chk_component.setText(self.Language_zh_CN.get("Inclube Component"))
        self.ui.tabLeft.setTabText(0, self.Language_zh_CN.get("Database"))
        self.ui.tabLeft.setTabText(1, self.Language_zh_CN.get("Template"))
