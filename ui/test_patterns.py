# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_patterns.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import ui.res_rc

class Ui_TestPatternsWindow(object):
    def setupUi(self, TestPatternsWindow):
        if not TestPatternsWindow.objectName():
            TestPatternsWindow.setObjectName(u"TestPatternsWindow")
        TestPatternsWindow.resize(1496, 785)
        icon = QIcon()
        icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        TestPatternsWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(TestPatternsWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_btns = QFrame(self.centralwidget)
        self.frame_btns.setObjectName(u"frame_btns")
        self.frame_btns.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_btns.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_btns)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_success = QPushButton(self.frame_btns)
        self.pushButton_success.setObjectName(u"pushButton_success")
        font = QFont()
        font.setPointSize(50)
        self.pushButton_success.setFont(font)
        self.pushButton_success.setStyleSheet(u"color: green;\n"
"padding: 20%;\n"
"background: white;")

        self.horizontalLayout.addWidget(self.pushButton_success)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_fail = QPushButton(self.frame_btns)
        self.pushButton_fail.setObjectName(u"pushButton_fail")
        self.pushButton_fail.setFont(font)
        self.pushButton_fail.setStyleSheet(u"color: red;\n"
"padding: 20%;\n"
"background: white;")

        self.horizontalLayout.addWidget(self.pushButton_fail)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.pushButton_relaunch = QPushButton(self.frame_btns)
        self.pushButton_relaunch.setObjectName(u"pushButton_relaunch")
        self.pushButton_relaunch.setFont(font)
        self.pushButton_relaunch.setStyleSheet(u"color: red;\n"
"padding: 20%;\n"
"background: white;")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRestore))
        self.pushButton_relaunch.setIcon(icon1)
        self.pushButton_relaunch.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.pushButton_relaunch)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.pushButton_all_test_break = QPushButton(self.frame_btns)
        self.pushButton_all_test_break.setObjectName(u"pushButton_all_test_break")
        font1 = QFont()
        font1.setPointSize(20)
        self.pushButton_all_test_break.setFont(font1)
        self.pushButton_all_test_break.setStyleSheet(u"background: yellow")

        self.horizontalLayout_4.addWidget(self.pushButton_all_test_break)


        self.horizontalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addWidget(self.frame_btns)

        TestPatternsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TestPatternsWindow)

        QMetaObject.connectSlotsByName(TestPatternsWindow)
    # setupUi

    def retranslateUi(self, TestPatternsWindow):
        TestPatternsWindow.setWindowTitle(QCoreApplication.translate("TestPatternsWindow", u"Test_Patterns", None))
        self.pushButton_success.setText(QCoreApplication.translate("TestPatternsWindow", u"\u0423\u0441\u043f\u0435\u0445", None))
        self.pushButton_fail.setText(QCoreApplication.translate("TestPatternsWindow", u"\u041e\u0448\u0438\u0431\u043a\u0430", None))
        self.pushButton_relaunch.setText("")
        self.pushButton_all_test_break.setText(QCoreApplication.translate("TestPatternsWindow", u"\u041f\u0440\u0435\u0440\u0432\u0430\u0442\u044c \u0442\u0435\u0441\u0442\u044b", None))
    # retranslateUi

