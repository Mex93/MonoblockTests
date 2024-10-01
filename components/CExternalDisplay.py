from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimedia import QMediaPlayer
import PySide6.QtCore as WindowModality
from PySide6.QtCore import QUrl, Qt

import subprocess

from enuuuums import EXTERNAL_DISPLAY_PARAMS, TEST_TYPE
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

    def window_show(self) -> bool:
        patch = CExternalDisplay.get_test_stats(EXTERNAL_DISPLAY_PARAMS.VIDEO_PATCH)
        if patch is not None:
            if isinstance(patch, str):
                if patch.find("content") != -1:
                    if patch.find(".mp4") != -1 or patch.find(".avi") != -1:
                        CExternalDisplay.setup_window_for_dual_monitor()
                        self.player.setSource(QUrl.fromLocalFile(patch))
                        self.player.play()
                        self.show()

                        return True

    def closeEvent(self, e):
        self.player.stop()
        CExternalDisplay.setup_window_for_single_monitor()
        e.accept()
