# -*- coding: utf-8 -*-

from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PySide6.QtCore import Qt, QRegularExpression

class TextHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)

        # 设置 keyword 高亮的字体格式
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(Qt.red)
        self.keyword_format.setBackground(Qt.yellow)
        self.keyword_format.setFontWeight(QFont.Bold)

        self.keyword = kwargs.get("keyword")

    def highlightBlock(self, text):
        """
        设置高亮的实际方法
        :param text:
        :return:
        """
        expression = QRegularExpression(self.keyword)
        index = expression.globalMatch(text)
        while index.hasNext():
            match = index.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)