import time
from sys import argv, exit
from os.path import isdir as file_isdir
from os.path import abspath as os_abspath
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QTimer

from wmi import WMI
import subprocess
import argparse
from ui.untitled import Ui_MainWindow
from ui.get_check_string_window import Ui_MainWindow as Ui_StringWindow

from components.CErrorLabel import TestResultLabel

from common import (send_message_box, SMBOX_ICON_TYPE, get_about_text, get_rules_text, send_message_box_triple_variant,
                    get_current_unix_time)
from enuuuums import PROGRAM_JOB_TYPE

from components.CConfig import CNewConfig, BLOCKS_DATA, SYS_INFO_PARAMS, CONFIG_PARAMS
from components.CTests import CTests, TEST_TYPE, CTestProcess, TEST_RESULT
from components.CConfig_Main import CMainConfig
from components.CSystemInfoTest import CSystemInfo, CSystemInfoWindow
from components.CExternalDisplayTest import CExternalDisplayWindow, CExternalDisplay, EXTERNAL_DISPLAY_PARAMS
from components.CSpeakerTest import CSpeakerTestWindow, CSpeakerTest, SPEAKER_PARAMS
from components.CVideoCamTest import CVideoCam, CVideoCamWindow, VIDEO_CAM_PARAMS
from components.CKeysBTNTest import CKeyTest, CKeyTestWindow, KEYSBUTTOMS_PARAMS
from components.CBrightnessTest import CBrightnessTest, CBrightnessTestWindow, BRIGHTNESS_PARAMS
from components.CPatternsTest import CPatternsTest, CPatternsTestWindow, PATTERNS_TEST_PARAMS
from components.CUSBTest import CUSBDevicesTest, CUSBDevicesTestWindow, USB_TEST_PARAMS
from components.CButtons import CButtoms


# from components.CHWMonitor import HWMonitor


# pyside6-uic .\ui\test.ui -o .\ui\test.py

# pyside6-uic .\ui\untitled.ui -o .\ui\untitled.py
# pyside6-uic .\ui\get_check_string_window.ui -o .\ui\get_check_string_window.py
# pyside6-uic .\ui\test_sys_info.ui -o .\ui\test_sys_info.py
# pyside6-uic .\ui\test_external_display.ui -o .\ui\test_external_display.py
# pyside6-uic .\ui\test_videocam.ui -o .\ui\test_videocam.py
# pyside6-uic .\ui\test_keys.ui -o .\ui\test_keys.py
# pyside6-uic .\ui\test_brightness.ui -o .\ui\test_brightness.py
# pyside6-uic .\ui\test_patterns.ui -o .\ui\test_patterns.py
# pyside6-uic .\ui\test_usb_devices.ui -o .\ui\test_usb_devices.py
# pyside6-uic .\ui\test_speaker_audio.ui -o .\ui\test_speaker_audio.py
# pyside6-rcc .\ui\res.qrc -o .\ui\res_rc.py


