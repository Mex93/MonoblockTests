from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl, Qt, QThread, Signal, QTimer
from PySide6.QtGui import QIcon
from os.path import isfile as file_isfile
from common import send_message_box, SMBOX_ICON_TYPE
from pyaudio import PyAudio, paInt16
from wave import open as wave_open
from enuuuums import SPEAKER_PARAMS, TEST_TYPE, AUDIO_CHANNEL, AUDIO_STATUS, AUDIO_TEST_RECORD_STATE, AUDIO_TEST_STEP
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
        self.test_type = test_type
        self.path_to_record_audio = "content/output_sound.wav"
        self.precord = PyAudio()
        self.record_state: AUDIO_TEST_RECORD_STATE = AUDIO_TEST_RECORD_STATE.STATE_NONE
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

        self.ui.pushButton_repeat.clicked.connect(
            self.on_user_pressed_repeat_test)

        self.ui.pushButton_start_test.clicked.connect(
            self.on_user_pressed_start_test_loop)

        self.ui.horizontalSlider_volume.valueChanged.connect(self.on_user_choise_volume)

        self.RecordAudioWorker = RecordWorker(self)
        self.RecordAudioWorker.update_label.connect(self.RecordAudioWorker.update_label)

        self.play_record_timer_count = 0
        self.play_record_timer = QTimer()
        self.play_record_timer.timeout.connect(self.on_update_record_timer)

        self.setWindowTitle(f'Меню теста')

    def on_user_pressed_start_test_loop(self):
        if not AutoTest.is_auto_test_start():
            self.show_result_btns(False)
            MediaPlayer.stop_any_play()

            self.stop_record_stream()
            self.set_default_record_play()

            AutoTest.start_test()
            AutoTest.set_step(4, AUDIO_TEST_STEP.STEP_LEFT_CHANNEL)
            self.set_auto_test_enabled_ui_event(True)

            self.on_user_pressed_play_left()
        else:
            current_test = AutoTest.get_current_auto_test()
            if current_test == AUDIO_TEST_STEP.STEP_LEFT_CHANNEL:
                AutoTest.set_step(4, AUDIO_TEST_STEP.STEP_RIGHT_CHANNEL)
                self.on_user_pressed_play_right()
            elif current_test == AUDIO_TEST_STEP.STEP_RIGHT_CHANNEL:
                AutoTest.set_step(4, AUDIO_TEST_STEP.STEP_RECORD)
                self.on_user_pressed_micro_record()
            elif current_test == AUDIO_TEST_STEP.STEP_RECORD:
                return
                # AutoTest.set_step(4, AUDIO_TEST_STEP.STEP_PLAY)
            elif current_test == AUDIO_TEST_STEP.STEP_PLAY:
                AutoTest.stop()
                self.set_auto_test_enabled_ui_event(False)
                self.show_result_btns(True)

    def on_update_record_timer(self):
        if self.record_state == AUDIO_TEST_RECORD_STATE.STATE_PLAY:
            if self.play_record_timer_count > 0:
                self.play_record_timer_count -= 1
            if self.play_record_timer_count == 0:
                self.on_stop_record_play_time()
                self.show_result_btns(True)

        current_test = AutoTest.get_current_auto_test()
        if current_test == AUDIO_TEST_STEP.STEP_LEFT_CHANNEL:
            result = AutoTest.set_update_time_count()
            if result:  # выполнился
                AutoTest.set_step(4, AUDIO_TEST_STEP.STEP_RIGHT_CHANNEL)
                self.on_user_pressed_play_right()
        elif current_test == AUDIO_TEST_STEP.STEP_RIGHT_CHANNEL:
            result = AutoTest.set_update_time_count()
            if result:  # выполнился
                AutoTest.set_step(7, AUDIO_TEST_STEP.STEP_RECORD)
                self.on_user_pressed_micro_record()
        elif current_test == AUDIO_TEST_STEP.STEP_RECORD:
            result = AutoTest.set_update_time_count()
            if result:  # выполнился
                AutoTest.set_step(4, AUDIO_TEST_STEP.STEP_PLAY)
        elif current_test == AUDIO_TEST_STEP.STEP_PLAY:
            result = AutoTest.set_update_time_count()
            if result:  # выполнился
                AutoTest.stop()
                self.show_result_btns(True)
                self.set_auto_test_enabled_ui_event(False)

    def set_auto_test_enabled_ui_event(self, status: bool):
        if status:  # запустить
            self.ui.pushButton_start_test.setText("Запущен тест...\nДалее ->")
            self.ui.pushButton_record.setDisabled(True)
            self.ui.pushButton_right.setDisabled(True)
            self.ui.pushButton_left.setDisabled(True)
        else:
            self.ui.pushButton_start_test.setText("Запустить")
            self.ui.pushButton_record.setDisabled(False)
            self.ui.pushButton_right.setDisabled(False)
            self.ui.pushButton_left.setDisabled(False)

    def on_user_pressed_micro_record(self):
        print("micro record")
        if self.record_state == AUDIO_TEST_RECORD_STATE.STATE_NONE:
            if self.is_any_record_avalible() and self.is_record_avalible_open():
                self.record_state = AUDIO_TEST_RECORD_STATE.STATE_RECORD
                self.set_record_btn_current_status()
                self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_RIGHT, AUDIO_STATUS.STATUS_STOP)
                self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_LEFT, AUDIO_STATUS.STATUS_STOP)
                MediaPlayer.stop_any_play()

                self.RecordAudioWorker.start()
            else:
                MediaPlayer.stop_any_play()
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_WARNING,
                                 text="Не обнаружен источник звукозаписи!",
                                 title="Внимание!",
                                 variant_yes="Закрыть", variant_no="", callback=None)
                self.__main_window.on_test_phb_fail(self.test_type)

    def stop_record_stream(self):
        """Если запущен поток аудиозаписи
            Отключен потому что вызывает конфиликт в отдельном потоке.
        """
        pass
        # if self.stream is not None:
        #     self.stream.stop_stream()
        #     self.stream.close()
        #     self.stream = None

    def on_user_pressed_repeat_test(self):
        self.set_test_default_params()
        MediaPlayer.stop_any_play()

        self.stop_record_stream()
        self.set_default_record_play()

    def set_test_default_params(self):
        self.show_result_btns(False)
        UserFollowTest.set_clear_class()
        UserFollowTest(AUDIO_TEST_STEP.STEP_RECORD)
        UserFollowTest(AUDIO_TEST_STEP.STEP_LEFT_CHANNEL)
        UserFollowTest(AUDIO_TEST_STEP.STEP_RIGHT_CHANNEL)

        self.all_channel_player.load_file(self.path_to_record_audio)
        self.all_channel_player.set_volume(1.0)
        self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_RIGHT, AUDIO_STATUS.STATUS_STOP)
        self.set_audio_test_icon(AUDIO_CHANNEL.CHANNEL_LEFT, AUDIO_STATUS.STATUS_STOP)
        self.set_record_btn_current_status()
        self.left_channel_player.set_volume(1.0)  # * .01
        self.right_channel_player.set_volume(1.0)  # * .01
        self.ui.horizontalSlider_volume.setValue(100)

    def on_stop_record_play_time(self):
        """Вызов после колнца таймера"""
        self.set_default_record_play()
        self.stop_record_stream()
        self.set_record_btn_current_status()
        self.all_channel_player.stop_play()
        if AutoTest.is_auto_test_start():
            AutoTest.stop()
            self.set_auto_test_enabled_ui_event(False)
        self.is_all_sub_test_used(AUDIO_TEST_STEP.STEP_RECORD)
        print("Вызов on_stop_record_play_time")

    def set_default_record_play(self):
        """Сброс записи и таймера"""
        self.record_state = AUDIO_TEST_RECORD_STATE.STATE_NONE
        self.set_record_btn_current_status()
        self.play_record_timer_count = 0

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
        if self.record_state == AUDIO_TEST_RECORD_STATE.STATE_NONE:
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
            self.is_all_sub_test_used(AUDIO_TEST_STEP.STEP_LEFT_CHANNEL)

    def on_user_pressed_play_right(self):
        print("play right")
        if self.record_state == AUDIO_TEST_RECORD_STATE.STATE_NONE:
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
            self.is_all_sub_test_used(AUDIO_TEST_STEP.STEP_RIGHT_CHANNEL)

    def window_show(self, test_type: TEST_TYPE) -> str:
        """
        Напоминалочка: Отключенный к херам аудио драйвер не даёт ошибку при воспроизведение треков
        :param test_type:
        :return:
        """
        patch_left = CSpeakerTest.get_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_LEFT)
        patch_right = CSpeakerTest.get_test_stats(SPEAKER_PARAMS.AUDIO_PATCH_RIGHT)
        if None in (patch_left, patch_right) or not isinstance(patch_left, str) or not isinstance(patch_right, str):
            return "Один из путей до файла с музыкой в файле конфигурации ошибочно задан"

        if patch_left.find("content") == -1 or patch_right.find("content") == -1:
            return "Файл с песней должен лежать в папке 'content'"

        if patch_left.find(".mp3") == -1 or patch_right.find(".mp3") == -1:
            return "Поддерживаемые форматы песен: .mp3"

        if not file_isfile(patch_left) or not file_isfile(patch_right):
            return "Указанный в конфигурации файл с песней не обнаружен"

        self.left_channel_player.load_file(patch_left)
        self.right_channel_player.load_file(patch_right)
        self.set_test_default_params()
        if test_type == TEST_TYPE.TEST_SPEAKER_MIC:
            self.ui.groupBox.setTitle("Тест динамиков и микрофона")
        elif test_type == TEST_TYPE.TEST_HEADSET_MIC:
            self.ui.groupBox.setTitle("Тест наушников и микрофона(В наушниках)")

        self.play_record_timer.start(1007)
        self.show()
        return "True"

    def is_record_avalible_open(self) -> bool:
        stream = None
        try:
            stream = self.precord.open(format=self.FORMAT, channels=self.CHANNELS,
                                       rate=self.RATE, input=True,
                                       )

            stream.start_stream()
            return True
        except:
            return False
        finally:
            if stream is not None:
                stream.stop_stream()
                stream.close()

    def show_result_btns(self, status: bool):
        status = not status
        # self.ui.pushButton_fail.setHidden(status)
        self.ui.pushButton_success.setHidden(status)
        self.ui.pushButton_repeat.setHidden(status)
        self.ui.pushButton_start_test.setHidden(not status)

    @classmethod
    def is_any_record_avalible(cls) -> bool:
        try:
            p = PyAudio()

            # Получение информации о устройствах
            device_count = p.get_device_count()
            for i in range(device_count):
                device_info = p.get_device_info_by_index(i)
                # Проверяем, является ли устройство микрофоном
                if device_info['maxInputChannels'] > 0:
                    return True

            return False
        except:
            return False

    def closeEvent(self, e):
        MediaPlayer.stop_any_play()

        self.stop_record_stream()
        self.set_default_record_play()
        self.play_record_timer.stop()
        if AutoTest.is_auto_test_start():
            AutoTest.stop()
            self.set_auto_test_enabled_ui_event(False)

        e.accept()

    def is_all_sub_test_used(self, incomming_sub_step: AUDIO_TEST_STEP):
        if not UserFollowTest.is_buttons_already_show():

            UserFollowTest.set_user_test_result(incomming_sub_step, True)
            if UserFollowTest.is_all_test_is_true():
                self.show_result_btns(True)


