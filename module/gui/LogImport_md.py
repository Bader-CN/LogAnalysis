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
    # 所有软件的分类数据
    category_dict = {
        "MicroFocus": {
            "IMG": ["Connected Backup(CBK)", "IDOL"],
            "ITOM": ["Operations Agent(OA)", "Operations Bridge Manager(OBM)"], },

        "Company1": {"ProductLine1": ["ProductName1", "ProductName2"], }
    }

    def __init__(self):
        # 继承父类 QWidget
        super().__init__()
        # 导入自定义 Ui_From 界面 (module.gui.LogImport_ui.Ui_From)
        self.ui = Ui_Form()
        # 初始化界面
        self.ui.setupUi(self)
        # 加载原始语言
        self.ui.usernote.setText("""Note:
1. Import function will cost much CPU and Memory
    > this value is determined by "Number of Processes"
    > Temporary modify: "Number of Processes"
    > Permanent modify: "config.cfg"

2. Select button to select the specified file or folder
    > The file or folder is determined by "path type"
    > Can click a file or folder on the left to add it auto
    > Double click to expand subdirectories""")

        # 调整软件界面
        self.setWindowTitle("Import Wizard")
        self.set_language_by_import()
        self.set_max_process()
        self.set_path_type()
        self.set_path_tree()
        self.set_default_comboxs()

        # 连接槽函数
        self.ui.combox_company.activated.connect(self.slot_combox_company)
        self.ui.combox_product_line.activated.connect(self.slot_combox_product_line)
        self.ui.btn_cancel.clicked.connect(self.close)

    def set_language_by_import(self):
        """
        根据配置文件来显示软件语言
        :return:
        """
        if ReadConfig.get_language() == "zh_CN":
            AppMainLogger.debug("Start setting logImport GUI to Chinese(zh_CN)")
            self.set_zh_CN()
            AppMainLogger.debug("End setting logImport GUI to Chinese(zh_CN)")

    def set_zh_CN(self):
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
        self.ui.usernote.setText(Language_zh_CN.get("User Note"))

    def set_max_process(self):
        """
        设定日志读取的进程数量值
        :return:
        """
        # 获取处理器物理核心数量
        num_cpu_count = ReadConfig.get_cpu_count()
        AppMainLogger.debug("CPU have {} core".format(num_cpu_count))
        # 根据配置文件来决定可能的进程数
        max_processes = ReadConfig.get_max_process()
        AppMainLogger.debug("ConfigFile App_Optimiz.Max_Processes's value: {}".format(max_processes))
        if max_processes in ["Auto", "auto"]:
            max_processes = num_cpu_count
        elif num_cpu_count >= int(max_processes):
            max_processes = num_cpu_count
        else:
            max_processes = int(max_processes)
        AppMainLogger.debug("Final max_processes will set to {}".format(str(max_processes)))
        num_list = [str(x) for x in range(1, max_processes+1)]
        self.ui.combox_max_process.addItems(num_list)

        # 进程数的默认数值
        number = ReadConfig.get_max_process()
        # 如果值是 Auto, 则默认为物理核心数 - 1
        if number in ["Auto", "auto"]:
            number = ReadConfig.get_cpu_count() - 1
        # 如果该值小于等于 2, 则固定返回 2
        elif int(number) <= 2:
            number = 2
        # 其余情况, 则返回指定的值
        else:
            number = int(number)
        AppMainLogger.debug("Default max_processes value to {}".format(str(number)))

        self.ui.combox_max_process.setCurrentIndex(num_list.index(str(number)))

    def set_path_type(self):
        """
        设置想要指定的路径类型, 可选为 Folder 或 File
        :return:
        """
        self.ui.combox_path_type.addItems(["Folder", "File"])
        # 连接槽函数: slot_set_path_tree
        self.ui.combox_path_type.activated.connect(self.slot_change_path_tree)

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
        # 连接槽函数: 将点击鼠标的事件连接到 get_path_tree()
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

    def set_default_comboxs(self):
        """
        当点击导入按钮后, 默认显示 ComboBox(组合框) 的值
        :return:
        """
        AppMainLogger.debug("Start setting Company, ProductLine and Product")
        # 设置 ComboBox(组合框) 的值: 公司
        companys = [x for x in self.category_dict]
        self.ui.combox_company.addItems(companys)
        # 设置 ComboBox(组合框) 的值: 产品线
        current_company = self.ui.combox_company.currentText()
        productlines = self.category_dict.get(current_company)
        productlines = [x for x in productlines]
        self.ui.combox_product_line.addItems(productlines)
        # 设置 ComboBox(组合框) 的值: 产品
        current_proline = self.ui.combox_product_line.currentText()
        products = self.category_dict.get(current_company).get(current_proline)
        self.ui.combox_product.addItems(products)
        AppMainLogger.debug("End setting Company, ProductLine and Product")

    def slot_change_path_tree(self):
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

    def slot_combox_company(self):
        """
        根据当前公司的 ComboBox(组合框) 里的值, 来决定 Company, ProductLine, Product 的值
        :return:
        """
        current_company = self.ui.combox_company.currentText()
        AppMainLogger.debug("QComboBox by Company is activated, now value is: {}".format(current_company))
        productlines = self.category_dict.get(current_company)
        productlines = [x for x in productlines]
        self.ui.combox_product_line.clear()
        self.ui.combox_product_line.addItems(productlines)
        AppMainLogger.debug("addItems in ProductLine: {}".format(str(productlines)))
        current_proline = self.ui.combox_product_line.currentText()
        products = self.category_dict.get(current_company).get(current_proline)
        self.ui.combox_product.clear()
        self.ui.combox_product.addItems(products)
        AppMainLogger.debug("addItems in Products: {}".format(str(products)))

    def slot_combox_product_line(self):
        """
        根据当产品线 ComboBox(组合框) 里的值, 来决定 Product 里的值
        :return:
        """
        current_company = self.ui.combox_company.currentText()
        current_productline = self.ui.combox_product_line.currentText()
        AppMainLogger.debug("QComboBox by ProductLine is activated, now value is: {}".format(current_productline))
        productlinesdb = self.category_dict.get(current_company)
        products = productlinesdb.get(current_productline)
        self.ui.combox_product.clear()
        self.ui.combox_product.addItems(products)
        AppMainLogger.debug("addItems in Products: {}".format(str(products)))