class MainWindow(QMainWindow):
    def __init__(self, pr_type2: PROGRAM_JOB_TYPE, parent=None):
        super().__init__(parent)

        self.__base_program_version = "0.2"  # Менять при каждом обновлении любой из подпрограмм

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QFontDatabase.addApplicationFont("designs/Iosevka Bold.ttf")
        self.PROGRAM_JOB_FLAG = pr_type2
        if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_NORMAL:
            self.setWindowTitle(f'Тестирование моноблоков Kvant 2024 v1.0 [ALL]')
        elif self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:
            self.setWindowTitle(f'Тестирование моноблоков Kvant 2024 v1.0 [LINE]')
        else:
            self.setWindowTitle(f'Тестирование моноблоков Kvant 2024 v1.0 [-]')
        self.load_with_error = False
        self.auto_test_line_time_launch = False
        self.button_blocker = 0
        self.main_config = CMainConfig()
        # ---------------------------------------
        try:
            if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_NORMAL:
                if self.main_config.load_data() is False:
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text="Ошибка в главном файле конфигурации!\n"
                                          "Один или несколько параметров ошибочны!",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
                    return

            if not file_isdir("content"):
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                 text="Ошибка проверки компонентов!\n\n"
                                      "В директории должна быть папка 'content'. В этой директории лежат тестовые файлы!",
                                 title="Внимание!",
                                 variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
                return

            if not file_isdir("content/patterns"):
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                 text="Ошибка проверки компонентов!\n\n"
                                      "В директории должна быть папка 'content/patterns'. В этой директории лежат паттерны для проверки дисплея!",
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
        self.ctest_process = CTestProcess()
        TestResultLabel.set_main_window(self)
        TestResultLabel.set_show_status(False)

        self.ui.pushButton_launchall.setEnabled(False)
        self.ui.pushButton_clear.setEnabled(False)

        self.cmain_window_get_string = CStringWindow(self)
        self.ctest_window_sys_info = CSystemInfoWindow(self)
        self.ctest_window_external_display = CExternalDisplayWindow(self)
        self.ctest_window_video_cam = CVideoCamWindow(self)
        self.ctest_window_hardwarekeys = CKeyTestWindow(self)
        self.ctest_window_usb_devices = CUSBDevicesTestWindow(self)
        self.ctest_window_brightness = CBrightnessTestWindow(self)
        self.ctest_window_patterns = CPatternsTestWindow(self)
        self.ctest_window_speaker_window = CSpeakerTestWindow(self, TEST_TYPE.TEST_SPEAKER_MIC)
        self.ctest_window_headset_window = CSpeakerTestWindow(self, TEST_TYPE.TEST_HEADSET_MIC)
        # self.chw_monitor = HWMonitor()

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
            btn_unit = CButtoms(btn)
            btn_unit.set_buttons_default_value()
            btn_unit.set_enabled(False)

        self.ui.comboBox_config_get.currentIndexChanged.connect(self.on_changed_config)
        self.ui.pushButton_exit.clicked.connect(self.set_close)
        self.ui.pushButton_clear.clicked.connect(self.on_user_pressed_clear_all_test)
        self.ui.pushButton_launchall.clicked.connect(self.on_user_pressed_start_all_test)
        self.ui.pushButton_get_strings.clicked.connect(self.on_user_pressed_check_string)
        self.ui.pushButton_furmark.clicked.connect(self.on_user_clicked_on_run_furmark)
        self.ui.pushButton_cpu_temp.clicked.connect(self.on_user_clicked_on_run_ophwm)

        self.ui.action_info.triggered.connect(self.rules)

        self.ui.pushButton_alter_prog.setHidden(True)
        if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_NORMAL:
            timer_update_cpu_temp = QTimer(self)
            timer_update_cpu_temp.timeout.connect(self.on_timer_cpu_temp_update)
            timer_update_cpu_temp.start(2000)
            self.ui.pushButton_cpu_temp.setHidden(False)

        else:
            self.ui.pushButton_cpu_temp.setHidden(True)

        self.call_time_sync_bat()
        if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_NORMAL:
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
            if self.ui.comboBox_config_get.count() == 0:
                send_message_box_triple_variant(icon_style=SMBOX_ICON_TYPE.ICON_WARNING,
                                                text="Программа обнаружила, что не создано ни одного файла конфигурации для выбора.\n\n"
                                                     f"Вы можете создать файл конфигурации в автоматическом режиме или выйти из программы.\n"
                                                     f"Без файла конфигурации дальнейшая работа программы невозможна.\n\n"
                                                     f"После создания файла конфигурации, Вы сможете зайти в папку с программой и переименовать его название.\n"
                                                     f"Все настройки нового файла конфигурации будут установлены на стандартные значения.",
                                                title="Ошибка поиска конфигурации",
                                                variant_yes="Закрыть программу",
                                                variant_no="Создать новую конфигурацию",
                                                variant_apply="",
                                                callback=self.on_config_is_not_find,
                                                exit_callback=lambda: self.on_config_is_not_find(None))

        else:
            self.ui.comboBox_config_get.setCurrentIndex(-1)
            self.on_changed_config()

    def set_get_button_blocker(self) -> bool:
        if self.button_blocker < get_current_unix_time():
            self.button_blocker = get_current_unix_time() + 1
            return True

        return False

    def on_user_clicked_on_run_ophwm(self):
        # надо перепилить
        if not self.set_get_button_blocker():
            return
        patch = "OpenHardwareMonitor/OpenHardwareMonitor.exe"
        self.run_programm(patch)

    def run_programm(self, patch: str):
        result = ""
        if isinstance(patch, str) and len(patch):
            if patch.find('.exe') != -1:
                result = self.run_external_program(patch)
                if result is True:
                    return
            elif patch.find('.bat') != -1:
                result = self.run_external_bat(patch)
                if result is True:
                    return

        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                         text="Не удалось запустить программу!\n"
                              "Поддерживается .exe, .bat файлы.\n"
                              f"Путь: {patch}!\n"
                              f"Ошибка: {result}",
                         title="Внимание!",
                         variant_yes="Закрыть", variant_no="", callback=None)

    def on_user_clicked_on_run_furmark(self):
        if not self.set_get_button_blocker():
            return
        patch = self.main_config.get_furmark_patch()
        self.run_programm(patch)

    @staticmethod
    def run_external_program(program_path) -> bool | str:
        try:
            subprocess.Popen(program_path)
            return True

        except Exception as err:
            return str(err)

    @staticmethod
    def run_external_bat(program_path) -> bool:
        try:
            full_path = os_abspath(program_path)
            subprocess.Popen(full_path)
            return True

        except subprocess.CalledProcessError as e:
            print(f"Произошла ошибка при выполнении батника: {e}")
            return False

        except FileNotFoundError:
            print("Файл не найден. Проверьте путь к .bat файлу.")
            return False

    def on_timer_cpu_temp_update(self):
        try:
            w = WMI(namespace="root/OpenHardwareMonitor")
            temperature_infos = w.Sensor()
            for sensor in temperature_infos:
                if sensor.SensorType == u'Temperature':
                    # print(sensor.Name, sensor.Value)
                    if isinstance(sensor.Name, str):
                        if sensor.Name.find("CPU Package") != -1:
                            self.ui.pushButton_cpu_temp.setText(f"{sensor.Name}: {sensor.Value}")
                            return
        except:
            pass

        self.ui.pushButton_cpu_temp.setText(f"Запустите OpenHardwareMonitor")

    @classmethod
    def rules(cls):
        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_INFO,
                         text=f"{get_about_text()}"
                              f"\n"
                              f"\n"
                              f"{get_rules_text()}",
                         title="О программе",
                         variant_yes="Закрыть", variant_no="")

    def get_window_title(self) -> str:
        return self.windowTitle()

    def on_user_pressed_check_string(self):
        if not self.set_get_button_blocker():
            return
        result = self.ctest_window_sys_info.get_data(False)
        string_window = self.cmain_window_get_string
        string_window.ui.textBrowser_set_string.clear()
        string_window.ui.textBrowser_set_string.setStyleSheet("font-size:14pt;"
                                                              ""
                                                              "")
        if result:
            data, on_test_count, is_test_passed_count, is_test_fail_string_check_count = result
            string_window.ui.textBrowser_set_string.append("Получение информации...\n")
            if data is None:
                string_window.ui.textBrowser_set_string.append("Все тесты отключены. "
                                                               "Для получения нужных строк сравнения ключите нужные Вам тесты!")
            else:
                for item_dict in data:
                    test_type = item_dict.get("test_id", None)
                    item_data = item_dict.get("only_data", None)
                    item_check_string = item_dict.get("check_string", None)
                    if None in (test_type, item_data, item_check_string):
                        continue
                    test_name = CSystemInfo.get_sub_test_name_from_type(test_type)
                    if test_name is not None:
                        string_window.ui.textBrowser_set_string.append(f"Тест '{test_name}'\n"
                                                                       f"Строка информации: {item_data}\n"
                                                                       f"Строка проверки: {item_check_string}\n")

                string_window.ui.textBrowser_set_string.append(f"Всего тестов активировано: {on_test_count}\n"
                                                               f"Тестов провалено: {on_test_count - is_test_passed_count}\n"
                                                               f"Тестов сравнений строк провалено: {is_test_fail_string_check_count}\n"
                                                               f"Тестов успешно: {is_test_passed_count}\n")

                string_window.ui.textBrowser_set_string.append(
                    "Примечание: Строка проверки копируется полностью в конфиг")
        else:
            string_window.ui.textBrowser_set_string.append("Все тесты отключены!\n")
        string_window.show()
        string_window.setFocus()

    def on_user_pressed_start_all_test(self):
        if not self.set_get_button_blocker():
            return

        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.stop_test()

        self.ui.pushButton_launchall.setText("Тесты запущены...")

        TestResultLabel.clear_text()
        TestResultLabel.set_show_status(False)

        test_list = CButtoms.get_all_tests()
        if test_list is None:
            send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                             text="Ошибка в обработчике старта теста!\n"
                                  "Список с тестами из класса кнопок пуст!\n\n",
                             title="Внимание!",
                             variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
            return

        for test in test_list:
            self.ctest_process.add_test_in_launch(test)

        first_test = test_list[0]
        self.ctest_process.start_test(first_test)
        CButtoms.set_buttoms_default_color()
        self.show_test_window_no_window(first_test, True)

    def on_user_pressed_clear_all_test(self):
        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.stop_test()
            self.ui.pushButton_launchall.setText("Запустить всё")
        TestResultLabel.clear_text()
        TestResultLabel.set_show_status(False)

        CButtoms.set_buttoms_default_color()

    def on_user_presed_launch_test(self, test_type: TEST_TYPE):
        print(f"Запущен тест: {test_type}")
        if self.ctest_process.is_test_launch() == TEST_TYPE.TEST_NONE and self.auto_test_line_time_launch is False:
            test_list = CTests.get_avalible_test_list()
            if len(test_list):
                if test_type in test_list:
                    self.show_test_window_with_window(test_type, False)

    def on_changed_config(self):

        text = self.ui.comboBox_config_get.currentText()
        if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:
            text = "For Line"
        if text:
            if self.ctest_process.is_test_launch() != TEST_TYPE.TEST_NONE:
                self.ctest_process.stop_test()
                self.ui.pushButton_launchall.setText("Запустить всё")

            CButtoms.set_buttoms_default_color()
            if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_NORMAL:
                if not self.cconfig_unit.set_init_config(text):
                    self.cconfig_unit.create_config_data()
                    self.close()
                    return

                try:
                    self.cconfig_unit.load_config()
                except Exception as err:
                    # self.cconfig_unit.create_config_data()

                    send_message_box_triple_variant(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                                    text="Во время выполнения программы произошла ошибка считывания конфигурации.\n\n"
                                                         f"Конфигуратор сообщил детальный код ошибки: '{err}'!\n\n"
                                                         f"Код ошибки блока RunTime: 'on_changed_config -> [Error Read Config Data]'",
                                                    title="Фатальная ошибка",
                                                    variant_yes="Закрыть программу",
                                                    variant_no="Сбросить конфиг по умолчанию",
                                                    variant_apply="Продолжить выполнение",
                                                    callback=self.on_config_is_broken, exit_callback=
                                                    lambda: self.on_config_is_broken(None))
                    if not self.load_with_error:
                        return

                    # self.send_error_message(
                    #     "Во время выполнения программы произошла ошибка считывания конфигурации.\n"
                    #     "Весь конфиг файл был сброшен по умолчанию!\n\n"
                    #     f"Код ошибки: 'on_changed_config -> [Error Read Data]'")
                    # self.close()
                    # return
                display_resolution = self.cconfig_unit.get_config_value(BLOCKS_DATA.PROGRAM_SETTING,
                                                                        CONFIG_PARAMS.DISPLAY_RESOLUTION)

                if len(display_resolution):
                    if display_resolution.find("x") != -1:
                        height: str
                        width: str

                        height, width = display_resolution.split("x")
                        if height.isnumeric() and width.isnumeric():
                            display_resolution = [int(height), int(width)]

                if isinstance(display_resolution, list):
                    self.ctest_window_external_display.resize(*display_resolution)

                else:
                    # на всю длинну если не задано
                    # задаётся и для видео кам теста через конфиг экстерн дисплея
                    CExternalDisplay.set_test_stats(CONFIG_PARAMS.DISPLAY_RESOLUTION, "full-screen")

                config_human_name = self.cconfig_unit.get_config_value(BLOCKS_DATA.PROGRAM_SETTING,
                                                                       CONFIG_PARAMS.CONFIG_NAME)

                self.ui.label_monoblock_config_name.setText(f"Тест моноблоков: {config_human_name}")

                self.main_config.save_last_config(text)
            else:
                CExternalDisplay.set_test_stats(CONFIG_PARAMS.DISPLAY_RESOLUTION, "full-screen")

            self.ui.pushButton_get_strings.setHidden(True)
            if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:
                self.ui.pushButton_get_strings.setEnabled(False)
                self.ui.comboBox_config_get.setEnabled(False)
                self.ui.pushButton_launchall.setEnabled(False)
                self.ui.pushButton_clear.setEnabled(False)
                self.ui.pushButton_furmark.setHidden(True)
                self.ui.label_monoblock_config_name.setText("Тесты для сборочной линии")

            if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_NORMAL:
                # LOAD
                # Sys Info
                # check
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.TEST_USED,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.TEST_USED))

                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.BIOS_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.BIOS_CHECK))

                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.MB_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.MB_CHECK))

                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.CPU_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.CPU_CHECK))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.RAM_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.RAM_CHECK))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.DISK_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.DISK_CHECK))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.WLAN_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.WLAN_CHECK))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.BT_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.BT_CHECK))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.LAN_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.LAN_CHECK))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.OS_CHECK,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.OS_CHECK))

                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.OS_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.OS_STRING))

                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.LAN_IP,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.LAN_IP))

                # string
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.BIOS_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.BIOS_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.CPU_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.CPU_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.RAM_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.RAM_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.DISK_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.DISK_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.WLAN_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.WLAN_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.BT_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.BT_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.LAN_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.LAN_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.MB_MODEL_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.MB_MODEL_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.MB_FAMILY_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.MB_FAMILY_STRING))
                CSystemInfo.set_test_stats(SYS_INFO_PARAMS.MB_SKU_NUMBER_STRING,
                                           self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                              SYS_INFO_PARAMS.MB_SKU_NUMBER_STRING))

                # External display
                # check
                CExternalDisplay.set_test_stats(EXTERNAL_DISPLAY_PARAMS.TEST_USED,
                                                self.cconfig_unit.get_config_value(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST,
                                                                                   EXTERNAL_DISPLAY_PARAMS.TEST_USED))
                # string
                CExternalDisplay.set_test_stats(EXTERNAL_DISPLAY_PARAMS.VIDEO_PATCH,
                                                self.cconfig_unit.get_config_value(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST,
                                                                                   EXTERNAL_DISPLAY_PARAMS.VIDEO_PATCH))

                CExternalDisplay.set_test_stats(EXTERNAL_DISPLAY_PARAMS.WINDOW_DEFAULT,
                                                self.cconfig_unit.get_config_value(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST,
                                                                                   EXTERNAL_DISPLAY_PARAMS.WINDOW_DEFAULT))

                CExternalDisplay.set_test_stats(EXTERNAL_DISPLAY_PARAMS.WINDOW_SWITCH_TO,
                                                self.cconfig_unit.get_config_value(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST,
                                                                                   EXTERNAL_DISPLAY_PARAMS.WINDOW_SWITCH_TO))

                # Speaker test
                # check
                CSpeakerTest.set_test_stats(SPEAKER_PARAMS.SPEAKER_TEST_USED,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                               SPEAKER_PARAMS.SPEAKER_TEST_USED))
                CSpeakerTest.set_test_stats(SPEAKER_PARAMS.HEADSET_TEST_USED,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                               SPEAKER_PARAMS.HEADSET_TEST_USED))

                CSpeakerTest.set_test_stats(SPEAKER_PARAMS.SPEAKER_TEST_RECORD_ENABLE,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                               SPEAKER_PARAMS.SPEAKER_TEST_RECORD_ENABLE))

                CSpeakerTest.set_test_stats(SPEAKER_PARAMS.HEADSET_TEST_RECORD_ENABLE,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                               SPEAKER_PARAMS.HEADSET_TEST_RECORD_ENABLE))

                # string
                CSpeakerTest.set_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_LEFT,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                               SPEAKER_PARAMS.AUDIO_PATCH_LEFT))
                CSpeakerTest.set_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_RIGHT,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                               SPEAKER_PARAMS.AUDIO_PATCH_RIGHT))

                # VideoCam test
                # check
                CVideoCam.set_test_stats(VIDEO_CAM_PARAMS.TEST_USED,
                                         self.cconfig_unit.get_config_value(BLOCKS_DATA.VIDEO_CAM_TEST,
                                                                            VIDEO_CAM_PARAMS.TEST_USED))
                CVideoCam.set_test_stats(VIDEO_CAM_PARAMS.CAMERA_INDEX,
                                         self.cconfig_unit.get_config_value(BLOCKS_DATA.VIDEO_CAM_TEST,
                                                                            VIDEO_CAM_PARAMS.CAMERA_INDEX))

                # HardwareKeys test
                # check
                CKeyTest.set_test_stats(KEYSBUTTOMS_PARAMS.TEST_USED,
                                        self.cconfig_unit.get_config_value(BLOCKS_DATA.HARDWARE_BTN_TEST,
                                                                           KEYSBUTTOMS_PARAMS.TEST_USED))

                # Brighntess test
                # check
                CBrightnessTest.set_test_stats(BRIGHTNESS_PARAMS.TEST_USED,
                                               self.cconfig_unit.get_config_value(BLOCKS_DATA.BRIGHTNESS_TEST,
                                                                                  BRIGHTNESS_PARAMS.TEST_USED))

                CBrightnessTest.set_test_stats(BRIGHTNESS_PARAMS.FILE_PATCH,
                                               self.cconfig_unit.get_config_value(BLOCKS_DATA.BRIGHTNESS_TEST,
                                                                                  BRIGHTNESS_PARAMS.FILE_PATCH))

                # USB Devices test
                # check
                CUSBDevicesTest.set_test_stats(USB_TEST_PARAMS.TEST_USED,
                                               self.cconfig_unit.get_config_value(BLOCKS_DATA.USB_DEVICE_TEST,
                                                                                  USB_TEST_PARAMS.TEST_USED))

                CUSBDevicesTest.set_test_stats(USB_TEST_PARAMS.MAX_SIZE,
                                               self.cconfig_unit.get_config_value(BLOCKS_DATA.USB_DEVICE_TEST,
                                                                                  USB_TEST_PARAMS.MAX_SIZE))

                # Patterns test
                # check
                CPatternsTest.set_test_stats(PATTERNS_TEST_PARAMS.TEST_USED,
                                             self.cconfig_unit.get_config_value(BLOCKS_DATA.PATTERNS_TEST,
                                                                                PATTERNS_TEST_PARAMS.TEST_USED))
            else:  # Only Line
                CVideoCam.set_test_stats(VIDEO_CAM_PARAMS.CAMERA_INDEX,
                                         0)

                CSpeakerTest.set_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_LEFT,
                                            "content/audio_test_left.mp3")
                CSpeakerTest.set_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_RIGHT,
                                            "content/audio_test_right.mp3")

            CButtoms.set_clear_callbacks_for_all()

            btn_index = 0

            if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:

                tests_list = \
                    [
                        [CSystemInfo, TEST_TYPE.TEST_SYSTEM_INFO, SYS_INFO_PARAMS.TEST_USED, None],
                        [CSpeakerTest, TEST_TYPE.TEST_SPEAKER_MIC, SPEAKER_PARAMS.SPEAKER_TEST_USED, None],
                        [CPatternsTest, TEST_TYPE.TEST_PATTERNS, PATTERNS_TEST_PARAMS.TEST_USED, None],
                        [CVideoCam, TEST_TYPE.TEST_FRONT_CAMERA, VIDEO_CAM_PARAMS.TEST_USED, None]
                    ]
            else:

                self.ui.pushButton_launchall.setEnabled(True)
                self.ui.pushButton_clear.setEnabled(True)
                tests_list = \
                    [
                        [CSystemInfo, TEST_TYPE.TEST_SYSTEM_INFO, SYS_INFO_PARAMS.TEST_USED, None],
                        [CExternalDisplay, TEST_TYPE.TEST_EXTERNAL_DISPLAY, EXTERNAL_DISPLAY_PARAMS.TEST_USED, None],
                        [CVideoCam, TEST_TYPE.TEST_FRONT_CAMERA, VIDEO_CAM_PARAMS.TEST_USED, None],
                        [CSpeakerTest, TEST_TYPE.TEST_SPEAKER_MIC, SPEAKER_PARAMS.SPEAKER_TEST_USED, None],
                        [CSpeakerTest, TEST_TYPE.TEST_HEADSET_MIC, SPEAKER_PARAMS.HEADSET_TEST_USED, None],
                        [CKeyTest, TEST_TYPE.TEST_HARDWARE_BTN, KEYSBUTTOMS_PARAMS.TEST_USED, None],
                        [CBrightnessTest, TEST_TYPE.TEST_BRIGHTNESS, BRIGHTNESS_PARAMS.TEST_USED, None],
                        [CUSBDevicesTest, TEST_TYPE.TEST_USB_DEVICES, USB_TEST_PARAMS.TEST_USED, None],
                        [CPatternsTest, TEST_TYPE.TEST_PATTERNS, PATTERNS_TEST_PARAMS.TEST_USED, None],
                    ]

            self.ui.pushButton_get_strings.setHidden(True)
            # name insert
            for index, test in enumerate(tests_list, 0):
                tests_list[index][3] = CTests.get_test_name_from_test_type(tests_list[index][1])

            # buffering tests

            for index, test in enumerate(tests_list):
                test_class, btype, on_params, bname = test

                is_only_line_test = False
                load = False

                if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:
                    is_only_line_test = True
                    load = True

                if not is_only_line_test:
                    if test_class.get_test_stats(on_params) is True:
                        load = True
                        if btype == TEST_TYPE.TEST_SYSTEM_INFO:
                            self.ui.pushButton_get_strings.setHidden(False)  # ИЗНАЧАЛЬНО ВЫКЛЮЧАЮ

                if load:
                    btn_unit = CButtoms.get_unit_from_index(btn_index)
                    btn_unit.set_callback(btype, self.on_user_presed_launch_test)
                    btn_unit.set_name(bname)
                    btn_unit.set_enabled(True)
                    btn_unit.set_hidden(False)
                    btn_index += 1

            # отключаем лишние
            btn_size = CButtoms.get_current_size()
            if btn_index < btn_size:
                for index in range(btn_index, btn_size):
                    btn_unit = CButtoms.get_unit_from_index(index)
                    btn_unit.set_enabled(False)
                    btn_unit.set_hidden(True)

            if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:
                self.auto_test_line_time_launch = True

                self.ctest_window_sys_info.disabled_test_for_only_line()
                timer = QTimer(self)
                timer.timeout.connect(
                    lambda: self.on_launch_line_start(timer))  # сколько навесиш раз функцию столько и будет вызываться
                timer.start(1500)

    def on_launch_line_start(self, timer_id: QTimer):
        timer_id.stop()
        self.auto_test_line_time_launch = False
        self.on_user_pressed_start_all_test()

    def on_config_is_not_find(self, variants: QPushButton | None):
        """
        Напоминаение: on_config_is_not_find вызовется быстрее, чем выполнится msg бокс
        :param variants:
        :return:
        """
        if variants is None:
            self.set_close()
            return

        text = variants.text()
        if text.find("Продолжить выполнение") != -1:
            self.load_with_error = True

        elif text.find("Закрыть программу") != -1:
            self.set_close()
        elif text.find("Создать новую конфигурацию") != -1:
            config_name = self.cconfig_unit.create_new_config_data()
            if isinstance(config_name, bool):
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                 text=f"Файл конфигурации небыл создан из за ошибки.\n"
                                      "Перезагрузите программу.",
                                 title="Создание нового файла конфигурации",
                                 variant_yes="Закрыть программу", variant_no="", callback=lambda: self.set_close())
            else:
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_INFO,
                                 text=f"Файл конфигурации успешно создан с названием '{config_name}'.\n"
                                      "Программа должна быть перезагружена для удачной загрузки нового файла конфигурации.",
                                 title="Создание нового файла конфигурации",
                                 variant_yes="Закрыть программу", variant_no="", callback=lambda: self.set_close())
            self.set_close()
        else:
            self.set_close()

    def on_config_is_broken(self, variants: QPushButton | None):
        """
        Напоминаение: on_config_is_broken вызовется быстрее, чем выполнится msg бокс
        :param variants:
        :return:
        """
        if variants is None:
            self.set_close()
            return

        text = variants.text()
        if text.find("Продолжить выполнение") != -1:
            self.load_with_error = True

        elif text.find("Закрыть программу") != -1:
            self.set_close()
        elif text.find("Сбросить конфиг по умолчанию") != -1:
            self.cconfig_unit.create_config_data()

            send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                             text="Файл конфигурации успешно сброшен.\n"
                                  "Программа должна быть перезагружена для удачной загрузки нового файла конфигурации.",
                             title="Сброс конфигурации",
                             variant_yes="Закрыть программу", variant_no="", callback=lambda: self.set_close())
            self.set_close()
        else:
            self.set_close()

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

    def show_test_window_no_window(self, test_type: TEST_TYPE, auto_test_launch: bool):
        """
            Разница с без окна и с окном в показе окна. Без показа тест автоматом проходит без открытия, но не для всех тестов.
            Для других тестов вызывается только окно, там где это нужно

            В тестах без открытия окна, а именно в автоматических, после авто завершения теста идёт вызов следующего,
            пока не закончится

        :param auto_test_launch:
        :param test_type:
        :return:
        """
        match test_type:
            case TEST_TYPE.TEST_SYSTEM_INFO:
                self.ctest_window_sys_info.set_default_string()
                btn_unit: CButtoms = CButtoms.get_unit_from_test_type(test_type)
                if btn_unit is not None:
                    current_test = self.ctest_process.is_test_launch()
                    if current_test != TEST_TYPE.TEST_NONE:
                        CSystemInfoWindow.clear_all_test_in_error_label()
                        result = self.ctest_window_sys_info.get_data()
                        if result:
                            data, on_test_count, is_test_passed_count, is_test_fail_string_check_count = result
                            is_test_passed = False
                            if on_test_count > 0:
                                if on_test_count - is_test_passed_count == 0 and is_test_fail_string_check_count == 0:
                                    btn_unit.set_btn_color_green()
                                    is_test_passed = True
                                else:
                                    btn_unit.set_btn_color_red()
                            else:
                                btn_unit.set_btn_color_red()
                            self.set_next_test(current_test, is_test_passed)
                        else:
                            btn_unit.set_btn_color_red()
                            self.set_next_test(current_test, False)

            case _:
                test_list = CTests.get_avalible_test_list()
                if test_type in test_list:
                    self.show_test_window_with_window(test_type, auto_test_launch)

    @classmethod
    def set_hidden_break_test_btn(cls, auto_test_launch: bool, btn_id: QPushButton):
        if isinstance(btn_id, QPushButton):
            if auto_test_launch:
                btn_id.setHidden(False)
                btn_id.setText("Прервать тесты")
            else:
                btn_id.setHidden(True)
                btn_id.setText("Прервать тест")

    def show_test_window_with_window(self, test_type: TEST_TYPE, auto_test_launch: bool):
        """
                   Разница с без окна и с окном в показе окна. Без показа тест автоматом проходит без открытия, но не для всех тестов.
                   Для других тестов вызывается только окно, там где это нужно

                   В тестах без открытия окна, а именно в автоматических, после авто завершения теста идёт вызов следующего,
                   пока не закончится

               :param auto_test_launch:
               :param test_type:
               :return:
               """
        match test_type:
            case TEST_TYPE.TEST_SYSTEM_INFO:
                self.ctest_window_sys_info.set_default_string()
                CSystemInfoWindow.clear_all_test_in_error_label()
                self.ctest_window_sys_info.show()
                self.set_hidden_break_test_btn(auto_test_launch,
                                               self.ctest_window_sys_info.ui.pushButton_all_test_break)

                self.ctest_window_sys_info.setFocus()
                result = self.ctest_window_sys_info.get_data()
                if result:
                    data, on_test_count, is_test_passed_count, is_test_fail_string_check_count = result
                    self.ctest_window_sys_info.load_data(data, on_test_count, is_test_passed_count,
                                                         is_test_fail_string_check_count)
                    return
                self.ctest_window_sys_info.load_data(None, 0, 0, 0)

            case TEST_TYPE.TEST_EXTERNAL_DISPLAY:
                result = self.ctest_window_external_display.window_show()

                if result != "True":
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text=f"Ошибка запуска теста '{CTests.get_test_name_from_test_type(test_type)}'!\n"
                                          f"Тест сообщил описание ошибки: '{result}'.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                    self.on_test_phb_fail(test_type, False)
                else:
                    self.set_hidden_break_test_btn(auto_test_launch,
                                                   self.ctest_window_external_display.ui.pushButton_all_test_break)

                    self.ctest_window_external_display.setFocus()

            case TEST_TYPE.TEST_FRONT_CAMERA:
                result = self.ctest_window_video_cam.window_show()

                if result != "True":
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text=f"Ошибка запуска теста '{CTests.get_test_name_from_test_type(test_type)}'!\n"
                                          f"Тест сообщил описание ошибки: '{result}'.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                    self.on_test_phb_fail(test_type, False)
                else:
                    self.set_hidden_break_test_btn(auto_test_launch,
                                                   self.ctest_window_video_cam.ui.pushButton_all_test_break)

                    self.ctest_window_video_cam.setFocus()

            case TEST_TYPE.TEST_SPEAKER_MIC:
                result = self.ctest_window_speaker_window.window_show(test_type)
                if result != "True":
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text=f"Ошибка запуска теста '{CTests.get_test_name_from_test_type(test_type)}'!\n"
                                          f"Тест сообщил описание ошибки: '{result}'.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                    self.on_test_phb_fail(test_type, False)
                else:
                    self.set_hidden_break_test_btn(auto_test_launch,
                                                   self.ctest_window_speaker_window.ui.pushButton_all_test_break)

                    self.ctest_window_speaker_window.setFocus()

            case TEST_TYPE.TEST_HEADSET_MIC:
                result = self.ctest_window_headset_window.window_show(test_type)
                if result != "True":
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text=f"Ошибка запуска теста '{CTests.get_test_name_from_test_type(test_type)}'!\n"
                                          f"Тест сообщил описание ошибки: '{result}'.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                    self.on_test_phb_fail(test_type, False)
                else:
                    self.set_hidden_break_test_btn(auto_test_launch,
                                                   self.ctest_window_headset_window.ui.pushButton_all_test_break)

                    self.ctest_window_headset_window.setFocus()

            case TEST_TYPE.TEST_HARDWARE_BTN:
                result = self.ctest_window_hardwarekeys.window_show()
                if result != "True":
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text=f"Ошибка запуска теста '{CTests.get_test_name_from_test_type(test_type)}'!\n"
                                          f"Тест сообщил описание ошибки: '{result}'.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                    self.on_test_phb_fail(test_type, False)
                else:
                    self.set_hidden_break_test_btn(auto_test_launch,
                                                   self.ctest_window_hardwarekeys.ui.pushButton_all_test_break)

                    self.ctest_window_hardwarekeys.setFocus()

            case TEST_TYPE.TEST_BRIGHTNESS:
                result = self.ctest_window_brightness.window_show()
                if result != "True":
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text=f"Ошибка запуска теста '{CTests.get_test_name_from_test_type(test_type)}'!\n"
                                          f"Тест сообщил описание ошибки: '{result}'.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                    self.on_test_phb_fail(test_type, False)
                else:
                    self.set_hidden_break_test_btn(auto_test_launch,
                                                   self.ctest_window_brightness.ui.pushButton_all_test_break)

                    self.ctest_window_brightness.setFocus()

            case TEST_TYPE.TEST_USB_DEVICES:
                result = self.ctest_window_usb_devices.window_show()
                if result != "True":
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text=f"Ошибка запуска теста '{CTests.get_test_name_from_test_type(test_type)}'!\n"
                                          f"Тест сообщил описание ошибки: '{result}'.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                    self.on_test_phb_fail(test_type, False)
                else:
                    self.set_hidden_break_test_btn(auto_test_launch,
                                                   self.ctest_window_usb_devices.ui.pushButton_all_test_break)

                    self.ctest_window_usb_devices.setFocus()

            case TEST_TYPE.TEST_PATTERNS:
                result = self.ctest_window_patterns.window_show()
                if result != "True":
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text=f"Ошибка запуска теста '{CTests.get_test_name_from_test_type(test_type)}'!\n"
                                          f"Тест сообщил описание ошибки: '{result}'.",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)

                    self.on_test_phb_fail(test_type, False)
                else:
                    self.set_hidden_break_test_btn(auto_test_launch,
                                                   self.ctest_window_patterns.ui.pushButton_all_test_break)

                    self.ctest_window_patterns.setFocus()

    def on_test_phb_break_all_test(self, test_type: TEST_TYPE):
        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.stop_test()
            self.ui.pushButton_launchall.setText("Запустить всё")

        self.close_current_test_window(test_type)

    def set_next_test(self, current_test: TEST_TYPE, test_passed: bool):
        next_test = self.ctest_process.get_next_test(current_test)

        if next_test is None:
            self.ctest_process.stop_test()
            self.ui.pushButton_launchall.setText("Тест завершён")

            if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:  # Проверяем, что нажата левая кнопка мыши
                self.call_power_off_bat()

            print("тест завершён так как дальше нету")
        else:
            print("Я ещё нашёл тесты")
            time.sleep(0.5)
            is_next = True
            # если какой то тест прервался по какой либо причине для лайна то остановим луп
            if self.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:
                if test_passed is False:
                    is_next = False
                    if current_test != TEST_TYPE.TEST_NONE:
                        self.ctest_process.stop_test()
            if is_next:
                self.ctest_process.switch_launch_test(next_test)
                self.show_test_window_no_window(next_test, True)

        if TestResultLabel.is_any_element():
            if not TestResultLabel.is_label_show():
                TestResultLabel.set_show_status(True)

    def on_test_phb_success(self, test_type: TEST_TYPE):

        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.set_result_test(current_test, TEST_RESULT.SUCCESS)
            self.set_next_test(current_test, True)

        if TestResultLabel.is_label_show():
            test_name = CTests.get_test_name_from_test_type(test_type)
            TestResultLabel.delete_test(test_name)
            if not TestResultLabel.is_any_element():
                TestResultLabel.set_show_status(False)

        btn_unit: CButtoms = CButtoms.get_unit_from_test_type(test_type)
        if btn_unit is not None:
            btn_unit.set_btn_color_green()

        self.close_current_test_window(test_type)

    def call_power_off_bat(self):
        bat_file_path = "content/bats/power_off.bat"
        self.run_external_bat(bat_file_path)
        return

    def call_time_sync_bat(self):
        bat_file_path = "content/bats/time_sync.bat"
        self.run_external_bat(bat_file_path)
        return

    def on_call_in_close_test_window(self, test_type: TEST_TYPE):
        # self.on_test_phb_break_all_test(test_type)
        pass

    def on_test_phb_fail(self, test_type: TEST_TYPE, is_window_open: bool = True):

        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.set_result_test(current_test, TEST_RESULT.FAIL)
            self.set_next_test(current_test, False)

        if not TestResultLabel.is_label_show():
            TestResultLabel.set_show_status(True)

        if test_type != TEST_TYPE.TEST_SYSTEM_INFO:
            # У сис инфо свои суб тесты отправляют строку
            test_name = CTests.get_test_name_from_test_type(test_type)
            TestResultLabel.add_text(test_name)

        btn_unit: CButtoms = CButtoms.get_unit_from_test_type(test_type)
        if btn_unit is not None:
            btn_unit.set_btn_color_red()
        if is_window_open:
            self.close_current_test_window(test_type)

    def close_current_test_window(self, current_test: TEST_TYPE):
        if current_test == TEST_TYPE.TEST_SYSTEM_INFO:
            self.ctest_window_sys_info.close()
        elif current_test == TEST_TYPE.TEST_EXTERNAL_DISPLAY:
            self.ctest_window_external_display.close()
        elif current_test == TEST_TYPE.TEST_FRONT_CAMERA:
            self.ctest_window_video_cam.close()
        elif current_test == TEST_TYPE.TEST_SPEAKER_MIC:
            self.ctest_window_speaker_window.close()
        elif current_test == TEST_TYPE.TEST_HEADSET_MIC:
            self.ctest_window_headset_window.close()
        elif current_test == TEST_TYPE.TEST_HARDWARE_BTN:
            self.ctest_window_hardwarekeys.close()
        elif current_test == TEST_TYPE.TEST_BRIGHTNESS:
            self.ctest_window_brightness.close()
        elif current_test == TEST_TYPE.TEST_USB_DEVICES:
            self.ctest_window_usb_devices.close()
        elif current_test == TEST_TYPE.TEST_PATTERNS:
            self.ctest_window_patterns.close()

    def closeEvent(self, e):
        e.accept()

    def set_close(self):
        if self.auto_test_line_time_launch is False:
            exit()


