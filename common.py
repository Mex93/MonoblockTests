from datetime import datetime
from PySide6.QtWidgets import QMessageBox
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize

from enuuuums import SMBOX_ICON_TYPE

INFO_CURRENT_ADMIN_EMAIL = "ryazanov.n@tvkvant.ru"


def get_rules_text() -> str:
    return (
        "Приведённые правила использования программы обязательны к соблюдению всем пользователям.\n\n"
        "Перечень:\n"
        "1) Разглашение данных предоставляемых программой сторонним лицам, не имеющим отношения к 'ООО Квант', "
        "строго запрещено!\n"
        "2) Попытка декомпиляции и любое вредительство внутри рабочей директории программы строго "
        "запрещено и снимает с разработчика ответственность за возможный ущерб.\n"
        # "3) Перед использованием программы пользователь должен быть ознакомлен с инструкцией.\n"
        "3) Для корректной работы программы пользователь должен указывать корректные данные в файле конфигурации.\n"
        "4) Разработчик имеет право вносить любые изменения в программу и документацию без уведомления пользователей.\n"
        "5) Невыполнение любого из пунктов правил влечёт нарушение пользователем своих обязательств."
    )


def get_about_text() -> str:
    current_year = datetime.now().year
    return ("Комплекс тестов для проверки моноблоков.\n\n"
            "Все права принадлежат ООО 'Квант'.\n\n"
            "Разработчик: Рязанов Н.В.\n"
            f"По всем интересующим вопросам и пожеланиям обращайтесь на почту {INFO_CURRENT_ADMIN_EMAIL}\n\n"
            f"\t\t\t{current_year} г.")


def send_message_box(icon_style, text: str, title: str, variant_yes: str, variant_no: str, callback=None):
    msg = QMessageBox()
    msg.setWindowTitle(title)
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
    icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Normal, QIcon.Off)

    msg.setWindowIcon(icon)
    if len(variant_yes) > 0:
        msg.addButton(variant_yes, QtWidgets.QMessageBox.ButtonRole.YesRole)
    if len(variant_no) > 0:
        msg.addButton(variant_no, QtWidgets.QMessageBox.ButtonRole.NoRole)
    msg.setText(text)

    font = QFont()
    font.setFamilies([u"Segoe UI Emoji"])
    font.setPointSize(12)
    msg.setFont(font)

    if callback is not None:
        msg.buttonClicked.connect(callback)

    msg.exec()
    return msg
