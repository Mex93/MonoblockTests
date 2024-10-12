
class TestResultLabel:
    __list_of_tests = list()
    __main_window = None
    __text_of_tests = set()

    @classmethod
    def set_main_window(cls,  main_window):
        TestResultLabel.__main_window = main_window

    @classmethod
    def is_label_show(cls) -> bool:
        return not cls.__main_window.ui.label_tests_failed.isHidden()

    @classmethod
    def set_show_status(cls, result: bool):
        result = not result
        cls.__main_window.ui.label_tests_failed.setHidden(result)

    @classmethod
    def clear_text(cls):
        cls.__text_of_tests.clear()
        cls.__update_text()

    @classmethod
    def is_any_element(cls) -> bool:
        clist = list(cls.__text_of_tests)
        if len(clist):
            return True
        else:
            return False

    @classmethod
    def delete_test(cls, text: str):
        try:
            cls.__text_of_tests.remove(text)
            cls.__update_text()
        except KeyError:

            if not len(cls.__text_of_tests):
                cls.set_show_status(False)

    @classmethod
    def __update_text(cls):
        if not len(cls.__text_of_tests):
            cls.__main_window.ui.label_tests_failed.setText("Тесты провалены: -")
        else:
            cls.__main_window.ui.label_tests_failed.setText(f"<span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">Тесты провалены: </span> <br> {'<br>'.join(cls.__text_of_tests)}")

    @classmethod
    def add_text(cls, text: str):
        if text not in cls.__text_of_tests:
            cls.__text_of_tests.add(text)
            cls.__update_text()
