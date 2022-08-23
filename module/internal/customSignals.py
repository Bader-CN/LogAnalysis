# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal


class CustomSignals(QObject):
    send_want_data = Signal(dict)


allSignals = CustomSignals()
