# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_speaker_audio.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QVBoxLayout, QWidget)

class Ui_TestAudioWindow(object):
    def setupUi(self, TestAudioWindow):
        if not TestAudioWindow.objectName():
            TestAudioWindow.setObjectName(u"TestAudioWindow")
        TestAudioWindow.resize(1035, 388)
        font = QFont()
        font.setPointSize(15)
        TestAudioWindow.setFont(font)
        self.centralwidget = QWidget(TestAudioWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_right = QPushButton(self.groupBox)
        self.pushButton_right.setObjectName(u"pushButton_right")
        self.pushButton_right.setFont(font)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeHigh))
        self.pushButton_right.setIcon(icon)
        self.pushButton_right.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.pushButton_right, 0, 2, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(20)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.pushButton_left = QPushButton(self.groupBox)
        self.pushButton_left.setObjectName(u"pushButton_left")
        self.pushButton_left.setFont(font)
        self.pushButton_left.setIcon(icon)
        self.pushButton_left.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.pushButton_left, 0, 1, 1, 1)

        self.pushButton_record = QPushButton(self.groupBox)
        self.pushButton_record.setObjectName(u"pushButton_record")
        self.pushButton_record.setFont(font)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaRecord))
        self.pushButton_record.setIcon(icon1)
        self.pushButton_record.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.pushButton_record, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_9)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.horizontalSlider_volume = QSlider(self.groupBox)
        self.horizontalSlider_volume.setObjectName(u"horizontalSlider_volume")
        self.horizontalSlider_volume.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.horizontalSlider_volume)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_success = QPushButton(self.groupBox)
        self.pushButton_success.setObjectName(u"pushButton_success")
        font2 = QFont()
        font2.setPointSize(50)
        self.pushButton_success.setFont(font2)
        self.pushButton_success.setStyleSheet(u"color: green;\n"
"padding: 20%;")

        self.horizontalLayout.addWidget(self.pushButton_success)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_fail = QPushButton(self.groupBox)
        self.pushButton_fail.setObjectName(u"pushButton_fail")
        self.pushButton_fail.setFont(font2)
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
        self.pushButton_all_test_break.setFont(font1)
        self.pushButton_all_test_break.setStyleSheet(u"background: yellow")

        self.horizontalLayout_4.addWidget(self.pushButton_all_test_break)


        self.horizontalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addWidget(self.groupBox)

        TestAudioWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TestAudioWindow)

        QMetaObject.connectSlotsByName(TestAudioWindow)
    # setupUi

    def retranslateUi(self, TestAudioWindow):
        TestAudioWindow.setWindowTitle(QCoreApplication.translate("TestAudioWindow", u"Test_Audio", None))
        self.groupBox.setTitle(QCoreApplication.translate("TestAudioWindow", u"\u0422\u0435\u0441\u0442 \u0437\u0432\u0443\u043a\u0430 \u0414\u0438\u043d\u0430\u043c\u0438\u043a\u0438:", None))
        self.pushButton_right.setText(QCoreApplication.translate("TestAudioWindow", u"\u041f\u0440\u0430\u0432\u044b\u0439 \u043a\u0430\u043d\u0430\u043b", None))
        self.label.setText(QCoreApplication.translate("TestAudioWindow", u"\u0417\u0432\u0443\u043a:", None))
        self.pushButton_left.setText(QCoreApplication.translate("TestAudioWindow", u"\u041b\u0435\u0432\u044b\u0439 \u043a\u0430\u043d\u0430\u043b", None))
        self.pushButton_record.setText(QCoreApplication.translate("TestAudioWindow", u"\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044c", None))
        self.label_2.setText(QCoreApplication.translate("TestAudioWindow", u"\u0417\u0430\u043f\u0438\u0441\u044c:", None))
        self.label_3.setText(QCoreApplication.translate("TestAudioWindow", u"-", None))
        self.label_4.setText(QCoreApplication.translate("TestAudioWindow", u"+", None))
        self.pushButton_success.setText(QCoreApplication.translate("TestAudioWindow", u"\u0423\u0441\u043f\u0435\u0445", None))
        self.pushButton_fail.setText(QCoreApplication.translate("TestAudioWindow", u"\u041e\u0448\u0438\u0431\u043a\u0430", None))
        self.pushButton_all_test_break.setText(QCoreApplication.translate("TestAudioWindow", u"\u041f\u0440\u0435\u0440\u0432\u0430\u0442\u044c \u0442\u0435\u0441\u0442\u044b", None))
    # retranslateUi

