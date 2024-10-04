from sys import argv, exit

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QUrl, Qt

from ui.untitled import Ui_MainWindow
from ui.get_check_string_window import Ui_MainWindow as Ui_StringWindow
from common import send_message_box, SMBOX_ICON_TYPE, get_about_text, get_rules_text

from components.CConfig import CNewConfig, CParameters, BLOCKS_DATA, SYS_INFO_PARAMS, CONFIG_PARAMS
from components.CTests import CTests, TEST_TYPE, CTestProcess, TEST_RESULT
from components.CConfig_Main import CMainConfig
from components.CSystemInfo import CSystemInfo, CSystemInfoWindow
from components.CExternalDisplay import CExternalDisplayWindow, CExternalDisplay, EXTERNAL_DISPLAY_PARAMS
from components.CSpeaker import CSpeakerTestWindow, CSpeakerTest, SPEAKER_PARAMS
from components.CButtons import CButtoms


# pyside6-uic .\ui\untitled.ui -o .\ui\untitled.py
# pyside6-uic .\ui\get_check_string_window.ui -o .\ui\get_check_string_window.py
# pyside6-uic .\ui\test_sys_info.ui -o .\ui\test_sys_info.py
# pyside6-uic .\ui\test_external_display.ui -o .\ui\test_external_display.py
# pyside6-uic .\ui\test_speaker_audio.ui -o .\ui\test_speaker_audio.py
# pyside6-rcc .\ui\res.qrc -o .\ui\res_rc.py
# Press the green button in the gutter to run the script.


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__base_program_version = "0.1"  # Менять при каждом обновлении любой из подпрограмм

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QFontDatabase.addApplicationFont("designs/Iosevka Bold.ttf")
        self.setWindowTitle(f'Тестирование моноблоков Kvant 2024 v0.1a')

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
        self.ctest_process = CTestProcess()

        self.cmain_window_get_string = CStringWindow(self)
        self.ctest_window_sys_info = CSystemInfoWindow(self)
        self.ctest_window_external_display = CExternalDisplayWindow(self)
        self.ctest_window_speaker_window = CSpeakerTestWindow(self, TEST_TYPE.TEST_SPEAKER_MIC)
        self.ctest_window_headset_window = CSpeakerTestWindow(self, TEST_TYPE.TEST_HEADSET_MIC)

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

    def get_window_title(self) -> str:
        return self.windowTitle()

    def on_user_pressed_check_string(self):
        result = self.ctest_window_sys_info.get_data()
        string_window = self.cmain_window_get_string
        if result:
            data, fail_tests_count, all_used_test_count = self.ctest_window_sys_info.get_data()
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

                string_window.ui.textBrowser_set_string.append(f"Всего тестов активировано: {all_used_test_count}\n"
                                                               f"Тестов провалено: {fail_tests_count}\n"
                                                               f"Тестов успешно: {all_used_test_count - fail_tests_count}\n")

                string_window.ui.textBrowser_set_string.append("Примечание: Строка проверки копируется полностью в конфиг")
        else:
            string_window.ui.textBrowser_set_string.append("Все тесты отключены!\n")
        string_window.show()

    def on_user_pressed_start_all_test(self):
        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.stop_test()

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
        self.show_test_window_no_window(first_test)

    def on_user_pressed_clear_all_test(self):
        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.stop_test()

        CButtoms.set_buttoms_default_color()

    def on_user_presed_launch_test(self, test_type: TEST_TYPE):
        print(f"Запущен тест: {test_type}")

        if test_type == TEST_TYPE.TEST_SYSTEM_INFO:
            self.show_test_window_with_window(test_type)

        elif test_type == TEST_TYPE.TEST_EXTERNAL_DISPLAY:
            self.show_test_window_with_window(test_type)

        elif test_type == TEST_TYPE.TEST_SPEAKER_MIC:
            self.show_test_window_with_window(test_type)

        elif test_type == TEST_TYPE.TEST_HEADSET_MIC:
            self.show_test_window_with_window(test_type)

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
                CExternalDisplay.set_test_stats(CONFIG_PARAMS.DISPLAY_RESOLUTION, "full-screen")
                # send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_WARNING,
                #                  text="Ошибка в обработке размера окна из конфига!\n"
                #                       f"Ошибка в размере: '{display_resolution}'!\n\n"
                #                       f"Окна для тестов будут открываться в стандартном разрешении, "
                #                       f"заданном при проектировании",
                #                  title="Внимание!",
                #                  variant_yes="Закрыть", variant_no="", callback=None)

            config_human_name = self.cconfig_unit.get_config_value(BLOCKS_DATA.PROGRAM_SETTING,
                                                                   CONFIG_PARAMS.CONFIG_NAME)

            self.ui.label_monoblock_config_name.setText(f"Тест моноблоков: {config_human_name}")
            self.main_config.save_last_config(text)

            # LOAD
            # Sys Info
            # check
            CSystemInfo.set_test_stats(SYS_INFO_PARAMS.SYS_INFO_TEST_USED,
                                       self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                          SYS_INFO_PARAMS.SYS_INFO_TEST_USED))

            CSystemInfo.set_test_stats(SYS_INFO_PARAMS.BIOS_CHECK,
                                       self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                          SYS_INFO_PARAMS.BIOS_CHECK))
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

            CSystemInfo.set_test_stats(SYS_INFO_PARAMS.SYS_INFO_NOT_WINDOW_TEST,
                                       self.cconfig_unit.get_config_value(BLOCKS_DATA.SYS_INFO_TEST,
                                                                          SYS_INFO_PARAMS.SYS_INFO_NOT_WINDOW_TEST))

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

            # External display
            # check
            CExternalDisplay.set_test_stats(EXTERNAL_DISPLAY_PARAMS.EXTD_TEST_USED,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST,
                                                                               EXTERNAL_DISPLAY_PARAMS.EXTD_TEST_USED))
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
            # string
            CSpeakerTest.set_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_LEFT,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                               SPEAKER_PARAMS.AUDIO_PATCH_LEFT))
            CSpeakerTest.set_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_RIGHT,
                                            self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                               SPEAKER_PARAMS.AUDIO_PATCH_RIGHT))
            CSpeakerTest.set_test_stats(SPEAKER_PARAMS.HEADSET_TEST_USED,
                                        self.cconfig_unit.get_config_value(BLOCKS_DATA.SPEAKER_TEST,
                                                                           SPEAKER_PARAMS.HEADSET_TEST_USED))

            CButtoms.set_clear_callbacks_for_all()

            block_datas = CTests.get_config_block_data()
            btn_index = 0
            for index, block_data in enumerate(block_datas):
                bname, btype = block_datas[index]
                if btype == TEST_TYPE.TEST_SYSTEM_INFO:
                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.SYS_INFO_TEST_USED) is True:
                        btn_unit = CButtoms.get_unit_from_index(btn_index)
                        btn_unit.set_callback(btype, self.on_user_presed_launch_test)
                        btn_unit.set_name(bname)
                        btn_unit.set_enabled(True)
                        btn_unit.set_hidden(False)
                        btn_index += 1
                elif btype == TEST_TYPE.TEST_EXTERNAL_DISPLAY:
                    if CExternalDisplay.get_test_stats(EXTERNAL_DISPLAY_PARAMS.EXTD_TEST_USED) is True:
                        btn_unit = CButtoms.get_unit_from_index(btn_index)
                        btn_unit.set_callback(btype, self.on_user_presed_launch_test)
                        btn_unit.set_name(bname)
                        btn_unit.set_enabled(True)
                        btn_unit.set_hidden(False)
                        btn_index += 1
                elif btype == TEST_TYPE.TEST_SPEAKER_MIC:
                    if CSpeakerTest.get_test_stats(SPEAKER_PARAMS.SPEAKER_TEST_USED) is True:
                        btn_unit = CButtoms.get_unit_from_index(btn_index)
                        btn_unit.set_callback(btype, self.on_user_presed_launch_test)
                        btn_unit.set_name(bname)
                        btn_unit.set_enabled(True)
                        btn_unit.set_hidden(False)
                        btn_index += 1

                elif btype == TEST_TYPE.TEST_HEADSET_MIC:
                    if CSpeakerTest.get_test_stats(SPEAKER_PARAMS.HEADSET_TEST_USED) is True:
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

    def show_test_window_no_window(self, test_type: TEST_TYPE):
        """
            Разница с без окна и с окном в показе окна. Без показа тест автоматом проходит без открытия, но не для всех тестов.
            Для других тестов вызывается только окно, там где это нужно

            В тестах без открытия окна, а именно в автоматических, после авто завершения теста идёт вызов следующего,
            пока не закончится

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
                        result = self.ctest_window_sys_info.get_data()
                        if result:
                            data, fail_tests_count, all_used_test_count = self.ctest_window_sys_info.get_data()
                            if all_used_test_count > 0:
                                if fail_tests_count == 0:
                                    btn_unit.set_btn_color_green()
                                else:
                                    btn_unit.set_btn_color_red()
                            else:
                                btn_unit.set_btn_color_red()
                            self.set_next_test(current_test)
                        else:
                            btn_unit.set_btn_color_red()
                            self.set_next_test(current_test)

            case TEST_TYPE.TEST_EXTERNAL_DISPLAY:
                self.show_test_window_with_window(test_type)
            case TEST_TYPE.TEST_SPEAKER_MIC:
                self.show_test_window_with_window(test_type)
            case TEST_TYPE.TEST_HEADSET_MIC:
                self.show_test_window_with_window(test_type)

    def show_test_window_with_window(self, test_type: TEST_TYPE):
        """
                   Разница с без окна и с окном в показе окна. Без показа тест автоматом проходит без открытия, но не для всех тестов.
                   Для других тестов вызывается только окно, там где это нужно

                   В тестах без открытия окна, а именно в автоматических, после авто завершения теста идёт вызов следующего,
                   пока не закончится

               :param test_type:
               :return:
               """
        match test_type:
            case TEST_TYPE.TEST_SYSTEM_INFO:
                self.ctest_window_sys_info.set_default_string()

                self.ctest_window_sys_info.show()
                self.ctest_window_sys_info.setFocus()
                result = self.ctest_window_sys_info.get_data()
                if result:
                    data, fail_tests_count, all_used_test_count = result
                    self.ctest_window_sys_info.load_data(data, fail_tests_count, all_used_test_count)
                    return
                self.ctest_window_sys_info.load_data(None, 0, 0)

            case TEST_TYPE.TEST_EXTERNAL_DISPLAY:
                result = self.ctest_window_external_display.window_show()
                if not result:
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text="Ошибка в файле конфигурации для видео!\n"
                                          "Один или несколько параметров ошибочны!\n\n"
                                     ,
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                else:
                    self.ctest_window_external_display.setFocus()

            case TEST_TYPE.TEST_SPEAKER_MIC:
                result = self.ctest_window_speaker_window.window_show(test_type)
                if not result:
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text="Ошибка в файле конфигурации для аудио!\n"
                                          "Один или несколько параметров ошибочны!\n\n",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                else:
                    self.ctest_window_speaker_window.setFocus()

            case TEST_TYPE.TEST_HEADSET_MIC:
                result = self.ctest_window_headset_window.window_show(test_type)
                if not result:
                    send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                     text="Ошибка в файле конфигурации для аудио в наушниках!\n"
                                          "Один или несколько параметров ошибочны!\n\n",
                                     title="Внимание!",
                                     variant_yes="Закрыть", variant_no="", callback=None)
                else:
                    self.ctest_window_headset_window.setFocus()

    def on_test_phb_break_all_test(self, test_type: TEST_TYPE):
        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.stop_test()

        self.close_current_test_window(test_type)

    def set_next_test(self, current_test: TEST_TYPE):
        next_test = self.ctest_process.get_next_test(current_test)

        if next_test is None:
            self.ctest_process.stop_test()
            print("тест завершён так как дальше нету")
        else:
            print("Я ещё нашёл тесты")
            self.ctest_process.switch_launch_test(next_test)

            self.show_test_window_no_window(next_test)

    def on_test_phb_success(self, test_type: TEST_TYPE):

        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.set_result_test(current_test, TEST_RESULT.SUCCESS)
            self.set_next_test(current_test)

        btn_unit: CButtoms = CButtoms.get_unit_from_test_type(test_type)
        if btn_unit is not None:
            btn_unit.set_btn_color_green()

        self.close_current_test_window(test_type)

    def on_test_phb_fail(self, test_type: TEST_TYPE):

        current_test = self.ctest_process.is_test_launch()
        if current_test != TEST_TYPE.TEST_NONE:
            self.ctest_process.set_result_test(current_test, TEST_RESULT.FAIL)
            self.set_next_test(current_test)

        btn_unit: CButtoms = CButtoms.get_unit_from_test_type(test_type)
        if btn_unit is not None:
            btn_unit.set_btn_color_red()

        self.close_current_test_window(test_type)

    def close_current_test_window(self, current_test: TEST_TYPE):
        if current_test == TEST_TYPE.TEST_SYSTEM_INFO:
            self.ctest_window_sys_info.close()
        elif current_test == TEST_TYPE.TEST_EXTERNAL_DISPLAY:
            self.ctest_window_external_display.close()
        elif current_test == TEST_TYPE.TEST_SPEAKER_MIC:
            self.ctest_window_speaker_window.close()
        elif current_test == TEST_TYPE.TEST_HEADSET_MIC:
            self.ctest_window_headset_window.close()

    def closeEvent(self, e):
        e.accept()

    @staticmethod
    def set_close():
        exit()


class CStringWindow(QMainWindow):
    def __init__(self, main_window: MainWindow, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_StringWindow()
        self.ui.setupUi(self)

        # self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setWindowTitle(main_window.get_window_title())


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
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
