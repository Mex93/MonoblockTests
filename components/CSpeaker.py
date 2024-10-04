from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon

from enuuuums import SPEAKER_PARAMS, TEST_TYPE, AUDIO_CHANNEL, AUDIO_STATUS
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

        self.left_channel_player = MediaPlayer(AUDIO_CHANNEL.CHANNEL_LEFT)
        self.right_channel_player = MediaPlayer(AUDIO_CHANNEL.CHANNEL_RIGHT)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_SPEAKER_MIC))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_SPEAKER_MIC))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_SPEAKER_MIC))

        self.ui.pushButton_play.clicked.connect(
            self.on_user_pressed_micro_play)

        self.ui.pushButton_record.clicked.connect(
            self.on_user_pressed_micro_record)

        self.ui.pushButton_left.clicked.connect(
            self.on_user_pressed_play_left)

        self.ui.pushButton_right.clicked.connect(
            self.on_user_pressed_play_right)

        self.ui.horizontalSlider_volume.valueChanged.connect(self.on_user_choise_volume)

        self.setWindowTitle(f'Меню теста')

    def on_user_choise_volume(self):
        current_slider_pos = self.ui.horizontalSlider_volume.value()
        self.left_channel_player.set_volume(current_slider_pos * .01)
        self.right_channel_player.set_volume(current_slider_pos * .01)

    def set_audio_test_icon(self, channel_type: AUDIO_CHANNEL, audio_status: AUDIO_STATUS):
        if channel_type == AUDIO_CHANNEL.CHANNEL_LEFT:
            icon = None
            if audio_status == AUDIO_STATUS.STATUS_PLAY:
                icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeHigh))
            elif audio_status == AUDIO_STATUS.STATUS_STOP:
                icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeMuted))
            if icon:
                self.ui.pushButton_left.setIcon(icon)

        elif channel_type == AUDIO_CHANNEL.CHANNEL_RIGHT:
            icon = None
            if audio_status == AUDIO_STATUS.STATUS_PLAY:
                icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeHigh))
            elif audio_status == AUDIO_STATUS.STATUS_STOP:
                icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeMuted))
            if icon:
                self.ui.pushButton_right.setIcon(icon)

    def on_user_pressed_micro_play(self):
        print("micro play")

    def on_user_pressed_micro_record(self):
        print("micro record")

    def on_user_pressed_play_left(self):
        print("play left")
        current_channel = MediaPlayer.is_any_play()
        if current_channel is not None:
            if current_channel == AUDIO_CHANNEL.CHANNEL_LEFT:
                self.left_channel_player.stop_play()
                self.set_audio_test_icon(current_channel, AUDIO_STATUS.STATUS_STOP)
                return
            else:
                self.set_audio_test_icon(current_channel, AUDIO_STATUS.STATUS_STOP)

        self.left_channel_player.start_play()
        self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_LEFT, AUDIO_STATUS.STATUS_PLAY)

    def on_user_pressed_play_right(self):
        print("play right")

        current_channel = MediaPlayer.is_any_play()
        if current_channel is not None:
            if current_channel == AUDIO_CHANNEL.CHANNEL_RIGHT:
                self.right_channel_player.stop_play()
                self.set_audio_test_icon(current_channel, AUDIO_STATUS.STATUS_STOP)
                return
            else:
                self.set_audio_test_icon(current_channel, AUDIO_STATUS.STATUS_STOP)

        self.right_channel_player.start_play()
        self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_RIGHT, AUDIO_STATUS.STATUS_PLAY)

    def window_show(self) -> bool:
        patch_left = CSpeakerTest.get_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_LEFT)
        patch_right = CSpeakerTest.get_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_RIGHT)
        if None not in (patch_left, patch_right):
            if isinstance(patch_left, str) and isinstance(patch_right, str):
                if patch_left.find("content") != -1 and patch_right.find("content") != -1:
                    if patch_left.find(".mp3") != -1 or patch_right.find(".mp3") != -1:
                        self.left_channel_player.load_file(patch_left)
                        self.right_channel_player.load_file(patch_right)
                        self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_RIGHT, AUDIO_STATUS.STATUS_STOP)
                        self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_LEFT, AUDIO_STATUS.STATUS_STOP)

                        self.left_channel_player.set_volume(1.0)  # * .01
                        self.right_channel_player.set_volume(1.0)  # * .01
                        self.ui.horizontalSlider_volume.setValue(100)
                        self.show()
                        return True

    def closeEvent(self, e):
        MediaPlayer.stop_any_play()
        e.accept()


class MediaPlayer:
    __player_units = list()

    def __init__(self, channel_type: AUDIO_CHANNEL):
        self.__player = QMediaPlayer()
        self.__audio_output = QAudioOutput()
        self.__player.setAudioOutput(self.__audio_output)
        self.__channel_type = channel_type
        MediaPlayer.__player_units.append([self.__player, channel_type])

    def set_volume(self, volume: float):
        self.__audio_output.setVolume(volume)

    def get_volume(self) -> float:
        return self.__audio_output.volume()

    def get_audio_unit(self) -> QAudioOutput:
        return self.__audio_output

    def get_unit(self) -> QMediaPlayer:
        return self.__player

    def is_play(self) -> bool:
        if self.__player.isPlaying():
            return True

    def stop_play(self):
        if self.is_play():
            self.__player.stop()

    def start_play(self):
        self.__player.play()

    def load_file(self, file_patch):
        self.__player.setSource(QUrl.fromLocalFile(file_patch))

    @classmethod
    def stop_any_play(cls) -> None:
        for player_list in cls.__player_units:
            player, channel = player_list
            if player.isPlaying():
                player.stop()

    @classmethod
    def is_any_play(cls) -> AUDIO_CHANNEL | None:
        for player_list in cls.__player_units:
            player, channel = player_list
            if player.isPlaying():
                player.stop()
                return channel
