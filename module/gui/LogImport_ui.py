# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LogImport.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(600, 400))
        Form.setMaximumSize(QSize(600, 400))
        self.horizontalLayoutWidget = QWidget(Form)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 581, 26))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_abspath = QLabel(self.horizontalLayoutWidget)
        self.label_abspath.setObjectName(u"label_abspath")
        self.label_abspath.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_abspath)

        self.lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.btn_select_file_or_path = QPushButton(self.horizontalLayoutWidget)
        self.btn_select_file_or_path.setObjectName(u"btn_select_file_or_path")

        self.horizontalLayout.addWidget(self.btn_select_file_or_path)

        self.tree_filedir = QTreeWidget(Form)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_filedir.setHeaderItem(__qtreewidgetitem)
        self.tree_filedir.setObjectName(u"tree_filedir")
        self.tree_filedir.setGeometry(QRect(10, 40, 221, 351))
        self.formLayoutWidget = QWidget(Form)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(240, 40, 351, 311))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.usernote = QTextEdit(self.formLayoutWidget)
        self.usernote.setObjectName(u"usernote")
        self.usernote.setLineWidth(0)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.usernote)

        self.label_type = QLabel(self.formLayoutWidget)
        self.label_type.setObjectName(u"label_type")
        self.label_type.setMinimumSize(QSize(100, 0))
        self.label_type.setLineWidth(2)
        self.label_type.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_type)

        self.combox_type = QComboBox(self.formLayoutWidget)
        self.combox_type.setObjectName(u"combox_type")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.combox_type)

        self.label_company = QLabel(self.formLayoutWidget)
        self.label_company.setObjectName(u"label_company")
        self.label_company.setMinimumSize(QSize(100, 0))
        self.label_company.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_company)

        self.combox_company = QComboBox(self.formLayoutWidget)
        self.combox_company.setObjectName(u"combox_company")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.combox_company)

        self.label_product_line = QLabel(self.formLayoutWidget)
        self.label_product_line.setObjectName(u"label_product_line")
        self.label_product_line.setMinimumSize(QSize(100, 0))
        self.label_product_line.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_product_line)

        self.combox_product_line = QComboBox(self.formLayoutWidget)
        self.combox_product_line.setObjectName(u"combox_product_line")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.combox_product_line)

        self.label_product = QLabel(self.formLayoutWidget)
        self.label_product.setObjectName(u"label_product")
        self.label_product.setMinimumSize(QSize(100, 0))
        self.label_product.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_product)

        self.combox_product = QComboBox(self.formLayoutWidget)
        self.combox_product.setObjectName(u"combox_product")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.combox_product)

        self.label_num_process = QLabel(self.formLayoutWidget)
        self.label_num_process.setObjectName(u"label_num_process")
        self.label_num_process.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_num_process)

        self.comboBox = QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox)

        self.btn_cancel = QPushButton(Form)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(240, 360, 171, 31))
        self.btn_import = QPushButton(Form)
        self.btn_import.setObjectName(u"btn_import")
        self.btn_import.setGeometry(QRect(420, 360, 171, 31))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_abspath.setText(QCoreApplication.translate("Form", u"Path", None))
        self.btn_select_file_or_path.setText(QCoreApplication.translate("Form", u"Select", None))
        self.label_type.setText(QCoreApplication.translate("Form", u"Path Type", None))
        self.label_company.setText(QCoreApplication.translate("Form", u"Company", None))
        self.label_product_line.setText(QCoreApplication.translate("Form", u"Product Line", None))
        self.label_product.setText(QCoreApplication.translate("Form", u"Product Name", None))
        self.label_num_process.setText(QCoreApplication.translate("Form", u"Num of Processes", None))
        self.btn_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.btn_import.setText(QCoreApplication.translate("Form", u"Import", None))
    # retranslateUi

