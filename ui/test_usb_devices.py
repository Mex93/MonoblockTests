# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_usb_devices.ui'
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

class Ui_TestUSBDevicesWindow(object):
    def setupUi(self, TestUSBDevicesWindow):
        if not TestUSBDevicesWindow.objectName():
            TestUSBDevicesWindow.setObjectName(u"TestUSBDevicesWindow")
        TestUSBDevicesWindow.resize(891, 583)
        icon = QIcon()
        icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        TestUSBDevicesWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(TestUSBDevicesWindow)
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

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_fail = QPushButton(self.groupBox)
        self.pushButton_fail.setObjectName(u"pushButton_fail")
        self.pushButton_fail.setFont(font1)
        self.pushButton_fail.setStyleSheet(u"color: red;\n"
"padding: 20%;")

        self.horizontalLayout.addWidget(self.pushButton_fail)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

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

        TestUSBDevicesWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TestUSBDevicesWindow)

        QMetaObject.connectSlotsByName(TestUSBDevicesWindow)
    # setupUi

    def retranslateUi(self, TestUSBDevicesWindow):
        TestUSBDevicesWindow.setWindowTitle(QCoreApplication.translate("TestUSBDevicesWindow", u"Test_USBDevices", None))
        self.groupBox.setTitle(QCoreApplication.translate("TestUSBDevicesWindow", u"\u0422\u0435\u0441\u0442 USB \u0440\u0430\u0437\u044a\u0451\u043c\u043e\u0432:", None))
        self.pushButton_success.setText(QCoreApplication.translate("TestUSBDevicesWindow", u"\u0423\u0441\u043f\u0435\u0445", None))
        self.pushButton_fail.setText(QCoreApplication.translate("TestUSBDevicesWindow", u"\u041e\u0448\u0438\u0431\u043a\u0430", None))
        self.pushButton_all_test_break.setText(QCoreApplication.translate("TestUSBDevicesWindow", u"\u041f\u0440\u0435\u0440\u0432\u0430\u0442\u044c \u0442\u0435\u0441\u0442\u044b", None))
    # retranslateUi

