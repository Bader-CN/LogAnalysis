# -*- coding: utf-8 -*-

import os, re, copy, hashlib
from threading import Thread
from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow, QMessageBox
from module.gui.LogAnalysis_ui import Ui_MainWindow
from module.tools.AppSettings import ReadConfig
from module.tools.HashTools import HashTools
from module.tools.AppDebug import AppMainLogger
from module.bridge.customSignals import allSignals
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from multiprocessing import Queue, Process


class LogAnalysisMain(QMainWindow):
    """
    LogAnalysis main window settings
    """
    msg_no_file = "No file needs to be insert!"

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
            allSignals.need_want_data.connect(self.slot_importlog_to_db)

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
        self.msg_no_file = Language_zh_CN.get("msg_no_file")

    def slot_check_taskdict(self, dict):

        # 定义待分析函数
        def check_taskdict(dict):
            # 加载文件规则
            if dict.get("company") == "MicroFocus" and dict.get("productline") == "ITOM" and dict.get("product") == "Operations Agent(OA)":
                from rules.MicroFocus.ITOM import OA_FileRule as FileRule
                from rules.MicroFocus.ITOM import OA_SQLTable as SQLTable

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

                # 此时字典里存储的是所有符合条件的文件
                dict["files"] = allfiles

                # 判断此时符合的文件是否为空, 非空才会继续处理
                if allfiles == []:
                    QMessageBox.warning(self, "Warning", self.msg_no_file)
                else:
                    # 实例化计算哈希工具, 准备后面进行文件哈希计算
                    hash = HashTools()

                    # 准备数据库会话
                    engine = create_engine("sqlite:///" + dict.get("targetdb"), future=True)
                    Session = sessionmaker(engine)
                    hash_session = Session()

                    if os.path.exists(dict.get("targetdb")):
                        AppMainLogger.info("Open the specified database:[{}]".format(dict.get("targetdb")))
                        # 遍历所有符合的文件, 检查是否存在重复的文件
                        # 需要复制一份字典, 否则会更改原数据
                        indexdict = copy.deepcopy(allfiles)
                        for file in indexdict:
                            filehash = hash.filehash(file)
                            # 如果数据库里有对应的数据, 则将对应的文件从 allfiles 中移除掉
                            query = hash_session.query(SQLTable.FileHash).filter(SQLTable.FileHash.hash == filehash).first()
                            if query:
                                allfiles.remove(file)
                                AppMainLogger.debug("Will not be ingest file:[{}]".format(file))
                            # 如果数据库里没有, 则将此文件的哈希值添加到数据库中
                            else:
                                sqldata = SQLTable.FileHash(filepath=file, hash=filehash)
                                hash_session.add(sqldata)
                                AppMainLogger.debug("Will insert file:[{}], file hash is:[{}]".format(file, filehash))
                        # 提交并关闭会话连接
                        hash_session.commit()
                        hash_session.close()

                        # 如果所有allfiles 里面没有数据, 则说明没有数据需要导入
                        if allfiles == []:
                            QMessageBox.warning(self, "Warning", self.msg_no_file)
                        else:
                            # 预处理完成的数据
                            print(dict)
                            self.statusBar().showMessage("checking file hash")
                            # 发射信号, 将预处理的字典数据传递给日志分析进程
                            allSignals.need_want_data.emit(dict)

                    else:
                        AppMainLogger.info("Create a new database:[{}]".format(dict.get("targetdb")))
                        # 创建数据库
                        SQLTable.BASE.metadata.create_all(engine)
                        # 针对每个文件计算哈希值, 并将数据写入到数据库中
                        for file in allfiles:
                            filehash = hash.filehash(file)
                            sqldata = SQLTable.FileHash(filepath=file, hash=filehash)
                            hash_session.add(sqldata)
                            AppMainLogger.debug("Will insert file:[{}], file hash is:[{}]".format(file, filehash))
                        # 提交并关闭会话连接
                        hash_session.commit()
                        hash_session.close()

                        # 预处理完成的数据
                        print(dict)
                        self.statusBar().showMessage("checking file hash")
                        # 发射信号, 将预处理的字典数据传递给日志分析进程
                        allSignals.need_want_data.emit(dict)

        check_taskdict(dict)