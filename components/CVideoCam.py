from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl, Qt

from os.path import isfile as file_isfile
import subprocess
from components.CExternalDisplay import CExternalDisplay
from enuuuums import VIDEO_CAM_PARAMS, TEST_TYPE, CONFIG_PARAMS
from ui.test_videocam import Ui_TestVideoCamWindow


class CVideoCam:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: VIDEO_CAM_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: VIDEO_CAM_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})


class CVideoCamWindow(QMainWindow):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestVideoCamWindow()
        self.ui.setupUi(self)
        self.center()
        # self.ui.graphicsView
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.ui.videobox)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_FRONT_CAMERA))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_FRONT_CAMERA))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_FRONT_CAMERA))

        self.setWindowTitle(f'Меню теста')

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

    def window_show(self) -> bool:
        # self.player.setSource(QUrl.fromLocalFile(patch))

        # потому что в общей куче конфигов
        # если задан список, то значит у нас есть указанные размеры
        # если строка то открываем на полный экран
        # Это не ошибка. В конфиге экстер дисплея сидит конфиг дисплей резолюшн
        display_resolution_list = CExternalDisplay.get_test_stats(CONFIG_PARAMS.DISPLAY_RESOLUTION)
        #self.player.play()
        if isinstance(display_resolution_list, str):
            self.showMaximized()
        else:
            self.show()

        return True

    def closeEvent(self, e):
        # self.player.stop()
        e.accept()
