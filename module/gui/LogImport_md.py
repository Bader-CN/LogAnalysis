# -*- coding: utf-8 -*-

from PySide6.QtCore import QDir
from PySide6.QtWidgets import QWidget, QFileSystemModel
from module.gui.LogImport_ui import Ui_Form
from module.tools.AppSettings import ReadConfig
from module.tools.AppDebug import AppMainLogger


class LogAnalysisImport(QWidget):
    """
    LogAnalysis Import GUI
    """
    # QTreeView.setModel() 可以加载此模型
    path_model = QFileSystemModel()

    def __init__(self):
        # 继承父类 QWidget
        super().__init__()
        # 导入自定义 Ui_From 界面 (module.gui.LogImport_ui.Ui_From)
        self.ui = Ui_Form()
        # 初始化界面
        self.ui.setupUi(self)

        # 调整软件界面
        self.setWindowTitle("Import Wizard")
        self.setui_language_by_import()
        self.set_max_process()
        self.set_path_type()
        self.set_path_tree()

    def setui_language_by_import(self):
        """
        根据配置文件来显示软件语言
        :return:
        """
        if ReadConfig.get_language() == "zh_CN":
            AppMainLogger.debug("Start setting logImport GUI to Chinese(zh_CN)")
            self.setui_zh_CN()
            AppMainLogger.debug("End setting logImport GUI to Chinese(zh_CN)")

    def setui_zh_CN(self):
        """
        将软件界面设置为中文
        :return:
        """
        from module.language.i18n_zh_CN import Language_zh_CN
        self.setWindowTitle(Language_zh_CN.get("Import Wizard"))
        self.ui.label_abspath.setText(Language_zh_CN.get("Path"))
        self.ui.btn_select_file_or_path.setText(Language_zh_CN.get("Select"))
        self.ui.label_max_process.setText(Language_zh_CN.get("Max of Processes"))
        self.ui.label_path_type.setText(Language_zh_CN.get("Path Type"))
        self.ui.label_company.setText(Language_zh_CN.get("Company"))
        self.ui.label_product_line.setText(Language_zh_CN.get("Product Line"))
        self.ui.label_product.setText(Language_zh_CN.get("Product Name"))
        self.ui.btn_import.setText(Language_zh_CN.get("Import"))
        self.ui.btn_cancel.setText(Language_zh_CN.get("Cancel"))

    def set_max_process(self):
        """
        设定日志读取的进程数量值
        :return:
        """
        # 根据 CPU 核心数来加载所有可能的选项
        max_process = ReadConfig.get_cpu_count()
        AppMainLogger.debug("CPU total is {} core".format(max_process))
        num_list = [str(x) for x in range(1, max_process+1)]
        self.ui.combox_max_process.addItems(num_list)

        # 根据配置文件的设置, 来决定默认的值
        number = ReadConfig.get_max_process()
        self.ui.combox_max_process.setCurrentIndex(num_list.index(str(number)))
        AppMainLogger.debug("set {} read processes".format(number))

    def set_path_type(self):
        """
        设置想要指定的路径类型, 可选为 Folder 或 File
        :return:
        """
        self.ui.combox_path_type.addItems(["Folder", "File"])
        # 连接槽函数: slot_set_path_tree
        self.ui.combox_path_type.activated.connect(self.slot_set_path_tree)

    def set_path_tree(self):
        """
        设置左方的文件列表, 如果文件类型为 Folder, 则不显示文件
        :return:
        """
        AppMainLogger.debug("Start setting path tree")
        self.path_model.setRootPath(QDir.rootPath())
        # QFileSystemModel 默认有4列, 分别为 Name, size, type, modified
        # 如果不想显示, 可以调用 QTreeView.setColumnHidden(<column_index>, True) 来隐藏掉
        self.ui.tree_filedir.setModel(self.path_model)
        self.ui.tree_filedir.setColumnHidden(1, True)
        self.ui.tree_filedir.setColumnHidden(2, True)
        self.ui.tree_filedir.setColumnHidden(3, True)
        # 如果文件类型为 Folder, 则不显示文件
        if self.ui.combox_path_type.currentText() == "Folder":
            # default filter 是 AllEntries | NoDotAndDotDot | AllDirs
            self.path_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        # 将点击鼠标的事件连接到 get_path_tree()
        self.ui.tree_filedir.clicked.connect(self.get_path_tree)
        AppMainLogger.debug("End setting path tree")

    def get_path_tree(self):
        """
        将选定的 QTableView 的值写在 lineEdit 中
        :return:
        """
        fullpath = self.path_model.filePath(self.ui.tree_filedir.currentIndex())
        self.ui.lineEdit.setText(fullpath)
        AppMainLogger.info("Clicked & Add Path [{}]".format(fullpath))

    def slot_set_path_tree(self):
        """
        判断路径类型, 根据路径类型来决定显示什么内容
        :return:
        """
        if self.ui.combox_path_type.currentText() == "Folder":
            # 新建一个模型, 重新进行设定 (http://www.qtcn.org/bbs/read.php?tid-32891.html)
            self.path_model = QFileSystemModel()
            self.path_model.setRootPath(QDir.rootPath())
            # default filter 是 AllEntries | NoDotAndDotDot | AllDirs
            self.path_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
            self.ui.tree_filedir.setModel(self.path_model)
            AppMainLogger.debug("Change QTableView's model Filter type to [QDir.AllDirs | QDir.NoDotAndDotDot]")
        else:
            # 新建一个模型, 重新进行设定 (http://www.qtcn.org/bbs/read.php?tid-32891.html)
            self.path_model = QFileSystemModel()
            self.path_model.setRootPath(QDir.rootPath())
            self.path_model.setFilter(QDir.AllEntries | QDir.AllDirs | QDir.NoDotAndDotDot)
            self.ui.tree_filedir.setModel(self.path_model)
            AppMainLogger.debug("Change QTableView's model Filter type to [QDir.AllEntries | QDir.AllDirs | QDir.NoDotAndDotDot]")
