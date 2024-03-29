# -*- coding: utf-8 -*-

import os
import markdown2
from PySide6.QtWidgets import QWidget, QFileSystemModel
from PySide6.QtCore import QDir
from module.gui.LogHelp_ui import Ui_Form
from module.tools.AppSettings import ReadConfig

class LogAnalysisHelp(QWidget):
    """
    LogAnalysis Help Documents for MarkDown
    """
    def __init__(self):
        # 继承父类
        super().__init__()
        # 初始化 GUI
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 调整标题
        self.setWindowTitle("Help Documents")
        # 调整左边目录树
        dir_model = QFileSystemModel()
        dir_model.setRootPath(os.path.join(QDir.currentPath(), "./help/mddoc"))
        # 调整右边内容框
        self.slot_btn_home()
        # 过滤指定文件
        dir_model.setNameFilterDisables(False)
        dir_model.setNameFilters(["*.md"])
        # 加载文件模型
        self.ui.dir_view.setModel(dir_model)
        self.ui.dir_view.setRootIndex(dir_model.index(os.path.join(QDir.currentPath(), "./help/mddoc")))
        self.ui.dir_view.setColumnHidden(1, True)
        self.ui.dir_view.setColumnHidden(2, True)
        self.ui.dir_view.setColumnHidden(3, True)
        self.ui.dir_view.setHeaderHidden(True)
        # 连接槽函数
        dir_model.directoryLoaded.connect(self.ui.dir_view.expandAll)
        # -> 需要先等待 QFileSystemModel 加载完毕后, 才能执行 QTreeView.expandAll 方法, 否则会无效
        self.ui.dir_view.clicked.connect(self.slot_select_dir_view)
        self.ui.btn_back.clicked.connect(self.slot_btn_back)
        self.ui.btn_home.clicked.connect(self.slot_btn_home)

    def slot_select_dir_view(self, model_index):
        """
        槽函数: 根据选择的内容来决定生成的内容
        """
        path = self.ui.dir_view.selectionModel().model().filePath(model_index)
        # 如果是文件, 则进行渲染 MarkDown 格式的内容
        # https://sebastianraschka.com/Articles/2014_markdown_syntax_color.html
        # https://github.com/trentm/python-markdown2/wiki/fenced-code-blocks
        # https://github.com/richleland/pygments-css

        if os.path.isdir(path):
            # 如果点击的路径是文件夹, 则寻找当前文件夹下的 description.txt 来进行渲染
            filepath = os.path.join(path, "description.txt")
        else:
            # 如果是文件, 则直接渲染该文件
            filepath = path

        # 加载文件和模板进行渲染
        md_txt = markdown2.markdown_path(filepath, encoding="utf-8", extras=["fenced-code-blocks"])
        md_txt = md_txt.replace('class="codehilite"', 'class="highlight"')
        with open("./help/html/km_template.html") as f:
            html = f.read()
        with open(ReadConfig.get_help_css(), encoding="utf-8") as f:
            css = f.read()
        html = html.replace("{{km_content}}", md_txt).replace("{{css_content}}", css)
        self.ui.mdview.setHtml(html)

    def slot_btn_back(self):
        """
        槽函数: 返回上一个 History URL
        """
        self.ui.mdview.back()

    def slot_btn_home(self):
        """
        槽函数: 返回帮助文档首页
        """
        filepath = "./help/mddoc/description.txt"
        md_txt = markdown2.markdown_path(filepath, encoding="utf-8", extras=["fenced-code-blocks"])
        md_txt = md_txt.replace('class="codehilite"', 'class="highlight"')
        with open("./help/html/km_template.html") as f:
            html = f.read()
        with open(ReadConfig.get_help_css(), encoding="utf-8") as f:
            css = f.read()
        html = html.replace("{{km_content}}", md_txt).replace("{{css_content}}", css)
        self.ui.mdview.setHtml(html)