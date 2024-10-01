# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_sys_info.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_TestSysInfoWindow(object):
    def setupUi(self, TestSysInfoWindow):
        if not TestSysInfoWindow.objectName():
            TestSysInfoWindow.setObjectName(u"TestSysInfoWindow")
        TestSysInfoWindow.resize(1211, 755)
        self.centralwidget = QWidget(TestSysInfoWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font = QFont()
        font.setPointSize(15)
        self.groupBox_2.setFont(font)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_bios_info = QLabel(self.groupBox_2)
        self.label_bios_info.setObjectName(u"label_bios_info")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_bios_info.sizePolicy().hasHeightForWidth())
        self.label_bios_info.setSizePolicy(sizePolicy)
        self.label_bios_info.setFont(font)

        self.verticalLayout.addWidget(self.label_bios_info)

        self.label_cpu_info = QLabel(self.groupBox_2)
        self.label_cpu_info.setObjectName(u"label_cpu_info")
        sizePolicy.setHeightForWidth(self.label_cpu_info.sizePolicy().hasHeightForWidth())
        self.label_cpu_info.setSizePolicy(sizePolicy)
        self.label_cpu_info.setFont(font)

        self.verticalLayout.addWidget(self.label_cpu_info)

        self.label_ram_info = QLabel(self.groupBox_2)
        self.label_ram_info.setObjectName(u"label_ram_info")
        sizePolicy.setHeightForWidth(self.label_ram_info.sizePolicy().hasHeightForWidth())
        self.label_ram_info.setSizePolicy(sizePolicy)
        self.label_ram_info.setFont(font)

        self.verticalLayout.addWidget(self.label_ram_info)

        self.label_os_info = QLabel(self.groupBox_2)
        self.label_os_info.setObjectName(u"label_os_info")
        sizePolicy.setHeightForWidth(self.label_os_info.sizePolicy().hasHeightForWidth())
        self.label_os_info.setSizePolicy(sizePolicy)
        self.label_os_info.setFont(font)

        self.verticalLayout.addWidget(self.label_os_info)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.pushButton_all_test_break = QPushButton(self.groupBox_2)
        self.pushButton_all_test_break.setObjectName(u"pushButton_all_test_break")
        font1 = QFont()
        font1.setPointSize(20)
        self.pushButton_all_test_break.setFont(font1)
        self.pushButton_all_test_break.setStyleSheet(u"background: yellow")

        self.horizontalLayout_3.addWidget(self.pushButton_all_test_break)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.groupBox_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.textBrowser_lan_port = QTextBrowser(self.groupBox)
        self.textBrowser_lan_port.setObjectName(u"textBrowser_lan_port")

        self.horizontalLayout_2.addWidget(self.textBrowser_lan_port)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_success = QPushButton(self.groupBox_2)
        self.pushButton_success.setObjectName(u"pushButton_success")
        font2 = QFont()
        font2.setPointSize(50)
        self.pushButton_success.setFont(font2)
        self.pushButton_success.setStyleSheet(u"color: green;\n"
"padding: 20%;")

        self.horizontalLayout.addWidget(self.pushButton_success)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_fail = QPushButton(self.groupBox_2)
        self.pushButton_fail.setObjectName(u"pushButton_fail")
        self.pushButton_fail.setFont(font2)
        self.pushButton_fail.setStyleSheet(u"color: red;\n"
"padding: 20%;")

        self.horizontalLayout.addWidget(self.pushButton_fail)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout_4.addWidget(self.groupBox_2)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)

        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.verticalLayout_5.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        TestSysInfoWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(TestSysInfoWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1211, 22))
        TestSysInfoWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(TestSysInfoWindow)
        self.statusbar.setObjectName(u"statusbar")
        TestSysInfoWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TestSysInfoWindow)

        QMetaObject.connectSlotsByName(TestSysInfoWindow)
    # setupUi

    def retranslateUi(self, TestSysInfoWindow):
        TestSysInfoWindow.setWindowTitle(QCoreApplication.translate("TestSysInfoWindow", u"Test_SystemInfo", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("TestSysInfoWindow", u"\u0422\u0435\u0441\u0442 \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u0438 \u043e \u0441\u0438\u0441\u0442\u0435\u043c\u0435:", None))
        self.label_bios_info.setText(QCoreApplication.translate("TestSysInfoWindow", u"BIOS: 4EUEHFG2978HGF429W87UFVU9", None))
        self.label_cpu_info.setText(QCoreApplication.translate("TestSysInfoWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u043e\u0440\u0430: Ryazan", None))
        self.label_ram_info.setText(QCoreApplication.translate("TestSysInfoWindow", u"\u041e\u0417\u0423: 100500 \u0433\u0431", None))
        self.label_os_info.setText(QCoreApplication.translate("TestSysInfoWindow", u"OS:", None))
        self.pushButton_all_test_break.setText(QCoreApplication.translate("TestSysInfoWindow", u"\u041f\u0440\u0435\u0440\u0432\u0430\u0442\u044c \u0442\u0435\u0441\u0442\u044b", None))
        self.groupBox.setTitle(QCoreApplication.translate("TestSysInfoWindow", u"\u0422\u0435\u0441\u0442\u044b:", None))
        self.textBrowser_lan_port.setHtml(QCoreApplication.translate("TestSysInfoWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#ff0000;\">efgege</span></p></body></html>", None))
        self.pushButton_success.setText(QCoreApplication.translate("TestSysInfoWindow", u"\u0423\u0441\u043f\u0435\u0445", None))
        self.pushButton_fail.setText(QCoreApplication.translate("TestSysInfoWindow", u"\u041e\u0448\u0438\u0431\u043a\u0430", None))
    # retranslateUi

