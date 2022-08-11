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
        self.ui.label_type.setText(Language_zh_CN.get("Path Type"))
        self.ui.label_company.setText(Language_zh_CN.get("Company"))
        self.ui.label_product_line.setText(Language_zh_CN.get("Product Line"))
        self.ui.label_product.setText(Language_zh_CN.get("Product Name"))
        self.ui.btn_import.setText(Language_zh_CN.get("Import"))
        self.ui.btn_cancel.setText(Language_zh_CN.get("Cancel"))