# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal


class CustomSignals(QObject):
    """
    定制的信号类, 用于传递相关信息
    """
    # 将用户指定的数据传递给待分析模块, 用于分析什么文件需要去读
    user_want_data = Signal(dict)

    # 实际需要处理的数据, 里面包含需要处理的各个参数
    need_want_data = Signal(dict)

    # 传递单元格内容的信息
    select_cell_data = Signal(str)

    # 传递进度百分比信号
    import_process = Signal(int)

    # 传递打开帮助文件的信号
    open_help_docs = Signal(str)

# 实例化定制的信号类
allSignals = CustomSignals()
