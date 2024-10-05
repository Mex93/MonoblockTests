import sys

from cv2 import VideoCapture as cv2_VideoCapture
from cv2 import cvtColor as cv2_cvtColor
from cv2 import COLOR_BGR2RGB as cv2_COLOR_BGR2RGB

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam Stream")

        # Устанавливаем макет
        layout = QVBoxLayout()
        self.imageLabel = QLabel(self)
        layout.addWidget(self.imageLabel)
        self.setLayout(layout)

        # Инициализируем веб-камеру
        self.capture = cv2_VideoCapture(0)  # 0 — это индекс для первой камеры

        # Таймер для обновления кадров
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Обновляем каждые 20 мс

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            # Преобразуем цветовую схему BGR в RGB
            frame = cv2_cvtColor(frame, cv2_COLOR_BGR2RGB)

            # Создаем QImage из массива numpy
            h, w, _ = frame.shape
            qImg = QImage(frame.data, w, h, w * 3, QImage.Format_RGB888)

            # Устанавливаем изображение в QLabel
            self.imageLabel.setPixmap(QPixmap.fromImage(qImg))

    def closeEvent(self, event):
        # Освобождаем камеру при закрытии окна
        self.capture.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    camera_widget = CameraWidget()
    camera_widget.show()
    sys.exit(app.exec())
