# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SelectCont.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 401)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lab_search = QLabel(Form)
        self.lab_search.setObjectName(u"lab_search")
        font = QFont()
        font.setFamilies([u"Consolas"])
        self.lab_search.setFont(font)
        self.lab_search.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lab_search, 0, 0, 1, 1)

        self.line_search = QLineEdit(Form)
        self.line_search.setObjectName(u"line_search")
        self.line_search.setFont(font)

        self.gridLayout.addWidget(self.line_search, 0, 1, 1, 1)

        self.cell_content = QTextEdit(Form)
        self.cell_content.setObjectName(u"cell_content")
        self.cell_content.setFont(font)

        self.gridLayout.addWidget(self.cell_content, 1, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lab_search.setText(QCoreApplication.translate("Form", u"Search Content", None))
    # retranslateUi

