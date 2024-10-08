from PySide6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from os.path import isfile as file_isfile
import screen_brightness_control as sbc

from enuuuums import BRIGHTNESS_PARAMS, TEST_TYPE
from ui.test_brightness import Ui_TestBrightnessWindow


class CBrightnessTest:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: BRIGHTNESS_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: BRIGHTNESS_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})


class CBrightnessTestWindow(QMainWindow):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestBrightnessWindow()
        self.ui.setupUi(self)

        self.timer_test = QTimer(self)
        self.timer_test.timeout.connect(self.update_brightness_test)
        self.timer_brightness = QTimer(self)
        self.timer_brightness.timeout.connect(self.update_brightness_value)
        self.start_test = False
        self.secons_for_stop = 0
        self.to_up = False

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_BRIGHTNESS))
        self.ui.pushButton_relaunch.clicked.connect(
            self.repeat_test)
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_BRIGHTNESS))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_BRIGHTNESS))

        self.setWindowTitle(f'Меню теста')
        self.viewer = None
        self.brightness_value = 0

    def repeat_test(self):
        CBrightnessTestWindow.set_brightness(100)
        self.start_test = True
        self.secons_for_stop = 5
        self.to_up = False

        self.ui.frame_btns.setHidden(True)

    def update_brightness_value(self):
        if self.start_test:

            self.brightness_value -= 5
            if self.brightness_value < 0:
                self.brightness_value = 100
            CBrightnessTestWindow.set_brightness(self.brightness_value)

    def update_brightness_test(self):
        if self.start_test:
            self.secons_for_stop -= 1
            if self.secons_for_stop <= 0:
                self.clear_test()
                self.ui.frame_btns.setHidden(False)

    def window_show(self) -> bool:
        image_path = CBrightnessTest.get_test_stats(BRIGHTNESS_PARAMS.FILE_PATCH)
        if image_path and isinstance(image_path, str):
            if image_path.find("content/") != -1:
                if file_isfile(image_path):
                    if self.viewer is None:
                        self.viewer = ImageView(image_path)  # Замените на путь к вашему изображению
                        self.ui.verticalLayout_2.insertWidget(0, self.viewer)
                    self.timer_test.start(1004)
                    self.timer_brightness.start(150)
                    CBrightnessTestWindow.set_brightness(100)
                    self.start_test = True
                    self.secons_for_stop = 5
                    self.to_up = False

                    self.ui.frame_btns.setHidden(True)
                    self.showFullScreen()
                    return True
        return False

    def clear_test(self):
        self.start_test = False
        self.secons_for_stop = 0
        self.to_up = False
        self.brightness_value = 100

    def closeEvent(self, e):
        self.clear_test()
        self.timer_test.stop()
        self.timer_brightness.stop()
        e.accept()

    @staticmethod
    def set_brightness(value):
        sbc.set_brightness(max(value, 0))  # Не допускаем отрицательных значений


class ImageView(QGraphicsView):
    def __init__(self, image_path):
        super().__init__()

        # Создаем сцену и устанавливаем ее на QGraphicsView
        scene = QGraphicsScene(self)

        self.setScene(scene)

        # Загружаем изображение
        pixmap = QPixmap(image_path)
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.setSceneRect(self.pixmap_item.boundingRect())
        scene.addItem(self.pixmap_item)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Масштабируем изображение по размеру  QGraphicsView

    def fit_image_to_view(self):
        # Метод для масштабирования изображения по размеру виджета
        if self.pixmap_item:
            self.setSceneRect(self.pixmap_item.boundingRect())
            self.fitInView(self.pixmap_item)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_image_to_view()  # Обновляем масштаб при изменении размера окна
