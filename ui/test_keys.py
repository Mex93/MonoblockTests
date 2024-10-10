# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_keys.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import ui.res_rc

class Ui_TestKeysWindow(object):
    def setupUi(self, TestKeysWindow):
        if not TestKeysWindow.objectName():
            TestKeysWindow.setObjectName(u"TestKeysWindow")
        TestKeysWindow.resize(891, 593)
        icon = QIcon()
        icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        TestKeysWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(TestKeysWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setPointSize(15)
        self.groupBox.setFont(font)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_volplus = QPushButton(self.groupBox)
        self.pushButton_volplus.setObjectName(u"pushButton_volplus")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AppointmentNew))
        self.pushButton_volplus.setIcon(icon1)
        self.pushButton_volplus.setIconSize(QSize(40, 40))

        self.horizontalLayout_2.addWidget(self.pushButton_volplus)

        self.pushButton_volminus = QPushButton(self.groupBox)
        self.pushButton_volminus.setObjectName(u"pushButton_volminus")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome))
        self.pushButton_volminus.setIcon(icon2)
        self.pushButton_volminus.setIconSize(QSize(40, 40))

        self.horizontalLayout_2.addWidget(self.pushButton_volminus)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_success = QPushButton(self.groupBox)
        self.pushButton_success.setObjectName(u"pushButton_success")
        font1 = QFont()
        font1.setPointSize(50)
        self.pushButton_success.setFont(font1)
        self.pushButton_success.setStyleSheet(u"color: green;\n"
"padding: 20%;")

        self.horizontalLayout.addWidget(self.pushButton_success)

        self.pushButton_fail = QPushButton(self.groupBox)
        self.pushButton_fail.setObjectName(u"pushButton_fail")
        self.pushButton_fail.setFont(font1)
        self.pushButton_fail.setStyleSheet(u"color: red;\n"
"padding: 20%;")

        self.horizontalLayout.addWidget(self.pushButton_fail)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)

        self.pushButton_all_test_break = QPushButton(self.groupBox)
        self.pushButton_all_test_break.setObjectName(u"pushButton_all_test_break")
        font2 = QFont()
        font2.setPointSize(20)
        self.pushButton_all_test_break.setFont(font2)
        self.pushButton_all_test_break.setStyleSheet(u"background: yellow")

        self.horizontalLayout_4.addWidget(self.pushButton_all_test_break)


        self.horizontalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addWidget(self.groupBox)

        TestKeysWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TestKeysWindow)

        QMetaObject.connectSlotsByName(TestKeysWindow)
    # setupUi

    def retranslateUi(self, TestKeysWindow):
        TestKeysWindow.setWindowTitle(QCoreApplication.translate("TestKeysWindow", u"Test_Keys", None))
        self.groupBox.setTitle(QCoreApplication.translate("TestKeysWindow", u"\u0422\u0435\u0441\u0442 \u043a\u043b\u0430\u0432\u0438\u0448:", None))
        self.pushButton_volplus.setText(QCoreApplication.translate("TestKeysWindow", u"VOL +", None))
        self.pushButton_volminus.setText(QCoreApplication.translate("TestKeysWindow", u"VOL -", None))
        self.pushButton_success.setText(QCoreApplication.translate("TestKeysWindow", u"\u0423\u0441\u043f\u0435\u0445", None))
        self.pushButton_fail.setText(QCoreApplication.translate("TestKeysWindow", u"\u041e\u0448\u0438\u0431\u043a\u0430", None))
        self.pushButton_all_test_break.setText(QCoreApplication.translate("TestKeysWindow", u"\u041f\u0440\u0435\u0440\u0432\u0430\u0442\u044c \u0442\u0435\u0441\u0442\u044b", None))
    # retranslateUi

