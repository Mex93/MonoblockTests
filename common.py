from datetime import datetime
from PySide6 import QtWidgets

from components.CCustomModalWindow import ModalWindow, SMBOX_ICON_TYPE

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
    window = ModalWindow(icon_style, text, title, callback)

    if len(variant_yes) > 0:
        window.add_variant(variant_yes, QtWidgets.QMessageBox.ButtonRole.YesRole)
    if len(variant_no) > 0:
        window.add_variant(variant_no, QtWidgets.QMessageBox.ButtonRole.NoRole)

    window.show()
    return window.get_window_id()


def send_message_box_triple_variant(icon_style, text: str, title: str, variant_yes: str, variant_no: str,
                                    variant_apply: str,
                                    callback=None, exit_callback=None):
    window = ModalWindow(icon_style, text, title, callback, exit_callback)

    if len(variant_yes) > 0:
        window.add_variant(variant_yes, QtWidgets.QMessageBox.ButtonRole.YesRole)
    if len(variant_no) > 0:
        window.add_variant(variant_no, QtWidgets.QMessageBox.ButtonRole.NoRole)
    if len(variant_apply) > 0:
        window.add_variant(variant_apply, QtWidgets.QMessageBox.ButtonRole.ApplyRole)

    window.show()
    return window.get_window_id()
