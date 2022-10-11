# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from module.gui.SelectCont_ui import Ui_Form
from module.tools.AppSettings import ReadConfig
from module.tools.AppDebug import AppMainLogger
from module.tools.TextHLight import TextHighLighter

class CellContUI(QWidget):
    """
    LogAnalysis Select Content GUI
    """
    def __init__(self):
        # 继承父类
        super().__init__()
        # 初始化 GUI
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 调整界面
        self.setWindowTitle("Cell Content")
        self.set_language_by_cell()
        # 连接信号
        self.ui.line_search.textChanged.connect(self.slot_search_content)

    def showContent(self, content):
        """
        显示文本框
        :param content: 单元格里的字符串数据
        """
        self.ui.cell_content.setPlainText(content)
        self.show()

    def set_language_by_cell(self):
        """
        根据配置文件来显示软件语言
        :return:
        """
        if ReadConfig.get_language() == "zh_CN":
            AppMainLogger.info("CellGUI Language setting to zh_CN")
            self.set_zh_CN()

    def set_zh_CN(self):
        from module.language.i18n_zh_CN import Language_zh_CN
        self.ui.lab_search.setText(Language_zh_CN.get("Search Content"))

    def slot_search_content(self):
        """
        搜索框内容发生变化时触发
        :return:
        """
        keyword = self.ui.line_search.text()
        # 设置高亮
        TextHighLighter(self.ui.cell_content, keyword=keyword)
