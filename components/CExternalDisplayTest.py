import time

from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl, Qt

from os.path import isfile as file_isfile
import subprocess
from screeninfo import get_monitors
from components.CSpeakerTest import AudioChannelHookEvent
from enuuuums import EXTERNAL_DISPLAY_PARAMS, TEST_TYPE, CONFIG_PARAMS
from ui.test_external_display import Ui_TestExternalDisplayWindow


class CExternalDisplay:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: EXTERNAL_DISPLAY_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: EXTERNAL_DISPLAY_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})

    @classmethod
    def is_monitor_mode_avalible(cls, mode: str) -> bool:
        imodes = ["internal", "extend", "clone", "external"]
        if mode in imodes:
            return True

    @classmethod
    def get_monitor_mode_avalible(cls) -> list:
        return ["internal", "extend", "clone", "external"]

    @classmethod
    def setup_window_for_dual_monitor(cls):
        wmode = CExternalDisplay.get_test_stats(EXTERNAL_DISPLAY_PARAMS.WINDOW_SWITCH_TO)
        if wmode is not None:
            if cls.is_monitor_mode_avalible(wmode):
                subprocess.Popen(f'displayswitch /{wmode}')

    @classmethod
    def setup_window_for_single_monitor(cls):
        wmode = CExternalDisplay.get_test_stats(EXTERNAL_DISPLAY_PARAMS.WINDOW_DEFAULT)
        if wmode is not None:
            if cls.is_monitor_mode_avalible(wmode):
                subprocess.Popen(f'displayswitch /{wmode}')


class CExternalDisplayWindow(QMainWindow):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestExternalDisplayWindow()
        self.ui.setupUi(self)
        self.center()
        # self.ui.graphicsView
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.ui.videobox)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_EXTERNAL_DISPLAY))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_EXTERNAL_DISPLAY))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_EXTERNAL_DISPLAY))

        self.setWindowTitle(f'Меню теста')

        self.audio_hook = AudioChannelHookEvent(self.on_audio_channel_switch)

    def on_audio_channel_switch(self, old_id: QAudioOutput.device, new_id: QAudioOutput.device):
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

    def center(self):
        """
        Центрируем экран
        :return:
        """
        # Получаем размеры экрана
        screen = self.screen().availableGeometry()
        screen_center = screen.center()

        # Получаем текущие размеры окна
        window_rect = self.frameGeometry()

        # Устанавливаем новое положение окна по центру экрана

        window_rect.moveCenter(screen_center)
        # self.move(window_rect.topLeft())

    @classmethod
    def check_second_monitor(cls) -> bool:
        monitors = get_monitors()
        # [Monitor(x=0, y=0, width=3440, height=1440, width_mm=797,
        # height_mm=333, name='\\\\.\\DISPLAY1', is_primary=True)]
        if len(monitors) > 1:
            return True
        return False

    def window_show(self) -> str:
        patch = CExternalDisplay.get_test_stats(EXTERNAL_DISPLAY_PARAMS.VIDEO_PATCH)
        if patch is None:
            return "Путь до файла с видео пустой"

        if not isinstance(patch, str):
            return "Путь до файла с видео должен быть строкой"
        if patch.find("content") == -1:
            return "В строке пути до файла с видео не найдено название папки 'content'"

        if patch.find(".mp4") == -1 and patch.find(".avi") == -1:
            return "Указан неверный формат видео файла. Доступно .avi, .mp4"

        if not file_isfile(patch):
            return "Указанный видео-файл не найден в папке 'content'"

        if not self.check_second_monitor():
            return "Не найден второй монитор"

        CExternalDisplay.setup_window_for_dual_monitor()
        time.sleep(2.0)
        self.player.setSource(QUrl.fromLocalFile(patch))

        # потому что в общей куче конфигов
        # если задан список, то значит у нас есть указанные размеры
        # если строка то открываем на полный экран
        display_resolution_list = CExternalDisplay.get_test_stats(CONFIG_PARAMS.DISPLAY_RESOLUTION)
        self.player.play()
        if isinstance(display_resolution_list, str):
            self.showMaximized()
        else:
            self.show()

        return "True"

    def closeEvent(self, e):
        self.player.stop()
        CExternalDisplay.setup_window_for_single_monitor()
        time.sleep(2.0)
        e.accept()
