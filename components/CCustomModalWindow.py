from PySide6.QtWidgets import QMessageBox
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize

from enuuuums import SMBOX_ICON_TYPE


class CustomMessageBox(QMessageBox):
    def __init__(self, closed_func_event=None, parent=None):
        super().__init__(parent)
        self.closed_func_event = closed_func_event

    def closeEvent(self, event):
        # Здесь вы можете выполнить нужную вам функцию
        if self.closed_func_event is not None:
            self.closed_func_event()
        super().closeEvent(event)


class ModalWindow:
    def __init__(self, icon_style, text: str, title: str, callback=None, exit_callback=None):
        msg = CustomMessageBox(exit_callback)
        msg.setWindowTitle(title)
        msg.clickedButton()

        match icon_style:
            case _, SMBOX_ICON_TYPE.ICON_NONE:
                msg.setIcon(QMessageBox.Icon.NoIcon)
            case SMBOX_ICON_TYPE.ICON_ERROR:
                msg.setIcon(QMessageBox.Icon.Critical)
            case SMBOX_ICON_TYPE.ICON_WARNING:
                msg.setIcon(QMessageBox.Icon.Warning)
            case SMBOX_ICON_TYPE.ICON_INFO:
                msg.setIcon(QMessageBox.Icon.Information)
            # case SMBOX_ICON_TYPE.ICON_SUCCESS:
            #     pass
        icon = QIcon()
        icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        msg.setWindowIcon(icon)
        msg.setText(text)

        font = QFont()
        font.setFamilies([u"Segoe UI Emoji"])
        font.setPointSize(12)
        msg.setFont(font)

        if callback is not None:
            msg.buttonClicked.connect(callback)

        self.msg = msg

    def add_variant(self, text: str, variant_type: QtWidgets.QMessageBox.ButtonRole):
        self.msg.addButton(text, variant_type)

    def show(self):
        self.msg.exec()

    def get_window_id(self) -> QMessageBox:
        return self.msg
