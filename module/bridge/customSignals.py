# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal


class CustomSignals(QObject):
    """
    定制的信号类, 用于传递相关信息
    """
    # 将用户指定的数据传递给待分析模块, 用于分析什么文件需要去读
    user_want_data = Signal(dict)

# 实例化定制的信号类
allSignals = CustomSignals()
