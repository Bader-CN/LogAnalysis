# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from module.gui.LogImport_ui import Ui_Form


class LogAnalysisImport(QWidget):
    """
    LogAnalysis Import GUI
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
