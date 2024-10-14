from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon

from enuuuums import KEYSBUTTOMS_PARAMS, TEST_TYPE, KEY_PRESSED_TYPE
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

        KeyPressed(KEY_PRESSED_TYPE.KEY_VOL_PLUS, self.ui.pushButton_volplus)
        KeyPressed(KEY_PRESSED_TYPE.KEY_VOL_MINUS, self.ui.pushButton_volminus)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_HARDWARE_BTN))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_HARDWARE_BTN))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_HARDWARE_BTN))

        self.setWindowTitle(f'Меню теста')

    def keyPressEvent(self, event):
        key_type = KEY_PRESSED_TYPE.NONE
        if event.key() == Qt.Key_VolumeUp:
            key_type = KEY_PRESSED_TYPE.KEY_VOL_PLUS
        elif event.key() == Qt.Key_VolumeDown:
            key_type = KEY_PRESSED_TYPE.KEY_VOL_MINUS
        else:
            super().keyPressEvent(event)

        if key_type != KEY_PRESSED_TYPE.NONE:
            key: KeyPressed = KeyPressed.get_key_from_type(key_type)
            if key:
                key.minus_pressed_count()
                if KeyPressed.is_key_successful_pressed():
                    self.__main_window.on_test_phb_success(TEST_TYPE.TEST_HARDWARE_BTN)

    def window_show(self) -> str:
        KeyPressed.set_keys_start()
        self.show()
        return "True"

    def closeEvent(self, e):

        self.__main_window.on_call_in_close_test_window(TEST_TYPE.TEST_HARDWARE_BTN)
        e.accept()


class KeyPressed:
    __keys_list = []

    def __init__(self, key_type: KEY_PRESSED_TYPE, key_id: QPushButton):
        self.__key_id = key_id
        self.__pressed_count = 3
        self.__key_type = key_type
        KeyPressed.__keys_list.append(self)

    @classmethod
    def set_keys_start(cls):
        for key in cls.__keys_list:
            key.set_start_pressed_count()

    @classmethod
    def get_key_from_type(cls, key_type: KEY_PRESSED_TYPE):
        for key in cls.__keys_list:
            if key.get_key_type() == key_type:
                return key
        return None

    @classmethod
    def get_key_text(cls, key_type: KEY_PRESSED_TYPE) -> str:
        if key_type == KEY_PRESSED_TYPE.KEY_VOL_PLUS:
            return "VOL+"
        elif key_type == KEY_PRESSED_TYPE.KEY_VOL_MINUS:
            return "VOL-"

    @classmethod
    def is_key_successful_pressed(cls) -> bool:
        keys = list()
        for key in cls.__keys_list:
            if key.__pressed_count == 0:
                keys.append(True)

        if len(keys) == len(cls.__keys_list):
            return True

    def set_current_text_and_icon(self):
        text = self.get_key_text(self.__key_type)
        self.__key_id.setText(f"{text} {self.__pressed_count}")

        if self.__pressed_count == 0:
            self.__key_id.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome)))
        else:
            self.__key_id.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AppointmentNew)))

    def get_key_type(self) -> KEY_PRESSED_TYPE:
        return self.__key_type

    def set_start_pressed_count(self):
        self.__pressed_count = 3

        self.set_current_text_and_icon()

    def minus_pressed_count(self):
        if self.__pressed_count > 0:
            self.__pressed_count -= 1

        self.set_current_text_and_icon()
