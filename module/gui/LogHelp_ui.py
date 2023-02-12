# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LogHelp.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSplitter,
    QTabWidget, QTextBrowser, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(840, 743)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.tabLeft = QTabWidget(self.splitter)
        self.tabLeft.setObjectName(u"tabLeft")
        self.tab_dir = QWidget()
        self.tab_dir.setObjectName(u"tab_dir")
        self.tabLeft.addTab(self.tab_dir, "")
        self.splitter.addWidget(self.tabLeft)
        self.mdview = QTextBrowser(self.splitter)
        self.mdview.setObjectName(u"mdview")
        self.splitter.addWidget(self.mdview)

        self.horizontalLayout.addWidget(self.splitter)


        self.retranslateUi(Form)

        self.tabLeft.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabLeft.setTabText(self.tabLeft.indexOf(self.tab_dir), QCoreApplication.translate("Form", u"Directory", None))
    # retranslateUi

