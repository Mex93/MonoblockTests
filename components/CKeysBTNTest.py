from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QTimer

from PySide6.QtGui import QImage, QPixmap

from enuuuums import KEYSBUTTOMS_PARAMS, TEST_TYPE
from ui.test_keys import Ui_TestKeysWindow


class CKeyTest:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: KEYSBUTTOMS_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: KEYSBUTTOMS_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})


class CKeyTestWindow(QMainWindow):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestKeysWindow()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_HARDWARE_BTN))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_HARDWARE_BTN))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_HARDWARE_BTN))

        self.setWindowTitle(f'Меню теста')

    def window_show(self) -> bool:

        self.show()
        return True

    def closeEvent(self, e):
        # Освобождаем камеру при закрытии окна

        e.accept()
