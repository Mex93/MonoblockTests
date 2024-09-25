# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import ui.res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1177, 384)
        MainWindow.setMinimumSize(QSize(719, 297))
        icon = QIcon()
        icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QSize(30, 30))
        self.action_info = QAction(MainWindow)
        self.action_info.setObjectName(u"action_info")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_monoblock_config_name = QLabel(self.centralwidget)
        self.label_monoblock_config_name.setObjectName(u"label_monoblock_config_name")
        font = QFont()
        font.setPointSize(20)
        self.label_monoblock_config_name.setFont(font)

        self.horizontalLayout.addWidget(self.label_monoblock_config_name)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.comboBox_config_get = QComboBox(self.centralwidget)
        self.comboBox_config_get.addItem("")
        self.comboBox_config_get.setObjectName(u"comboBox_config_get")
        font1 = QFont()
        font1.setPointSize(15)
        self.comboBox_config_get.setFont(font1)

        self.verticalLayout_2.addWidget(self.comboBox_config_get)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font1)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_launchall = QPushButton(self.groupBox_2)
        self.pushButton_launchall.setObjectName(u"pushButton_launchall")
        self.pushButton_launchall.setFont(font1)
        self.pushButton_launchall.setStyleSheet(u"padding:10px")

        self.horizontalLayout_2.addWidget(self.pushButton_launchall)

        self.pushButton_clear = QPushButton(self.groupBox_2)
        self.pushButton_clear.setObjectName(u"pushButton_clear")
        self.pushButton_clear.setFont(font1)
        self.pushButton_clear.setStyleSheet(u"padding:10px")

        self.horizontalLayout_2.addWidget(self.pushButton_clear)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_exit = QPushButton(self.groupBox_2)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"padding:10px")

        self.horizontalLayout_2.addWidget(self.pushButton_exit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addWidget(self.groupBox_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font1)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_btn1 = QPushButton(self.groupBox)
        self.pushButton_btn1.setObjectName(u"pushButton_btn1")

        self.gridLayout.addWidget(self.pushButton_btn1, 0, 0, 1, 1)

        self.pushButton_btn2 = QPushButton(self.groupBox)
        self.pushButton_btn2.setObjectName(u"pushButton_btn2")

        self.gridLayout.addWidget(self.pushButton_btn2, 0, 1, 1, 1)

        self.pushButton_btn3 = QPushButton(self.groupBox)
        self.pushButton_btn3.setObjectName(u"pushButton_btn3")

        self.gridLayout.addWidget(self.pushButton_btn3, 0, 2, 1, 1)

        self.pushButton_btn4 = QPushButton(self.groupBox)
        self.pushButton_btn4.setObjectName(u"pushButton_btn4")

        self.gridLayout.addWidget(self.pushButton_btn4, 1, 0, 1, 1)

        self.pushButton_btn5 = QPushButton(self.groupBox)
        self.pushButton_btn5.setObjectName(u"pushButton_btn5")

        self.gridLayout.addWidget(self.pushButton_btn5, 1, 1, 1, 1)

        self.pushButton_btn6 = QPushButton(self.groupBox)
        self.pushButton_btn6.setObjectName(u"pushButton_btn6")

        self.gridLayout.addWidget(self.pushButton_btn6, 1, 2, 1, 1)

        self.pushButton_btn7 = QPushButton(self.groupBox)
        self.pushButton_btn7.setObjectName(u"pushButton_btn7")

        self.gridLayout.addWidget(self.pushButton_btn7, 2, 0, 1, 1)

        self.pushButton_btn8 = QPushButton(self.groupBox)
        self.pushButton_btn8.setObjectName(u"pushButton_btn8")

        self.gridLayout.addWidget(self.pushButton_btn8, 2, 1, 1, 1)

        self.pushButton_btn9 = QPushButton(self.groupBox)
        self.pushButton_btn9.setObjectName(u"pushButton_btn9")

        self.gridLayout.addWidget(self.pushButton_btn9, 2, 2, 1, 1)

        self.pushButton_btn10 = QPushButton(self.groupBox)
        self.pushButton_btn10.setObjectName(u"pushButton_btn10")

        self.gridLayout.addWidget(self.pushButton_btn10, 3, 0, 1, 1)

        self.pushButton_btn11 = QPushButton(self.groupBox)
        self.pushButton_btn11.setObjectName(u"pushButton_btn11")

        self.gridLayout.addWidget(self.pushButton_btn11, 3, 1, 1, 1)

        self.pushButton_btn12 = QPushButton(self.groupBox)
        self.pushButton_btn12.setObjectName(u"pushButton_btn12")

        self.gridLayout.addWidget(self.pushButton_btn12, 3, 2, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalLayout_5.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1177, 22))
        self.menu_info = QMenu(self.menubar)
        self.menu_info.setObjectName(u"menu_info")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_info.menuAction())
        self.menu_info.addAction(self.action_info)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_info.setText(QCoreApplication.translate("MainWindow", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
        self.label_monoblock_config_name.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0441\u0442 \u043c\u043e\u043d\u043e\u0431\u043b\u043e\u043a\u043e\u0432:", None))
        self.comboBox_config_get.setItemText(0, QCoreApplication.translate("MainWindow", u"TRICOLOR", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0446\u0438\u0438:", None))
        self.pushButton_launchall.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u0432\u0441\u0435", None))
        self.pushButton_clear.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442", None))
        self.pushButton_exit.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0431\u043e\u0440 \u0442\u0435\u0441\u0442\u043e\u0432:", None))
        self.pushButton_btn1.setText(QCoreApplication.translate("MainWindow", u"btn1", None))
        self.pushButton_btn2.setText(QCoreApplication.translate("MainWindow", u"btn2", None))
        self.pushButton_btn3.setText(QCoreApplication.translate("MainWindow", u"btn3", None))
        self.pushButton_btn4.setText(QCoreApplication.translate("MainWindow", u"btn4", None))
        self.pushButton_btn5.setText(QCoreApplication.translate("MainWindow", u"btn5", None))
        self.pushButton_btn6.setText(QCoreApplication.translate("MainWindow", u"btn6", None))
        self.pushButton_btn7.setText(QCoreApplication.translate("MainWindow", u"btn7", None))
        self.pushButton_btn8.setText(QCoreApplication.translate("MainWindow", u"btn8", None))
        self.pushButton_btn9.setText(QCoreApplication.translate("MainWindow", u"btn9", None))
        self.pushButton_btn10.setText(QCoreApplication.translate("MainWindow", u"btn10", None))
        self.pushButton_btn11.setText(QCoreApplication.translate("MainWindow", u"btn11", None))
        self.pushButton_btn12.setText(QCoreApplication.translate("MainWindow", u"btn12", None))
        self.menu_info.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f", None))
    # retranslateUi

