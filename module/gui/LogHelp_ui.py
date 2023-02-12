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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QSizePolicy,
    QSplitter, QTabWidget, QTextBrowser, QTreeView,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(853, 743)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.tabLeft = QTabWidget(self.splitter)
        self.tabLeft.setObjectName(u"tabLeft")
        self.tabLeft.setMinimumSize(QSize(200, 0))
        self.tabLeft.setMaximumSize(QSize(300, 16777215))
        self.tab_dir = QWidget()
        self.tab_dir.setObjectName(u"tab_dir")
        self.verticalLayout_3 = QVBoxLayout(self.tab_dir)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.dir_view = QTreeView(self.tab_dir)
        self.dir_view.setObjectName(u"dir_view")
        self.dir_view.setMinimumSize(QSize(0, 0))
        self.dir_view.setMaximumSize(QSize(400, 16777215))
        self.dir_view.header().setVisible(True)

        self.verticalLayout_3.addWidget(self.dir_view)

        self.tabLeft.addTab(self.tab_dir, "")
        self.splitter.addWidget(self.tabLeft)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mdview = QTextBrowser(self.verticalLayoutWidget)
        self.mdview.setObjectName(u"mdview")
        self.mdview.setMinimumSize(QSize(400, 0))

        self.verticalLayout.addWidget(self.mdview)

        self.splitter.addWidget(self.verticalLayoutWidget)

        self.horizontalLayout.addWidget(self.splitter)


        self.retranslateUi(Form)

        self.tabLeft.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabLeft.setTabText(self.tabLeft.indexOf(self.tab_dir), QCoreApplication.translate("Form", u"Directory", None))
    # retranslateUi