class RecordWorker(QThread):
    update_label = Signal(str)

    def __init__(self, main_class: CSpeakerTestWindow):
        super().__init__()
        self._main_window = main_class

    def run(self):
        mw: CSpeakerTestWindow = self._main_window
        try:
            print("Вход в поток")

            frames = list()
            mw.stream = mw.precord.open(format=mw.FORMAT, channels=mw.CHANNELS,
                                        rate=mw.RATE, input=True,
                                        )

            mw.stream.start_stream()
            for i in range(0, int(mw.RATE / mw.CHUNK * 3)):
                data = mw.stream.read(mw.CHUNK)
                frames.append(data)

            mw.stream.stop_stream()
            mw.stream.close()

            if mw.record_state == AUDIO_TEST_RECORD_STATE.STATE_RECORD:
                wf = wave_open(mw.path_to_record_audio, 'wb')
                wf.setnchannels(mw.CHANNELS)
                wf.setsampwidth(mw.precord.get_sample_size(mw.FORMAT))
                wf.setframerate(mw.sample_rate)
                wf.writeframes(b''.join(frames))
                wf.close()
                mw.record_state = AUDIO_TEST_RECORD_STATE.STATE_PLAY
                mw.set_record_btn_current_status()

                mw.play_record_timer_count = 3
                mw.all_channel_player.start_play()

        except Exception as err:
            print(f"Ошибка в start_record_script -> '{err}'")
            mw.set_default_record_play()
            mw.stop_record_stream()
            mw.record_state = AUDIO_TEST_RECORD_STATE.STATE_NONE
            mw.set_record_btn_current_status()
        return


