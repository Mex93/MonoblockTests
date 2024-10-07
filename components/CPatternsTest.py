from PySide6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QApplication
from PySide6.QtCore import Qt, QTimer
import os, sys
from PySide6.QtGui import QImage, QPixmap

from enuuuums import PATTERNS_TEST_PARAMS, TEST_TYPE
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

        self.old_viever_id = None
        # self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_PATTERNS))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_PATTERNS))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_PATTERNS))
        self.setWindowTitle(f'Меню теста')

        # self.ui.graphicsView_patterns.mouse.connect(self.on_user_clicked())

        # получение списка

        self.patterns_list = list()
        self.patterns_index = 0

    def window_show(self) -> bool:
        self.patterns_list.clear()
        path = "content/patterns"

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
            self.patterns_index = -1
            self.ui.frame_btns.setHidden(True)
            # self.showFullScreen()
            self.showFullScreen()
            self.set_image()
            return True

        return False

    def set_image(self):
        self.patterns_index += 1
        if self.patterns_index > self.MAX_PATTERNS_INDEX:
            self.patterns_index = 0
        if self.old_viever_id is not None:
            self.old_viever_id.deleteLater()
            del self.old_viever_id

        viewer = ImageViewer(self.patterns_list[self.patterns_index])  # Замените на путь к вашему изображению
        self.ui.verticalLayout_2.addWidget(viewer)
        self.old_viever_id = viewer


    def on_user_clicked(self):
        print("я клтикнул")

    def closeEvent(self, e):

        e.accept()


class ImageViewer(QGraphicsView):
    def __init__(self, image_path):
        super().__init__()

        # Создание QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Загружаем изображение
        pixmap = QPixmap(image_path)

        # Создаем элемент с изображением
        self.pixmap_item = QGraphicsPixmapItem(pixmap)

        # Добавляем его на сцену
        self.scene.addItem(self.pixmap_item)

        # Устанавливаем размер сцены в размер изображения

    def fit_image_to_view(self):
        # Метод для масштабирования изображения по размеру виджета
        if self.pixmap_item:
            self.setSceneRect(self.pixmap_item.boundingRect())
            self.fitInView(self.pixmap_item)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_image_to_view()  # Обновляем масштаб при изменении размера окна

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:  # Проверяем, что нажата левая кнопка мыши
            print("та дам")


