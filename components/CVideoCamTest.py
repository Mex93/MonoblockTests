from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QTimer

from PySide6.QtGui import QImage, QPixmap

from cv2 import VideoCapture as cv2_VideoCapture
from cv2 import cvtColor as cv2_cvtColor
from cv2 import COLOR_BGR2RGB as cv2_COLOR_BGR2RGB

from enuuuums import VIDEO_CAM_PARAMS, TEST_TYPE
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

        self.start_capture = False
        # Таймер для обновления кадров
        self.capture = None  # 0 — это индекс для первой камеры
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)  # сколько навесиш раз функцию столько и будет вызываться

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

    def update_frame(self):
        if self.start_capture:
            ret, frame = self.capture.read()
            if ret:
                # Преобразуем цветовую схему BGR в RGB
                frame = cv2_cvtColor(frame, cv2_COLOR_BGR2RGB)

                # Создаем QImage из массива numpy
                h, w, _ = frame.shape
                qImg = QImage(frame.data, w, h, w * 3, QImage.Format_RGB888)

                # Устанавливаем изображение в QLabel
                self.ui.label_video.setPixmap(QPixmap.fromImage(qImg))

    def window_show(self) -> str:
        # self.player.setSource(QUrl.fromLocalFile(patch))

        # потому что в общей куче конфигов
        # если задан список, то значит у нас есть указанные размеры
        # если строка то открываем на полный экран
        # Это не ошибка. В конфиге экстер дисплея сидит конфиг дисплей резолюшн

        if self.start_capture:
            return "Камера занята"

        try:
            camera_index = CVideoCam.get_test_stats(VIDEO_CAM_PARAMS.CAMERA_INDEX)
            if not isinstance(camera_index, int) or (camera_index < 0 or camera_index > 20):
                return "Индекс камеры в файле конфигурации должен быть целым числом от 0 до 20"

            if not self.is_camera_connected(camera_index):
                return "Камера не обнаружена"
            self.start_capture = True
            self.capture = cv2_VideoCapture(camera_index)  # 0 — это индекс для первой камеры
            self.timer.start(20)  # Обновляем каждые 20 мс
            self.ui.label_video.setText("Получение данных...")
            self.show()
            return "True"
        except Exception as err:
            return f"Во время выполнения проверки старта теста возникла ошибка '{err}'"


    @classmethod
    def is_camera_connected(cls, cam_index=0):
        # Создаем объект VideoCapture
        cap = cv2_VideoCapture(cam_index)

        # Проверяем, удалось ли открыть камеру
        if not cap.isOpened():
            return False
        else:
            cap.release()  # Освобождаем объект VideoCapture
            return True

    def closeEvent(self, e):
        # Освобождаем камеру при закрытии окна
        if self.start_capture:
            self.start_capture = False
            self.timer.stop()

            if self.capture.isOpened():
                self.capture.release()
                del self.capture
        e.accept()
