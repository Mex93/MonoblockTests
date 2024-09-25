import configparser
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow, QPushButton
from PySide6.QtGui import QFontDatabase

from ui.untitled import Ui_MainWindow
from common import send_message_box, SMBOX_ICON_TYPE, get_about_text, get_rules_text

from components.CConfig import CTests, CConfig, TEST_TYPE
from components.CSystemInfo import CSystemInfo


# pyside6-uic .\ui\untitled.ui -o .\ui\untitled.py
# pyside6-rcc .\ui\res.qrc -o .\ui\res_rc.py
# Press the green button in the gutter to run the script.


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__base_program_version = "0.1"  # Менять при каждом обновлении любой из подпрограмм

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QFontDatabase.addApplicationFont("designs/Iosevka Bold.ttf")
        self.setWindowTitle(f'Печать QR Kvant 2024 v0.1 Бумага 58 на 20')

        self.cconfig_unit = None

        filtred_files = CConfig.get_configs_list_in_folder()
        if filtred_files is not None:
            for item in filtred_files:
                self.ui.comboBox_config_get.addItem(item)

        buttons = list()
        buttons.append(self.ui.pushButton_btn1)
        buttons.append(self.ui.pushButton_btn2)
        buttons.append(self.ui.pushButton_btn3)
        buttons.append(self.ui.pushButton_btn4)
        buttons.append(self.ui.pushButton_btn5)
        buttons.append(self.ui.pushButton_btn6)
        buttons.append(self.ui.pushButton_btn7)
        buttons.append(self.ui.pushButton_btn8)
        buttons.append(self.ui.pushButton_btn9)
        buttons.append(self.ui.pushButton_btn10)
        buttons.append(self.ui.pushButton_btn11)
        buttons.append(self.ui.pushButton_btn12)

        # кнопки в дефолт
        for btn in buttons:
            btn_unit = Buttoms(btn)
            btn_unit.set_buttons_default_value()
            btn_unit.set_enabled(False)

        self.ui.comboBox_config_get.setCurrentIndex(-1)
        self.ui.comboBox_config_get.currentIndexChanged.connect(self.on_changed_config)

    def on_user_presed_launch_test(self, test_type: TEST_TYPE):
        print(f"Запущен тест: {test_type}")

    def on_changed_config(self):
        text = self.ui.comboBox_config_get.currentText()
        if text:
            print(text)
            if not CConfig.set_init_config(text):
                CConfig.create_config_data()
                self.close()
                return

            c_handler = CConfig.get_config_handler()
            if c_handler is not None:
                try:
                    CConfig.load_config()
                except:
                    CConfig.create_config_data()
                    self.send_error_message(
                        "Во время выполнения программы произошла ошибка считывания конфигурации.\n"
                        "Весь конфиг файл был сброшен по умолчанию!\n\n"
                        f"Код ошибки: 'on_changed_config -> [Error Read Data]'")
                    self.close()
                    return

                name = CConfig.get_config_text_name()
                if name:
                    self.ui.label_monoblock_config_name.setText(f"Тест моноблоков: {name}")

                    # LOAD
                    CSystemInfo.set_test_used(CConfig.sys_info_test_used)
                    CSystemInfo.set_bios_stats(CConfig.bios_stats)
                    CSystemInfo.set_cpu_stats(CConfig.cpu_stats)
                    CSystemInfo.set_ram_stats(CConfig.ram_stats)
                    CSystemInfo.set_disk_stats(CConfig.disks_stats)

                    Buttoms.set_clear_callbacks_for_all()

                    block_datas = CTests.get_config_block_data()
                    btn_index = 0
                    for index, block_data in enumerate(block_datas):
                        bname, btype = block_datas[index]
                        if btype == TEST_TYPE.TEST_SYSTEM_INFO:
                            if CSystemInfo.is_test_used():
                                btn_unit = Buttoms.get_unit_from_index(btn_index)
                                btn_unit.set_callback(btype, self.on_user_presed_launch_test)
                                btn_unit.set_name(bname)
                                btn_unit.set_enabled(True)
                                btn_unit.set_hidden(False)
                                btn_index += 1

                    # отключаем лишние
                    btn_size = Buttoms.get_current_size()
                    if btn_index < btn_size:
                        for index in range(btn_index, btn_size):
                            btn_unit = Buttoms.get_unit_from_index(index)
                            btn_unit.set_enabled(False)
                            btn_unit.set_hidden(True)

                    print(CConfig.bios_stats)

    def send_error_message(self, text: str):
        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                         text=text,
                         title="Фатальная ошибка",
                         variant_yes="Закрыть программу", variant_no="", callback=lambda: self.set_close())

    def set_close(self):
        sys.exit()


class Buttoms:
    __units = list()

    def __init__(self, btn_id: QPushButton):
        self.__btn_id = btn_id
        self.__callback_func = None
        self.__units.append(self)

    def set_callback(self, test_type: TEST_TYPE, func):
        if self.__callback_func is None:
            self.__callback_func = func
            self.__btn_id.clicked.connect(lambda: func(test_type))

    @classmethod
    def get_current_size(cls):
        return len(cls.__units)

    @classmethod
    def set_clear_callbacks_for_all(cls):
        for btn in cls.__units:
            btn.set_clear_callbacks()

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
        self.set_clear_callbacks()

    @classmethod
    def set_buttoms_default_values(cls):
        for btn in cls.__units:
            btn.set_buttons_default_value()
    @classmethod
    def get_unit_from_index(cls, index: int):
        return cls.__units[index]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
