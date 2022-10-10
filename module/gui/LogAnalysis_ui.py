# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LogAnalysis.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateTimeEdit, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTabWidget, QTextEdit, QToolBar, QTreeView,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(965, 600)
        MainWindow.setMinimumSize(QSize(965, 600))
        self.actionDeleteDB = QAction(MainWindow)
        self.actionDeleteDB.setObjectName(u"actionDeleteDB")
        self.action2 = QAction(MainWindow)
        self.action2.setObjectName(u"action2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter_by_vrt = QSplitter(self.centralwidget)
        self.splitter_by_vrt.setObjectName(u"splitter_by_vrt")
        self.splitter_by_vrt.setOrientation(Qt.Horizontal)
        self.widget_left = QWidget(self.splitter_by_vrt)
        self.widget_left.setObjectName(u"widget_left")
        self.widget_left.setMinimumSize(QSize(200, 0))
        self.widget_left.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget_left)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabLeft = QTabWidget(self.widget_left)
        self.tabLeft.setObjectName(u"tabLeft")
        font = QFont()
        font.setFamilies([u"Consolas"])
        self.tabLeft.setFont(font)
        self.tab_database = QWidget()
        self.tab_database.setObjectName(u"tab_database")
        self.verticalLayout_3 = QVBoxLayout(self.tab_database)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.treeWidget_db = QTreeWidget(self.tab_database)
        self.treeWidget_db.setObjectName(u"treeWidget_db")
        self.treeWidget_db.setFont(font)

        self.verticalLayout_3.addWidget(self.treeWidget_db)

        self.tabLeft.addTab(self.tab_database, "")
        self.tab_template = QWidget()
        self.tab_template.setObjectName(u"tab_template")
        self.verticalLayout_4 = QVBoxLayout(self.tab_template)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.treeView_template = QTreeView(self.tab_template)
        self.treeView_template.setObjectName(u"treeView_template")

        self.verticalLayout_4.addWidget(self.treeView_template)

        self.tabLeft.addTab(self.tab_template, "")

        self.verticalLayout_2.addWidget(self.tabLeft)

        self.splitter_by_vrt.addWidget(self.widget_left)
        self.widget_right = QWidget(self.splitter_by_vrt)
        self.widget_right.setObjectName(u"widget_right")
        self.verticalLayout = QVBoxLayout(self.widget_right)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_hor1 = QHBoxLayout()
        self.layout_hor1.setObjectName(u"layout_hor1")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_hor1.addItem(self.horizontalSpacer)

        self.label_start_time = QLabel(self.widget_right)
        self.label_start_time.setObjectName(u"label_start_time")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_start_time.sizePolicy().hasHeightForWidth())
        self.label_start_time.setSizePolicy(sizePolicy)
        self.label_start_time.setAlignment(Qt.AlignCenter)

        self.layout_hor1.addWidget(self.label_start_time)

        self.date_start_time = QDateTimeEdit(self.widget_right)
        self.date_start_time.setObjectName(u"date_start_time")
        sizePolicy.setHeightForWidth(self.date_start_time.sizePolicy().hasHeightForWidth())
        self.date_start_time.setSizePolicy(sizePolicy)
        self.date_start_time.setMinimumSize(QSize(125, 0))
        self.date_start_time.setCalendarPopup(True)

        self.layout_hor1.addWidget(self.date_start_time)

        self.label_end_time = QLabel(self.widget_right)
        self.label_end_time.setObjectName(u"label_end_time")
        sizePolicy.setHeightForWidth(self.label_end_time.sizePolicy().hasHeightForWidth())
        self.label_end_time.setSizePolicy(sizePolicy)
        self.label_end_time.setAlignment(Qt.AlignCenter)

        self.layout_hor1.addWidget(self.label_end_time)

        self.date_end_time = QDateTimeEdit(self.widget_right)
        self.date_end_time.setObjectName(u"date_end_time")
        sizePolicy.setHeightForWidth(self.date_end_time.sizePolicy().hasHeightForWidth())
        self.date_end_time.setSizePolicy(sizePolicy)
        self.date_end_time.setMinimumSize(QSize(125, 0))
        self.date_end_time.setCalendarPopup(True)

        self.layout_hor1.addWidget(self.date_end_time)

        self.btn_new = QPushButton(self.widget_right)
        self.btn_new.setObjectName(u"btn_new")
        sizePolicy.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy)

        self.layout_hor1.addWidget(self.btn_new)

        self.btn_import = QPushButton(self.widget_right)
        self.btn_import.setObjectName(u"btn_import")
        sizePolicy.setHeightForWidth(self.btn_import.sizePolicy().hasHeightForWidth())
        self.btn_import.setSizePolicy(sizePolicy)

        self.layout_hor1.addWidget(self.btn_import)

        self.btn_export = QPushButton(self.widget_right)
        self.btn_export.setObjectName(u"btn_export")
        sizePolicy.setHeightForWidth(self.btn_export.sizePolicy().hasHeightForWidth())
        self.btn_export.setSizePolicy(sizePolicy)

        self.layout_hor1.addWidget(self.btn_export)

        self.btn_help = QPushButton(self.widget_right)
        self.btn_help.setObjectName(u"btn_help")
        sizePolicy.setHeightForWidth(self.btn_help.sizePolicy().hasHeightForWidth())
        self.btn_help.setSizePolicy(sizePolicy)

        self.layout_hor1.addWidget(self.btn_help)


        self.verticalLayout.addLayout(self.layout_hor1)

        self.layout_hor2 = QHBoxLayout()
        self.layout_hor2.setObjectName(u"layout_hor2")
        self.chk_regexp = QCheckBox(self.widget_right)
        self.chk_regexp.setObjectName(u"chk_regexp")
        sizePolicy.setHeightForWidth(self.chk_regexp.sizePolicy().hasHeightForWidth())
        self.chk_regexp.setSizePolicy(sizePolicy)

        self.layout_hor2.addWidget(self.chk_regexp)

        self.line_search = QLineEdit(self.widget_right)
        self.line_search.setObjectName(u"line_search")
        self.line_search.setMinimumSize(QSize(0, 0))
        self.line_search.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_hor2.addWidget(self.line_search)

        self.btn_query = QPushButton(self.widget_right)
        self.btn_query.setObjectName(u"btn_query")
        self.btn_query.setMinimumSize(QSize(0, 0))

        self.layout_hor2.addWidget(self.btn_query)


        self.verticalLayout.addLayout(self.layout_hor2)

        self.splitter_by_hor = QSplitter(self.widget_right)
        self.splitter_by_hor.setObjectName(u"splitter_by_hor")
        self.splitter_by_hor.setOrientation(Qt.Vertical)
        self.tabSQLQuery = QTabWidget(self.splitter_by_hor)
        self.tabSQLQuery.setObjectName(u"tabSQLQuery")
        self.tabSQLQuery.setTabsClosable(True)
        self.tabSQLQuery.setMovable(True)
        self.Query1 = QWidget()
        self.Query1.setObjectName(u"Query1")
        self.verticalLayout_5 = QVBoxLayout(self.Query1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.SQLTextEdit = QTextEdit(self.Query1)
        self.SQLTextEdit.setObjectName(u"SQLTextEdit")
        self.SQLTextEdit.setFont(font)

        self.verticalLayout_5.addWidget(self.SQLTextEdit)

        self.tabSQLQuery.addTab(self.Query1, "")
        self.splitter_by_hor.addWidget(self.tabSQLQuery)
        self.tabSQLResult = QTabWidget(self.splitter_by_hor)
        self.tabSQLResult.setObjectName(u"tabSQLResult")
        self.tabSQLResult.setTabsClosable(True)
        self.tabSQLResult.setMovable(True)
        self.splitter_by_hor.addWidget(self.tabSQLResult)

        self.verticalLayout.addWidget(self.splitter_by_hor)

        self.progressBar = QProgressBar(self.widget_right)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.splitter_by_vrt.addWidget(self.widget_right)

        self.horizontalLayout.addWidget(self.splitter_by_vrt)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 965, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionDeleteDB)

        self.retranslateUi(MainWindow)

        self.tabLeft.setCurrentIndex(0)
        self.tabSQLResult.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionDeleteDB.setText(QCoreApplication.translate("MainWindow", u"Delete DB", None))
        self.action2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        ___qtreewidgetitem = self.treeWidget_db.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"DB List", None));
        self.tabLeft.setTabText(self.tabLeft.indexOf(self.tab_database), QCoreApplication.translate("MainWindow", u"Database", None))
        self.tabLeft.setTabText(self.tabLeft.indexOf(self.tab_template), QCoreApplication.translate("MainWindow", u"Template", None))
        self.label_start_time.setText(QCoreApplication.translate("MainWindow", u"Start Time", None))
        self.label_end_time.setText(QCoreApplication.translate("MainWindow", u"End Time", None))
        self.btn_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.btn_import.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.btn_export.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.btn_help.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.chk_regexp.setText(QCoreApplication.translate("MainWindow", u"Enable Regexp", None))
        self.btn_query.setText(QCoreApplication.translate("MainWindow", u"Query", None))
        self.tabSQLQuery.setTabText(self.tabSQLQuery.indexOf(self.Query1), QCoreApplication.translate("MainWindow", u"Query1", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