class CStringWindow(QMainWindow):
    """Показ строк для проверки систем инфо"""

    def __init__(self, main_window: MainWindow, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_StringWindow()
        self.ui.setupUi(self)

        # self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setWindowTitle(main_window.get_window_title())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Please select job type mode")
    parser.add_argument('command', type=str, help='Command for set select job type')

    args = parser.parse_args(["PROGRAM_FULL"])  # args = parser.parse_args(["PROGRAM_FULL"])
    pr_type = PROGRAM_JOB_TYPE.JOB_NORMAL
    if args.command == "PROGRAM_LINE":
        pr_type = PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE
        print("Program job: PROGRAM_JOB_TYPE.PROGRAM_LINE")
    elif args.command == "PROGRAM_FULL":
        pr_type = PROGRAM_JOB_TYPE.JOB_NORMAL
        print("Program job: PROGRAM_JOB_TYPE.JOB_NORMAL")
    else:
        print("Unknown command.")

    app = QApplication(argv)
    window = MainWindow(pr_type)
    window.show()

    exit(app.exec())

# def trash()
# if test_type == TEST_TYPE.TEST_SYSTEM_INFO:
#     print("wdfqeq")
#     print(CSystemInfo.get_drives_info())
#
#     print("\\nИнформация о жёстких дисках:")
#     for drive in CSystemInfo.get_drives_info():
#         print(f"Устройство: {drive['device']}, "
#               f"Точка монтирования: {drive['mountpoint']}, "
#               f"Общий размер: {drive['total'] / (1024 ** 3):.2f} ГБ, "
#               f"Использовано: {drive['used'] / (1024 ** 3):.2f} ГБ, "
#               f"Свободно: {drive['free'] / (1024 ** 3):.2f} ГБ")
#
#     memory_info = CSystemInfo.get_memory_info()
#     print("\\nИнформация о памяти:")
#     print(f"Всего: {memory_info['total'] / (1024 ** 3):.2f} ГБ, "
#           f"Доступно: {memory_info['available'] / (1024 ** 3):.2f} ГБ, "
#           f"Использовано: {memory_info['used'] / (1024 ** 3):.2f} ГБ")
#
#     bios_info = CSystemInfo.get_bios_info()
#     print("\\nИнформация о BIOS:")
#     print(f"Производитель: {bios_info['manufacturer']}, "
#           f"Версия: {bios_info['version']}, "
#           f"Серийный номер: {bios_info['serial_number']}, "
#           f"Дата выпуска: {bios_info['release_date']}")
#
#     print("Сетевые интерфейсы:")
#     network_interfaces = CSystemInfo.get_network_interfaces()
#     for interface, info in network_interfaces.items():
#         if info['ip_address'] is not None:  # Выводим только интерфейсы с IP
#             print(f"Название: {interface}")
#             print(f"  Тип подключения: {info['type']}")
#             print(f"  IP-адрес: {info['ip_address']}")
#             print(f"  Маска сети: {info['netmask']}")
#             print("")
#
#     print("Проверка соединения с LAN...")
#     if CSystemInfo.check_lan_connectivity():
#         print("Соединение с LAN установлено.")
#     else:
#         print("Нет соединения с LAN.")
#
#     print("\\nИнформация о CPU:")
#     print(CSystemInfo.get_cpu_info())
