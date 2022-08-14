# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from module.gui.LogImport_ui import Ui_Form
from module.tools.AppSettings import ReadConfig
from module.tools.AppDebug import AppMainLogger


class LogAnalysisImport(QWidget):
    """
    LogAnalysis Import GUI
    """
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
