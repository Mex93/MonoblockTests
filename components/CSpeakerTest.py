
from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon
from os.path import isfile as file_isfile

from pyaudio import PyAudio, paInt16
from wave import open as wave_open
from threading import Timer as threading_Timer
from threading import Thread as threading_Thread
from common import send_message_box, SMBOX_ICON_TYPE
from enuuuums import SPEAKER_PARAMS, TEST_TYPE, AUDIO_CHANNEL, AUDIO_STATUS, AUDIO_TEST_RECORD_STATE
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
    # Настройки Audio
    CHUNK = 1024
    FORMAT = paInt16
    CHANNELS = 1
    RATE = 44100
    sample_rate = 44.1e3

    def __init__(self, main_window, test_type: TEST_TYPE, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestAudioWindow()
        self.ui.setupUi(self)

        self.thread_id = None
        self.thread_start = False

        self.path_to_record_audio = "content/output_sound.wav"
        self.precord = PyAudio()
        self.record_state: AUDIO_TEST_RECORD_STATE = AUDIO_TEST_RECORD_STATE.STATE_NONE
        self.play_record_timer: threading_Timer | None = None
        self.stream: PyAudio | None = None
        self.all_channel_player = MediaPlayer(AUDIO_CHANNEL.CHANNEL_ALL)

        self.left_channel_player = MediaPlayer(AUDIO_CHANNEL.CHANNEL_LEFT)
        self.right_channel_player = MediaPlayer(AUDIO_CHANNEL.CHANNEL_RIGHT)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(test_type))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(test_type))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(test_type))

        self.ui.pushButton_record.clicked.connect(
            self.on_user_pressed_micro_record)

        self.ui.pushButton_left.clicked.connect(
            self.on_user_pressed_play_left)

        self.ui.pushButton_right.clicked.connect(
            self.on_user_pressed_play_right)

        self.ui.horizontalSlider_volume.valueChanged.connect(self.on_user_choise_volume)

        self.setWindowTitle(f'Меню теста')

    def on_user_pressed_micro_record(self):
        print("micro record")
        if self.record_state == AUDIO_TEST_RECORD_STATE.STATE_NONE:
            self.record_state = AUDIO_TEST_RECORD_STATE.STATE_RECORD
            self.set_record_btn_current_status()
            self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_RIGHT, AUDIO_STATUS.STATUS_STOP)
            self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_LEFT, AUDIO_STATUS.STATUS_STOP)
            MediaPlayer.stop_any_play()
            if not self.thread_start:
                self.thread_id = threading_Thread(target=self.start_record_script)
                self.thread_id.start()
                self.thread_start = True

    def start_record_script(self):
        try:
            frames = list()
            self.stream = self.precord.open(format=self.FORMAT, channels=self.CHANNELS,
                                            rate=self.RATE, input=True,
                                            )

            self.stream.start_stream()
            for i in range(0, int(self.RATE / self.CHUNK * 3)):
                data = self.stream.read(self.CHUNK)
                frames.append(data)

            self.stream.stop_stream()
            self.stream.close()

            if self.record_state == AUDIO_TEST_RECORD_STATE.STATE_RECORD:
                wf = wave_open(self.path_to_record_audio, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.precord.get_sample_size(self.FORMAT))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
                wf.close()
                self.record_state = AUDIO_TEST_RECORD_STATE.STATE_PLAY
                self.set_record_btn_current_status()

                self.play_record_timer = threading_Timer(2.5, self.on_stop_record_play_time)
                self.play_record_timer.start()

                self.all_channel_player.start_play()
                print("я отработал (поток в рекорде)")

        except OSError:
            send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                             text="Нет источника записи звука!\n",
                             title="Внимание!",
                             variant_yes="Закрыть", variant_no="", callback=None)

        return

    def stop_record_stream(self):
        """Если запущен поток аудиозаписи
            Отключен потому что вызывает конфиликт в отдельном потоке.
        """
        pass
        # if self.stream is not None:
        #     self.stream.stop_stream()
        #     self.stream.close()
        #     self.stream = None

    def on_stop_record_play_time(self):
        """Вызов после колнца таймера"""
        self.set_default_record_play()
        self.stop_record_stream()
        self.set_record_btn_current_status()
        self.all_channel_player.stop_play()

    def set_default_record_play(self):
        """Сброс записи и таймера"""
        self.record_state = AUDIO_TEST_RECORD_STATE.STATE_NONE
        if self.play_record_timer is not None:
            if self.play_record_timer.is_alive():
                self.play_record_timer.cancel()
            self.play_record_timer = None

    def set_record_btn_current_status(self):
        icon = None
        match self.record_state:
            case AUDIO_TEST_RECORD_STATE.STATE_NONE:
                icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioInputMicrophone))
                self.ui.pushButton_record.setText("Записать")
            case AUDIO_TEST_RECORD_STATE.STATE_RECORD:
                icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaRecord))
                self.ui.pushButton_record.setText("Записываю...")
            case AUDIO_TEST_RECORD_STATE.STATE_PLAY:
                icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeMedium))
                self.ui.pushButton_record.setText("Воспроизвожу...")
        if icon:
            self.ui.pushButton_record.setIcon(icon)

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

    def window_show(self, test_type: TEST_TYPE) -> bool:
        patch_left = CSpeakerTest.get_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_LEFT)
        patch_right = CSpeakerTest.get_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_RIGHT)
        if None not in (patch_left, patch_right):
            if isinstance(patch_left, str) and isinstance(patch_right, str):
                if patch_left.find("content") != -1 and patch_right.find("content") != -1:
                    if patch_left.find(".mp3") != -1 and patch_right.find(".mp3") != -1:
                        if file_isfile(patch_left) and file_isfile(patch_right):
                            self.kill_thread_or_set_default()
                            self.left_channel_player.load_file(patch_left)
                            self.right_channel_player.load_file(patch_right)
                            self.all_channel_player.load_file(self.path_to_record_audio)
                            self.all_channel_player.set_volume(1.0)
                            self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_RIGHT, AUDIO_STATUS.STATUS_STOP)
                            self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_LEFT, AUDIO_STATUS.STATUS_STOP)
                            self.set_record_btn_current_status()
                            self.left_channel_player.set_volume(1.0)  # * .01
                            self.right_channel_player.set_volume(1.0)  # * .01
                            self.ui.horizontalSlider_volume.setValue(100)
                            if test_type == TEST_TYPE.TEST_SPEAKER_MIC:
                                self.ui.groupBox.setTitle("Тест динамиков и микрофона")
                            elif test_type == TEST_TYPE.TEST_HEADSET_MIC:
                                self.ui.groupBox.setTitle("Тест наушников и микрофона(В наушниках)")
                            self.show()
                            return True

    def kill_thread_or_set_default(self):
        if self.thread_start:
            self.thread_id.join()
            self.thread_start = False
            self.thread_id = None

    def closeEvent(self, e):
        self.kill_thread_or_set_default()
        MediaPlayer.stop_any_play()

        self.stop_record_stream()
        self.set_default_record_play()

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
