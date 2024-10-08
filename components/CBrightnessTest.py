from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from os.path import isfile as file_isfile

from enuuuums import BRIGHTNESS_PARAMS, TEST_TYPE
from ui.test_brightness import Ui_TestBrightnessWindow


class CBrightnessTest:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: BRIGHTNESS_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: BRIGHTNESS_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})


class CBrightnessTestWindow(QMainWindow):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestBrightnessWindow()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        # self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_BRIGHTNESS))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_BRIGHTNESS))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_BRIGHTNESS))

        self.setWindowTitle(f'Меню теста')

    def window_show(self) -> bool:
        image_path = CBrightnessTest.get_test_stats(BRIGHTNESS_PARAMS.FILE_PATCH)
        if image_path and isinstance(image_path, str):
            if image_path.find("content/") != -1:
                print(image_path)
                if file_isfile(image_path):
                    pixmap = QPixmap(image_path)
                    color = pixmap.toImage().pixelColor(pixmap.width() // 2, pixmap.height() // 2)
                    self.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});")

                    self.show()
                    return True
        return False

    def closeEvent(self, e):

        e.accept()
