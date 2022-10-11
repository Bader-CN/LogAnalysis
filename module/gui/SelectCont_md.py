# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from module.gui.SelectCont_ui import Ui_Form

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

    def showContent(self, content):
        """
        显示文本框
        :param content: 单元格里的字符串数据
        """
        self.ui.cell_content.setPlainText(content)
        self.show()