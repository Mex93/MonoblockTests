from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
import os
from PySide6.QtGui import QPixmap

from enuuuums import PATTERNS_TEST_PARAMS, TEST_TYPE
from ui.test_patterns import Ui_TestPatternsWindow


class CPatternsTest:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: PATTERNS_TEST_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: PATTERNS_TEST_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})


class CPatternsTestWindow(QMainWindow):
    MAX_PATTERNS_INDEX = 0

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestPatternsWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.buttons_show = False
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_PATTERNS))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_PATTERNS))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_PATTERNS))

        self.ui.pushButton_relaunch.clicked.connect(
            self.window_show)

        self.setWindowTitle(f'Меню теста')

        # получение списка

        self.patterns_list = list()
        self.patterns_index = 0

    def window_show(self) -> bool:
        self.patterns_list.clear()
        path = "content/patterns"

        # чтение записей
        with os.scandir(path) as listOfEntries:
            for entry in listOfEntries:
                # печать всех записей, являющихся файлами
                if entry.is_file():
                    if entry.name.find(".jpg") == -1:
                        continue

                    self.patterns_list.append(path + "/" + entry.name)

        if len(self.patterns_list):
            self.MAX_PATTERNS_INDEX = len(self.patterns_list)
            self.patterns_index = -1
            self.ui.frame_btns.setHidden(True)
            self.buttons_show = False
            self.set_image()
            self.showFullScreen()
            return True

        return False

    def set_background_color_from_image(self, image_path):
        pixmap = QPixmap(image_path)
        color = pixmap.toImage().pixelColor(pixmap.width() // 2, pixmap.height() // 2)
        self.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});")

    def set_image(self):
        self.patterns_index += 1
        if self.patterns_index == self.MAX_PATTERNS_INDEX:
            self.patterns_index = 0
            self.buttons_show = True
            self.ui.frame_btns.setHidden(False)
        else:
            if self.buttons_show:
                self.buttons_show = False
                self.ui.frame_btns.setHidden(True)

        self.set_background_color_from_image(self.patterns_list[self.patterns_index])

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:  # Проверяем, что нажата левая кнопка мыши
            self.set_image()

    def closeEvent(self, e):

        e.accept()
