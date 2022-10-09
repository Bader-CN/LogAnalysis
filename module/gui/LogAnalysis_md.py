# -*- coding: utf-8 -*-

import os, re, csv, copy
from threading import Thread
from PySide6.QtGui import QFont
from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTreeWidgetItem, QTextEdit, QWidget, QTableView, QVBoxLayout, QFileDialog
from PySide6.QtSql import QSqlDatabase, QSqlQueryModel
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

    # 类变量
    msg_no_file = "No file needs to be insert"
    msg_export_no_select = "Plese select the data you want to export"
    msg_export_no_query = "Please query first and then export function can work"
    msg_export_not_full = "Selected data must be a matrix"
    current_db = None
    current_tb = None
    num_new_query = 1
    rmove_db_file = None


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
            self.ui.toolBar.addAction(self.ui.actionDeleteDB)
            self.update_db_list()

            # 默认信号和槽函数
            self.ui.treeWidget_db.itemExpanded.connect(self.set_current_db)
            self.ui.treeWidget_db.itemDoubleClicked.connect(self.slot_dblist_sql_query)
            self.ui.tabSQLQuery.tabCloseRequested['int'].connect(self.slot_tab_sqlquery_close)
            self.ui.tabSQLResult.tabCloseRequested['int'].connect(self.slot_tab_sqlresult_close)
            self.ui.btn_new.clicked.connect(self.slot_add_new_query)
            self.ui.btn_query.clicked.connect(self.slot_run_sql_query)
            self.ui.btn_export.clicked.connect(self.slot_export_to_csv)
            self.ui.treeWidget_db.clicked['QModelIndex'].connect(self.slot_set_remove_db_file)
            self.ui.line_search.textChanged.connect(self.set_sql_statement)
            self.ui.actionDeleteDB.triggered.connect(self.slot_action_delete)

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
        self.ui.tabLeft.setTabText(0, Language_zh_CN.get("Database"))
        self.ui.tabLeft.setTabText(1, Language_zh_CN.get("Template"))
        self.msg_no_file = Language_zh_CN.get("msg_no_file")
        self.msg_export_no_select = Language_zh_CN.get("msg_export_no_select")
        self.msg_export_no_query = Language_zh_CN.get("msg_export_no_query")
        self.msg_export_not_full = Language_zh_CN.get("msg_export_not_full")
        self.ui.menuFile.setTitle(Language_zh_CN.get("File"))
        self.ui.actionDeleteDB.setText(Language_zh_CN.get("DeleteDB"))

    def set_current_db(self, dbitem):
        """
        设置当前打开的 DB
        :param dbitem:
        :return:
        """
        dbname = dbitem.text(0) + ".db"
        self.current_db = os.path.abspath(os.path.join("./data/database", dbname))
        AppMainLogger.info("Current select DB is {}".format(dbname))
        self.statusBar().showMessage("Current DB is {}".format(dbname))

    def set_sql_statement(self, query = "", type=None, tabname=None, *args, **kwargs):
        """
        根据输入的内容自动生成 SQL 语句
        :param query: str, 来自 QLineEdit 中的内容
        :param type: database
        :param tabname: str
        :param args:
        :param kwargs:
        :return: str
        """
        str_time = self.ui.date_start_time.text().replace("/", "-")
        end_time = self.ui.date_end_time.text().replace("/", "-")
        key_word = self.ui.line_search.text()
        operater = "LIKE"
        if self.ui.chk_regexp.isChecked():
            operater = "REGEXP"
            key_word = "'{}'".format(self.ui.line_search.text())
        else:
            key_word = "'%{}%'".format(self.ui.line_search.text())

        # 如果类型来自于 database
        if type == "database":
            # 如果表名为 filehash, 则生成特殊的 SQL 语句
            if tabname == "filehash" and query == "":
                return "SELECT * FROM {};".format(tabname)
            elif tabname == "filehash" and query != "":
                return "SELECT * FROM {}\nWHERE filepath LIKE {};".format(tabname, key_word)
            elif tabname != "filehash" and query == "":
                return "SELECT * FROM {}\nWHERE log_time >= '{}' AND log_time <= '{}'\nORDER BY log_time DESC;".format(tabname, str_time, end_time)
            else:
                return "SELECT * FROM {}\nWHERE log_time >= '{}' AND log_time <= '{}' AND log_cont LIKE {}\nORDER BY log_time DESC;".format(tabname, str_time, end_time, key_word)

        # 如果类型来自于 template
        elif type == "template":
            pass

        # 如果是其它类型, 说明是被 QLineEdit 触发
        else:
            now_query = self.ui.tabSQLQuery.currentWidget().findChild(QTextEdit)
            sqlsource = now_query.toPlainText()
            if self.current_tb == "filehash" and query != "":
                now_query.setText("SELECT * FROM {}\nWHERE filepath {} {};".format(self.current_tb, operater, key_word))
            elif self.current_tb == "filehash" and query == "":
                now_query.setText("SELECT * FROM {};".format(self.current_tb))
            elif query != "":
                now_query.setText("SELECT * FROM {}\nWHERE log_time >= '{}' AND log_time <= '{}' AND log_cont {} {}\nORDER BY log_time DESC;".format(self.current_tb, str_time, end_time, operater,key_word))
            else:
                now_query.setText("SELECT * FROM {}\nWHERE log_time >= '{}' AND log_time <= '{}'\nORDER BY log_time DESC;".format(self.current_tb, str_time, end_time))

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
            AppMainLogger.info("Start finding files that match the rules...")
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

        # 更新 DB List UI
        self.update_db_list()

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

    def slot_dblist_sql_query(self, item):
        """
        双击表时自动生成 SQL 语句
        :param item: QTreeWidgetItem 对象
        :return:
        """
        dbfiles = os.listdir("./data/database")
        dbfiles = [dbfile[:-3] for dbfile in dbfiles]
        tabname = item.text(0)
        # 如果选择的不是 DB 名, 则根据对应的表来自动生成 SQL 语句
        if tabname not in dbfiles:
            sql_query_text = self.set_sql_statement(type = "database", tabname = tabname)
            SQLTextEdit = self.ui.tabSQLQuery.currentWidget().findChild(QTextEdit)
            SQLTextEdit.setText(sql_query_text)
            # 确定一个全局变量
            self.current_tb = tabname

    def slot_add_new_query(self):
        """
        槽函数：创建新的 Table 标签
        :return:
        """
        # 新建的 Tab 名字
        self.num_new_query += 1
        tablabel = 'Query' + str(self.num_new_query)
        tlaylout = 'Layout' + str(self.num_new_query)
        textedit = 'sqlEdit' + str(self.num_new_query)
        # 生成 QWidget 以及 QTextEdit 中的内容
        self.tab_page = QWidget()
        self.tab_page.setObjectName(tablabel)
        self.tab_layout = QVBoxLayout(self.tab_page)
        self.tab_layout.setObjectName(tlaylout)
        self.tab_text = QTextEdit(self.tab_page)
        self.tab_text.setObjectName(textedit)
        self.tab_layout.addWidget(self.tab_text)
        # 将生成的 QWidget 中的内容追加到 QTabWidget 中
        self.ui.tabSQLQuery.addTab(self.tab_page, tablabel)
        self.ui.tabSQLQuery.setObjectName(tablabel)
        # 设置当前索引为当前新建的 Tab
        self.ui.tabSQLQuery.setCurrentIndex(self.ui.tabSQLQuery.count() - 1)
        # 设置字体
        font = QFont()
        font.setFamily("Consolas")
        self.tab_text.setFont(font)

    def slot_tab_sqlquery_close(self, index):
        """
        槽函数：SQL Query Tab 关闭函数
        :param index: QtabWidget 的 index
        """
        if self.ui.tabSQLQuery.count() > 1:
            self.ui.tabSQLQuery.removeTab(index)

    def slot_tab_sqlresult_close(self, index):
        """
        槽函数: SQL Result Tab 关闭函数
        :param index:
        :return:
        """
        if self.ui.tabSQLResult.count() > 1:
            self.ui.tabSQLResult.removeTab(index)

    def slot_run_sql_query(self):
        """
        槽函数：执行查询语句, 并且返回结果
        :return:
        """
        # 获取 sqlEdit 上一级的对象名
        sqltitle = self.ui.tabSQLQuery.currentWidget().objectName()
        # sqlEdit 返回的是当前激活的 QTextEdit 对象
        sqlEdit = self.ui.tabSQLQuery.currentWidget().findChild(QTextEdit)
        sqlText = sqlEdit.toPlainText().split(";")[0] + ";"

        # 如果获取的内容长度非0, 并且当前 db 不是 None, 则继续执行查询
        if len(sqlText) != 0 and self.current_db != None:
            querydb = QSqlDatabase.addDatabase('QSQLITE')
            # 启用正则表达式
            # https://doc.qt.io/qtforpython/overviews/sql-driver.html#enable-regexp-operator
            # https://doc.qt.io/qt-6/qsqldatabase.html#setConnectOptions
            querydb.setConnectOptions("QSQLITE_ENABLE_REGEXP")
            querydb.setDatabaseName(self.current_db)
            querydb.open()

            # 创建 model
            model = QSqlQueryModel()
            model.setQuery(sqlText, db=querydb)
            # 判断返回的数据是否多余 256 行, 如果多余 256 行, 则允许获取更多的数据 (fetchmode 意思是判断是否有更多的数据)
            # 参考链接 https://xbuba.com/questions/42286016
            while model.canFetchMore():
                model.fetchMore()
            # 校验语句是否出现错误
            if model.lastError().isValid():
                AppMainLogger.warning((model.lastError().text()))
                QMessageBox.warning(self, "SQL Error", model.lastError().text())
            else:
                AppMainLogger.info("SQL Query is: {}".format(sqlText))

            # 生成 QWidget 和 QtableView 对象: self.tab_view
            tablabel = sqltitle.replace('Query','Result')
            self.tab_page_result = QWidget()
            self.tab_page_result.setObjectName(tablabel)
            self.tab_layout_result = QVBoxLayout(self.tab_page_result)
            self.tab_view = QTableView(self.tab_page_result)
            self.tab_view.setObjectName(tablabel)
            self.tab_layout_result.addWidget(self.tab_view)

            # 将生成的 QWidget 追加到 QTabWidget 中
            self.ui.tabSQLResult.addTab(self.tab_page_result, tablabel)
            self.ui.tabSQLResult.setObjectName(tablabel)
            self.ui.tabSQLResult.setCurrentIndex(self.ui.tabSQLResult.count() - 1)

            # 展示表格并优化显示
            self.tab_view.setModel(model)
            ## 水平方向标签拓展剩下的窗口部分
            self.tab_view.horizontalHeader().setStretchLastSection(True)
            # self.tab_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            ## 设置单元格默认的行高
            self.tab_view.verticalHeader().setDefaultSectionSize(8)
            ## 设置单元格显示的字体
            self.tab_view.setFont(QFont('Consolas', 8, QFont.Normal))
            ## 自动调整每列的宽度
            self.tab_view.resizeColumnsToContents()
            ## 自动换行
            self.tab_view.setWordWrap(True)
            ## 隐藏行号
            self.tab_view.verticalHeader().hide()
            ## 连接槽函数, 在双击单元格时触发
            # self.tab_view.doubleClicked.connect(self.slot_show_cell)
            self.tab_view.show()

            # 关闭数据库连接
            querydb.close()

    def slot_export_to_csv(self):
        """
        将查询的数据导出到 csv 文件, 代码参考了如下链接:
        https://doc.qt.io/qtforpython/PySide6/QtWidgets/QAbstractItemView.html?highlight=selectionmodel#PySide6.QtWidgets.PySide6.QtWidgets.QAbstractItemView.model
        https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlRecord.html#PySide6.QtSql.PySide6.QtSql.QSqlRecord.fieldName
        https://cloud.tencent.com/developer/ask/sof/1252779
        :return:
        """
        # 判断有没有选择数据
        try:
            self.statusBar().showMessage("Checking the selected data, please wait...", timeout=5)
            isSelect = self.ui.tabSQLResult.currentWidget().findChild(QTableView).selectionModel().selectedIndexes()
            if isSelect != []:
                tableview = self.ui.tabSQLResult.currentWidget().findChild(QTableView)
                sqlrecord = tableview.selectionModel().model().record(0)
                rows_index = []
                columns_index = []
                select_datas = []
                # 获取选中的数据
                sqldatas = tableview.selectionModel().selectedIndexes()
                for sqldata in sqldatas:
                    if sqldata.column() not in columns_index:
                        columns_index.append(sqldata.column())
                    if sqldata.row() not in rows_index:
                        rows_index.append(sqldata.row())
                    select_datas.append(sqldata.data())

                # 判断数据是否符合要求
                if len(select_datas) == len(rows_index) * len(columns_index):
                    path, ok = QFileDialog.getSaveFileName(self, 'Export to CSV', os.getenv('HOME'), '*.csv')
                    if ok:
                        self.statusBar().showMessage("Exporting, please wait...")

                        # 列的标题名
                        columns_header = [sqlrecord.fieldName(x) for x in columns_index]

                        # 整理数据, 按组分割
                        csv_datas = [select_datas[i: i + len(columns_header)] for i in range(0, len(select_datas), len(columns_header))]

                        # 将数据写入到 csv 中
                        with open(path, "w", encoding="utf-8") as f:
                            write = csv.writer(f, lineterminator="\n")
                            write.writerow(columns_header)
                            write.writerows(csv_datas)
                        self.statusBar().showMessage("Export is complete! filepath: {}".format(path))
                else:
                    QMessageBox.warning(self, "Warning", self.msg_export_not_full)
            else:
                QMessageBox.warning(self, "Warning", self.msg_export_no_select)
        except:
            QMessageBox.warning(self, "Warning", self.msg_export_no_query)

    def slot_set_remove_db_file(self):
        """
        槽函数：设定需要删除数据库的文件
        """
        try:
            self.rmove_db_file = os.path.join('.\data\database', self.ui.treeWidget_db.currentItem().parent().text(0) + '.db')
        except:
            self.rmove_db_file = os.path.join('.\data\database', self.ui.treeWidget_db.currentItem().text(0) + '.db')

    def slot_action_delete(self):
        """
        槽函数：删除指定的 SQLite 数据库
        """
        if self.rmove_db_file != None:
            try:
                os.remove(self.rmove_db_file)
                self.update_db_list()
            except Exception as e:
                AppMainLogger.error(e)

    def update_db_list(self):
        """
        更新数据库列表信息
        :return:
        """
        # 清空 DB List 原始内容
        self.ui.treeWidget_db.clear()

        # 获取目录下的数据库文件
        dbfiles = os.listdir('./data/database')
        if dbfiles != []:
            # 如果存在 SQLite DB 文件, 则循环获取每个数据库包含的表名, 并保存在字典 dbinfo 里
            dbinfo = {}
            for dbfile in dbfiles:
                dbpath = os.path.abspath(os.path.join('./data/database', dbfile))
                db = QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName(dbpath)
                db.open()
                dbinfo[dbfile] = (sorted(db.tables()))
                db.close()

            # 获取了表后, 更新 DB List 内容
            for db, tbs in dbinfo.items():
                root = QTreeWidgetItem(self.ui.treeWidget_db)
                root.setText(0, db[:-3])
                # 进一步更新 DB List 的二级内容
                for tb in tbs:
                    sub_item = QTreeWidgetItem(root)
                    sub_item.setText(0, tb)
        else:
            # 如果没有 SQLite DB 文件, 则直接清空内容
            self.ui.treeWidget_db.clear()

