# -*- coding: utf-8 -*-

import os, re, copy, time, hashlib
from threading import Thread
from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow, QMessageBox
from module.gui.LogAnalysis_ui import Ui_MainWindow
from module.tools.AppSettings import ReadConfig
from module.tools.HashTools import HashTools
from module.tools.AppDebug import AppMainLogger
from module.bridge.customSignals import allSignals
from module.bridge.customQueues import QTask
from module.bridge.customQueues import QData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
            self.ui.progressBar.hide()

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
        self.msg_no_file = Language_zh_CN.get("msg_no_file")

    def check_taskdict(self, dict):
        """
        实际的预检查函数, 负责查找哪些文件符合导入规则
        :param dict: 字典类型的预处理数据
        :return:{"Signal": "Start"} / {"Signal": "Stop"}
        """
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

            # 开始遍历符合规则的文件
            AppMainLogger.info("Start finding files that match the rules ……")
            self.statusBar().showMessage("Finding files that match the rules ……")
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
                self.statusBar().clearMessage()
                AppMainLogger.warning("No file matching the rules")
                QMessageBox.warning(self, "Warning", self.msg_no_file)
                # 返回停止信号
                return {"Signal": "Stop"}

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
                        self.statusBar().clearMessage()
                        AppMainLogger.warning("No file needs to be imported because the file already exists")
                        QMessageBox.warning(self, "Warning", self.msg_no_file)
                        # 返回停止信号
                        return {"Signal": "Stop"}
                    else:
                        # 发射信号, 将预处理的字典数据传递给日志分析进程
                        allSignals.need_want_data.emit(dict)
                        self.statusBar().clearMessage()
                        # 返回开始信号
                        return {"Signal": "Start"}

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
                    # 发射信号, 将预处理的字典数据传递给日志分析进程
                    allSignals.need_want_data.emit(dict)
                    self.statusBar().clearMessage()
                    # 返回开始信号
                    return {"Signal": "Start"}

    def import_to_db(self):
        """
        获取管道里面的数据, 并将数据保存到数据库中
        :return:
        """
        path = r"sqlite:///"
        tasksnum = 0
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        # 从 QData 队列里获取数据, 并将获取到的数据写入到数据库中
        while True:
            dict = QData.get()
            totalnum = dict.get("total")
            try:
                # 任务首次, 创建 SQLAlchemy 会话, 写入数据
                if path == r"sqlite:///":
                    path = r"sqlite:///" + os.path.abspath(dict.get("targetdb"))
                    engine = create_engine(path, future=True)
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    session.add_all(dict.get("data"))
                    session.commit()
                    tasksnum += 1
                # 后续内容, 因为 SQLAlchemy 会话已经存在, 所以直接写入数据
                else:
                    session.add_all(dict.get("data"))
                    session.commit()
                    tasksnum += 1
            except Exception as e:
                # 如果出现了异常, 为了程序能够正常结束, tasksnum 计数仍然 + 1
                tasksnum += 1
                AppMainLogger.warning("Write to SQLiteDB faild, file is [{}], result is:\n{}".format(dict.get("file"), e))

            # 追加 debug 日志
            AppMainLogger.debug("Successful write to SQLiteDB, finish {}%, targetdb is:[{}]".format(str(int((tasksnum/totalnum)*100)), dict.get("targetdb")))

            # 更新进度条
            self.ui.progressBar.setValue(int((tasksnum/totalnum)*100))
            self.ui.progressBar.text()
            # 判断条件, 如果进度达到 100%, 则退出循环
            if int((tasksnum/totalnum)*100) == 100:
                self.ui.progressBar.hide()
                break

    def slot_check_taskdict(self, dict):
        """
        利用槽函数来调用真正的 check_taskdict(), 写入部分将采用子线程
        :param dict: 字典类型的预处理数据
        :return:
        """
        task_result = self.check_taskdict(dict)
        # 如果收到的信号是 {"Signal": "Stop"}, 则启动数据库写入线程
        if task_result.get("Signal") == "Start":
            t1 = Thread(target=self.import_to_db, daemon=True)
            t1.start()