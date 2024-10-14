from PySide6.QtWidgets import QPushButton
from enuuuums import TEST_TYPE


class CButtoms:
    __units = list()

    def __init__(self, btn_id: QPushButton):
        self.__btn_id = btn_id
        self.__btn_test_type = TEST_TYPE.TEST_NONE
        self.__callback_func = None
        self.__units.append(self)

    def set_callback(self, test_type: TEST_TYPE, func):
        if self.__callback_func is None:
            self.__callback_func = func
            self.__btn_test_type = test_type
            self.__btn_id.clicked.connect(lambda: func(test_type))

    def get_test_type(self) -> TEST_TYPE:
        return self.__btn_test_type

    def set_hidden(self, status: bool):
        self.__btn_id.setHidden(status)

    def set_clear_callbacks(self):
        if self.__callback_func is not None:
            self.__btn_id.clicked.disconnect()
            self.__callback_func = None

    def set_name(self, name: str):
        self.__btn_id.setText(name)

    def set_enabled(self, status: bool):
        self.__btn_id.setEnabled(status)

    def set_buttons_default_value(self):
        self.set_name("-")
        self.set_enabled(True)
        self.set_btn_color_default()
        self.set_clear_callbacks()

    def set_btn_color_red(self):
        self.__btn_id.setStyleSheet("color:red;"
                                    "font-size:15pt;")

    def set_btn_color_green(self):
        self.__btn_id.setStyleSheet("color:green;"
                                    "font-size:15pt;")

    def set_btn_color_default(self):
        self.__btn_id.setStyleSheet("color:none;"
                                    "font-size:15pt;")

    @classmethod
    def get_current_size(cls):
        return len(cls.__units)

    @classmethod
    def set_clear_callbacks_for_all(cls):
        for btn in cls.__units:
            btn.set_clear_callbacks()

    @classmethod
    def set_buttoms_default_color(cls):
        for btn in cls.__units:
            btn.set_btn_color_default()

    @classmethod
    def set_buttoms_default_values(cls):
        for btn in cls.__units:
            btn.set_buttons_default_value()

    @classmethod
    def get_unit_from_index(cls, index: int):
        return cls.__units[index]

    @classmethod
    def get_all_tests(cls) -> list | None:
        ret_list = list()
        for btn in cls.__units:
            test = btn.get_test_type()
            if test == TEST_TYPE.TEST_NONE:
                continue

            ret_list.append(test)

        if len(ret_list) > 0:
            return ret_list

    @classmethod
    def get_unit_from_test_type(cls, test_type: TEST_TYPE):
        for btn in cls.__units:
            if btn.get_test_type() == test_type:
                return btn