class UserFollowTest:
    """Класс для проверки чекал ли юзер тест"""
    __test_list = list()
    __show_buttons = False

    def __init__(self, test_step: AUDIO_TEST_STEP):
        self.result = False
        self.test_step = test_step
        UserFollowTest.__test_list.append(self)

    @classmethod
    def set_user_test_result(cls, test_step: AUDIO_TEST_STEP, result: bool):
        unit = cls.get_test_unit_from_test_type(test_step)
        if unit:
            unit.result = result

    @classmethod
    def is_all_test_is_true(cls) -> bool:
        all_len = len(cls.__test_list)
        count_of_true = 0
        for unit in cls.__test_list:
            if unit:
                if unit.result is True:
                    count_of_true += 1
        if all_len == count_of_true:
            cls.__show_buttons = True
            return True

        return False

    @classmethod
    def get_test_unit_from_test_type(cls, test_step: AUDIO_TEST_STEP) -> any:
        for unit in cls.__test_list:
            if unit.test_step == test_step:
                return unit

    @classmethod
    def set_clear_class(cls):
        for unit in cls.__test_list:
            if unit:
                del unit
        cls.__test_list.clear()
        cls.__show_buttons = False

    @classmethod
    def set_default_units(cls):
        for unit in cls.__test_list:
            if unit:
                unit.result = False

    @classmethod
    def is_buttons_already_show(cls) -> bool:
        return cls.__show_buttons


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


class AutoTest:
    __start_test = False
    __current_test = AUDIO_TEST_STEP.STEP_NONE
    __test_timer = 0

    @classmethod
    def is_auto_test_start(cls) -> bool:
        return cls.__start_test

    @classmethod
    def get_current_auto_test(cls) -> AUDIO_TEST_STEP:
        return cls.__current_test

    @classmethod
    def start_test(cls):
        cls.__start_test = True
        cls.__current_test = AUDIO_TEST_STEP.STEP_NONE
        cls.__test_timer = 0

    @classmethod
    def set_step(cls, timer_count: int, test_step: AUDIO_TEST_STEP):
        cls.__current_test = test_step
        cls.__test_timer = timer_count

    @classmethod
    def set_update_time_count(cls) -> bool:
        cls.__test_timer -= 1
        if cls.__test_timer == 0:
            return True

        return False

    @classmethod
    def stop(cls):
        cls.__current_test = AUDIO_TEST_STEP.STEP_NONE
        cls.__start_test = False
        cls.__test_timer = 0
