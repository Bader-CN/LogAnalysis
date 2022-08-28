# -*- coding: utf-8 -*-

import os, re, hashlib
from threading import Thread
from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow
from module.gui.LogAnalysis_ui import Ui_MainWindow
from module.tools.AppSettings import ReadConfig
from module.tools.AppDebug import AppMainLogger
from module.bridge.customSignals import allSignals


class LogAnalysisMain(QMainWindow):
    """
    LogAnalysis main window settings
    """
    def __init__(self):
        try:
            # 继承 QMainWindow 父类
            super().__init__()
            # 导入自定义界面 (module.gui.LogAnalysis_ui.Ui_MainWindow)
            self.ui = Ui_MainWindow()
            # 初始化界面
            self.ui.setupUi(self)

            # 调整软件界面
            self.setWindowTitle("LogAnalysis alpha")
            self.set_start_end_time()
            self.set_language_by_main()

            # 定制信号连接槽函数
            allSignals.user_want_data.connect(self.slot_check_taskdict)

        except Exception as e:
            AppMainLogger.error(e)

    # 调整软件界面
    def set_start_end_time(self):
        """
        软件启动时, 设置 Start/End Time 的显示时间
        :return:
        """
        self.ui.date_start_time.setDateTime(QDateTime.addDays(QDateTime.currentDateTime(), -30))
        self.ui.date_end_time.setDateTime(QDateTime.currentDateTime())

    # 调整显示语言
    def set_language_by_main(self):
        """
        根据配置文件来显示软件语言
        :return:
        """
        if ReadConfig.get_language() == "zh_CN":
            AppMainLogger.info("MainGUI Language setting to zh_CN")
            self.set_zh_CN()

    def set_zh_CN(self):
        """
        将软件界面设置为中文
        :return:
        """
        from module.language.i18n_zh_CN import Language_zh_CN
        self.ui.label_start_time.setText(Language_zh_CN.get("Start Time"))
        self.ui.label_end_time.setText(Language_zh_CN.get("End Time"))
        self.ui.btn_new.setText(Language_zh_CN.get("New"))
        self.ui.btn_import.setText(Language_zh_CN.get("Import"))
        self.ui.btn_export.setText(Language_zh_CN.get("Export"))
        self.ui.btn_help.setText(Language_zh_CN.get("Help"))
        self.ui.btn_query.setText(Language_zh_CN.get("Query"))
        self.ui.chk_regexp.setText(Language_zh_CN.get("Enable Regrxp"))
        self.ui.chk_component.setText(Language_zh_CN.get("Inclube Component"))
        self.ui.tabLeft.setTabText(0, Language_zh_CN.get("Database"))
        self.ui.tabLeft.setTabText(1, Language_zh_CN.get("Template"))

    def slot_check_taskdict(self, dict):

        # 定义待分析函数
        def check_taskdict(dict):
            # 加载文件规则
            if dict.get("company") == "MicroFocus" and dict.get("productline") == "ITOM" and dict.get("product") == "Operations Agent(OA)":
                from rules.MicroFocus.ITOM import OA_FileRule as FileRule

            # 输出待导入的文件
            if dict.get("pathtype") == "File":
                allfiles = [dict.get("path")]
            else:
                # 需要遍历目录, 找出所有的文件
                allfiles = []
                isNeed = False
                isBlck = False
                for root, dirs, files in os.walk(dict.get("path")):
                    for file in files:
                        # 生成文件的绝对路径
                        filepath = os.path.join(root, file)
                        # 判断每个文件是否需要导入
                        for needfilerule in FileRule.NeedFilesRule:
                            # 如果符合匹配列表: FileRule.NeedFilesRule, 将标记位 isNeed 设置为 True
                            if re.search(needfilerule, filepath, re.IGNORECASE):
                                isNeed = True
                            # 如果符合反匹列表: FileRule.BlckFilesRule, 将标记位 isBlck 设置为 True
                            for blckfilerule in FileRule.BlckFilesRule:
                                if re.search(blckfilerule, filepath, re.IGNORECASE):
                                    isBlck = True
                            # 如果符合匹配列表, 并且不在反匹列表, 则将此目录加入到 allfiles 列表里
                            if isNeed == True and isBlck == False:
                                allfiles.append(filepath)
                            # 初始化标记位
                            isNeed = False
                            isBlck = False

                # 展示准备处理的文件/hash
                dict["files"] = allfiles
                print(dict)
                for file in allfiles:
                    print(file)

        check_taskdict(dict)