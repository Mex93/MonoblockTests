
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QTimer
import os
from PySide6.QtGui import QPixmap
from os.path import isdir as file_isdir

from enuuuums import PATTERNS_TEST_PARAMS, TEST_TYPE, PROGRAM_JOB_TYPE
from ui.test_patterns import Ui_TestPatternsWindow


class CPatternsTest:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: PATTERNS_TEST_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: PATTERNS_TEST_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})


class CPatternsTestWindow(QMainWindow):
    MAX_PATTERNS_INDEX = 0

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestPatternsWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.buttons_show = False
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_PATTERNS))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_PATTERNS))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_PATTERNS))

        self.ui.pushButton_relaunch.clicked.connect(
            self.window_show)

        self.setWindowTitle(f'Меню теста')
        self.viewer = None

        # получение списка

        self.patterns_list = list()
        self.patterns_index = 0

    def window_show(self) -> str:
        self.patterns_list.clear()
        path = "content/patterns"
        if not file_isdir(path):
            return f"В директории программы не найден путь '{path}'"

        # чтение записей
        with os.scandir(path) as listOfEntries:
            for entry in listOfEntries:
                # печать всех записей, являющихся файлами
                if entry.is_file():
                    if entry.name.find(".jpg") == -1:
                        continue

                    self.patterns_list.append(path + "/" + entry.name)

        if len(self.patterns_list):
            self.MAX_PATTERNS_INDEX = len(self.patterns_list)
            self.patterns_index = 0
            self.ui.frame_btns.setHidden(True)
            self.buttons_show = False
            self.set_image()
            self.showFullScreen()
            return "True"
        else:
            return f"В папке '{path}' не обнаружен ни один файл с паттерном в формате .jpg"

    def set_background_color_from_image(self, image_path):
        pixmap = QPixmap(image_path)
        color = pixmap.toImage().pixelColor(pixmap.width() // 2, pixmap.height() // 2)
        self.setStyleSheet(f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});")

    def set_background_image_from_image(self, image_path):
        # self.ui.centralwidget.setStyleSheet(f"background-image: url({image_path}); background-attachment: fixed")
        self.ui.centralwidget.setPixmap(QPixmap.fromImage(image_path))

    def set_image(self):
        if self.patterns_index == self.MAX_PATTERNS_INDEX:
            if self.__main_window.PROGRAM_JOB_FLAG == PROGRAM_JOB_TYPE.JOB_ONLY_FOR_LINE:
                if self.viewer is None:
                    self.viewer = ImageView("content/please_wait_camera.jpg")  # Замените на путь к вашему изображению
                    self.ui.verticalLayout_2.insertWidget(0, self.viewer)
                    timer = QTimer(self)
                    timer.timeout.connect(
                        lambda: self.start_camera_timer(timer))  # сколько навесиш раз функцию столько и будет вызываться
                    timer.start(2000)

                    # self.__main_window.on_test_phb_success(TEST_TYPE.TEST_PATTERNS)
            else:
                self.__main_window.on_test_phb_success(TEST_TYPE.TEST_PATTERNS)
            # Данил велел сделать так, просто при полном пролистывании выкидывает теперь в главное
            return
            # self.patterns_index = 0
            # self.buttons_show = True
            # self.ui.frame_btns.setHidden(False)
        else:
            if self.buttons_show:
                self.buttons_show = False
                self.ui.frame_btns.setHidden(True)
        try:
            self.set_background_color_from_image(self.patterns_list[self.patterns_index])
            self.patterns_index += 1
        except Exception as err:
            # по какой то причине не всегда полный список вовзвращает файлов
            print(err)
            self.__main_window.on_test_phb_success(TEST_TYPE.TEST_PATTERNS)

    def start_camera_timer(self, timer_id: QTimer):
        timer_id.stop()
        self.__main_window.on_test_phb_success(TEST_TYPE.TEST_PATTERNS)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:  # Проверяем, что нажата левая кнопка мыши
            self.set_image()

    def closeEvent(self, e):
        self.__main_window.on_call_in_close_test_window(TEST_TYPE.TEST_PATTERNS)
        e.accept()


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
