# -*- coding: utf-8 -*-

################################################
# 参考代码：https://xbuba.com/questions/52765697
################################################

from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PySide6.QtCore import Qt, QRegularExpression

class SQLHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置 keyword 高亮的字体格式
        sql_keyword_format = QTextCharFormat()
        sql_keyword_format.setForeground(Qt.blue)
        sql_keyword_format.setFontWeight(QFont.Bold)
        # 设置 comment 高亮的字体格式
        sql_comment_format = QTextCharFormat()
        sql_comment_format.setForeground(Qt.darkGreen)
        sql_comment_format.setFontWeight(QFont.Bold)
        # 需要高亮的关键字
        sql_keywords = [
            # 基本 SQL 语句
            'SELECT', 'select ', 'FROM', 'from ',
            # SQL 子句
            'WHERE ', 'where ', 'ORDER BY ', 'order by ', 'GROUP BY ', 'group by ',
            # SQL 操作符/运算符
            ' AND ', ' and ', ' OR ', ' or ',
            ' LIKE ', ' like ', ' NOT LIKE ', ' not like ',
            ' GLOB ', ' glob ', ' NOT GLOB ', ' not glob ',
            ' REGEXP ', ' regexp ',
            ' JOIN ', ' join ',
            'INNER JOIN ', 'inner join ',
            'LEFT JOIN ', 'left join ',
            'RIGHT JOIN ', 'right join ',
            'FULL JOIN ', 'full join ',
            ' UNION', ' union', ' UNION ALL', ' union all',
            'DISTINCT ', 'distinct ',
            # SQL 常用函数
            # 参考链接：https://www.runoob.com/sqlite/sqlite-functions.html
            'SUM\(.*?\)', 'sum\(.*?\)',
            'TOTAL\(.*?\)', 'total\(.*?\)',
            'COUNT\(.*?\)', 'count\(.*?\)',
            'MAX\(.*?\)', 'max\(.*?\)',
            'MIN\(.*?\)', 'min\(.*?\)',
            'AVG\(.*?\)', 'avg\(.*?\)',
            'ABS\(.*?\)', 'abs\(.*?\)',
            'RANDOM\(.*?\)', 'random\(.*?\)',
            'UPPER\(.*?\)' ,'upper\(.*?\)',
            'LOWER\(.*?\)' ,'lower\(.*?\)',
            'LENGTH\(.*?\)', 'length\(.*?\)',
        ]
        # 根据前两个来生成高亮规则
        self.highlightRules = [(QRegularExpression(pattern), sql_keyword_format) for pattern in sql_keywords]
        # 追加 comment 规则
        self.highlightRules.append((QRegularExpression('--.*'), sql_comment_format))

    def highlightBlock(self, text):
        # keyword 高亮, 参考链接: https://doc.qt.io/qtforpython/PySide6/QtGui/QSyntaxHighlighter.html
            for pattern, _format in self.highlightRules:
                expression = QRegularExpression(pattern)
                index = expression.globalMatch(text)
                while index.hasNext():
                    match = index.next()
                    self.setFormat(match.capturedStart(), match.capturedLength(), _format)