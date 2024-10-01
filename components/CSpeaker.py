from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl, Qt

from enuuuums import SPEAKER_PARAMS, TEST_TYPE
from ui.test_speaker_audio import Ui_TestAudioWindow


class CSpeakerTest:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: SPEAKER_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: SPEAKER_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})


class CSpeakerTestWindow(QMainWindow):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestAudioWindow()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_SPEAKER_MIC))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_SPEAKER_MIC))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_SPEAKER_MIC))

        self.setWindowTitle(f'Меню теста')

    def window_show(self) -> bool:
        patch_left = CSpeakerTest.get_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_LEFT)
        patch_right = CSpeakerTest.get_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_RIGHT)
        if None not in (patch_left, patch_right):
            if isinstance((patch_left, patch_right), str):
                if patch_left.find("content") != -1 and patch_right.find("content") != -1:
                    if patch_left.find(".mp3") != -1 or patch_right.find(".mp3") != -1:
                        self.show()
                        return True

    def closeEvent(self, e):
        e.accept()
