import configparser
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow, QPushButton
from PySide6.QtGui import QFontDatabase

from ui.untitled import Ui_MainWindow
from common import send_message_box, SMBOX_ICON_TYPE, get_about_text, get_rules_text

from components.CConfig import CNewConfig, CParameters, BLOCKS_DATA, SYS_INFO_PARAMS, CONFIG_PARAMS
from components.CTests import CTests, TEST_TYPE
from components.CConfig_Main import CMainConfig
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

        self.main_config = CMainConfig()
        # ---------------------------------------
        try:
            if self.main_config.load_data() is False:
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                 text="Ошибка в главном файле конфигурации!\n"
                                      "Один или несколько параметров ошибочны!",
                                 title="Внимание!",
                                 variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
                return

        except Exception as err:
            send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                             text="Ошибка в файле конфигурации!\n"
                                  "Один или несколько параметров ошибочны!\n\n"
                                  f"Ошибка: '{err}'",
                             title="Внимание!",
                             variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
            return

        self.cconfig_unit = CNewConfig()
        self.cconfig_unit.init_params()

        filtred_files = CNewConfig.get_configs_list_in_folder()
        if filtred_files is not None:
            for item in filtred_files:
                if item.find("main.ini") != -1:
                    continue
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

        self.ui.comboBox_config_get.currentIndexChanged.connect(self.on_changed_config)

        only_config_name = self.main_config.get_only_config_name()
        if len(only_config_name):
            current_index = self.get_item_index_from_text(only_config_name)
            if current_index is not None:
                self.ui.comboBox_config_get.setCurrentIndex(current_index)
                self.on_changed_config()
                self.ui.comboBox_config_get.setEnabled(False)
                return

        last_config = self.main_config.get_last_config_name()
        if len(last_config):
            current_index = self.get_item_index_from_text(last_config)
            if current_index is not None:
                self.ui.comboBox_config_get.setCurrentIndex(current_index)
                self.on_changed_config()
                return

        self.ui.comboBox_config_get.setCurrentIndex(-1)

    def on_user_presed_launch_test(self, test_type: TEST_TYPE):
        print(f"Запущен тест: {test_type}")

    def on_changed_config(self):
        text = self.ui.comboBox_config_get.currentText()
        print(text)
        if text:

            if not self.cconfig_unit.set_init_config(text):
                self.cconfig_unit.create_config_data()
                self.close()
                return

            try:
                self.cconfig_unit.load_config()
            except:
                self.cconfig_unit.create_config_data()
                self.send_error_message(
                    "Во время выполнения программы произошла ошибка считывания конфигурации.\n"
                    "Весь конфиг файл был сброшен по умолчанию!\n\n"
                    f"Код ошибки: 'on_changed_config -> [Error Read Data]'")
                self.close()
                return
            config_human_name = self.cconfig_unit.get_config_value(BLOCKS_DATA.PROGRAM_SETTING, CONFIG_PARAMS.CONFIG_NAME)
            self.ui.label_monoblock_config_name.setText(f"Тест моноблоков: {config_human_name}")
            self.main_config.save_last_config(text)

            # LOAD
            CSystemInfo.set_test_used(self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.SYS_INFO_TEST_USED))
            CSystemInfo.set_bios_stats(self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.BIOS_CHECK))
            CSystemInfo.set_cpu_stats(self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.CPU_CHECK))
            CSystemInfo.set_ram_stats(self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.RAM_CHECK))
            CSystemInfo.set_disk_stats(self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.DISK_CHECK))

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

            print(config_human_name)

    def send_error_message(self, text: str):
        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                         text=text,
                         title="Фатальная ошибка",
                         variant_yes="Закрыть программу", variant_no="", callback=lambda: self.set_close())

    def get_item_index_from_text(self, item_text: str) -> int | None:
        for index in range(0, self.ui.comboBox_config_get.count()):
            print(self.ui.comboBox_config_get.itemText(index), item_text)
            if self.ui.comboBox_config_get.itemText(index) == item_text:
                return index
        return None

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
