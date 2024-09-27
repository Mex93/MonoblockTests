import platform
from psutil import disk_partitions, virtual_memory, disk_usage, net_if_addrs
from wmi import WMI
from os import system
from socket import AF_INET
from win32com.client import GetObject

from wifi import Cell as WIFI_Cell

from enuuuums import TEST_TYPE
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)

import PySide6.QtCore as qc

from ui.test_sys_info import Ui_TestSysInfoWindow


class CSystemInfo:
    __test_used = False
    __bios_string = ""
    __cpu_string = ""
    __ram_string = ""
    __disks_string = ""
    __bios_stats = None
    __cpu_stats = None
    __ram_stats = None
    __disks_stats = None

    @classmethod
    def is_test_used(cls) -> bool:
        return cls.__test_used

    @classmethod
    def set_test_used(cls, used: bool):
        cls.__test_used = used

    @classmethod
    def set_bios_stats(cls, value: bool):
        cls.__bios_stats = value

    @classmethod
    def get_bios_stats(cls) -> bool:
        return cls.__bios_stats

    ########
    @classmethod
    def set_cpu_stats(cls, value: bool):
        cls.__cpu_stats = value

    @classmethod
    def get_cpu_stats(cls) -> bool:
        return cls.__cpu_stats

    ########
    @classmethod
    def set_ram_stats(cls, value: bool):
        cls.__ram_stats = value

    @classmethod
    def get_ram_stats(cls) -> bool:
        return cls.__ram_stats

    @classmethod
    ########
    def set_disk_stats(cls, value: bool):
        cls.__disks_stats = value

    @classmethod
    def get_disk_stats(cls) -> bool:
        return cls.__disks_stats

    @staticmethod
    # Получаем название компьютера
    def get_computer_name():
        return platform.node()

    # Получаем информацию о подключенных жестких дисках
    @staticmethod
    def get_drives_only_disk_char():
        drives = []
        partitions = disk_partitions()
        for partition in partitions:
            drives.append(partition.device)
        return drives

    @staticmethod
    def get_cpu_info():
        root_winmgmts = GetObject("winmgmts:root/cimv2")
        cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
        return cpus[0].Name

    @staticmethod
    def get_drives_info():
        drives_info = []
        partitions = disk_partitions()
        for partition in partitions:
            try:
                partition_info = disk_usage(partition.mountpoint)
                drive_details = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'total': partition_info.total,
                    'used': partition_info.used,
                    'free': partition_info.free,
                }
                drives_info.append(drive_details)
            except Exception as e:
                print(f"Не удалось получить информацию о диске {partition.device}: {e}")
        return drives_info

    # Получаем объем оперативной памяти
    @staticmethod
    def get_ram():
        ram = virtual_memory().total / (1024 ** 3)  # Конвертируем в гигабайты
        return ram

    @staticmethod
    def get_memory_info():
        vmemory = virtual_memory()
        return {
            'total': vmemory.total,
            'available': vmemory.available,
            'used': vmemory.used,
        }

    # Получаем сведения о BIOS
    @staticmethod
    def get_bios_info():
        c = WMI()
        bios_info = c.Win32_BIOS()[0]
        return {
            'manufacturer': bios_info.Manufacturer,
            'version': bios_info.Version,
            'serial_number': bios_info.SerialNumber,
            'release_date': bios_info.ReleaseDate,
        }

    @staticmethod
    def get_network_interfaces():
        interfaces = net_if_addrs()
        interface_info = {}

        for interface in interfaces:
            # Получаем адреса интерфейса
            addresses = interfaces[interface]
            interface_info[interface] = {
                'ip_address': None,
                'netmask': None,
                'type': None
            }

            for addr in addresses:
                if addr.family == AF_INET:  # IPv4
                    interface_info[interface]['ip_address'] = addr.address
                    interface_info[interface]['netmask'] = addr.netmask
                    interface_info[interface]['type'] = 'Ethernet' if 'Ethernet' in interface else 'Wi-Fi'

        return interface_info

    @staticmethod
    def check_lan_connectivity() -> bool:
        # Пинговать известный адрес (например, 8.8.8.8 - Google DNS)
        hostname = "192.168.5.1"
        response = system("ping -n 1 " + hostname)
        if response == 0:
            return True

    @staticmethod
    def scan_wifi():
        wifi_cells = WIFI_Cell.all('wlan0')  # Укажите ваш интерфейс Wi-Fi (например, wlan0)
        networks = [(cell.ssid, cell.signal) for cell in wifi_cells]
        return networks



class CSystemInfoWindow(QMainWindow):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestSysInfoWindow()
        self.ui.setupUi(self)
        QFontDatabase.addApplicationFont("designs/Iosevka Bold.ttf")

        # unit = self.ui.tableWidget_devices

        # MAX_ROW_COUNT = 2
        # header_text = ["Накопитель", "Объём"]
        # unit.setColumnCount(MAX_ROW_COUNT)
        # for i in range(0, MAX_ROW_COUNT):
        #     item = QTableWidgetItem(header_text[i])  # Устанавливаем текст при создании
        #     unit.setHorizontalHeaderItem(i, item)  # Устанавливаем элемент заголовка

        self.setWindowTitle(f'Меню теста')
        self.setWindowModality(qc.Qt.WindowModality.ApplicationModal)

    def load_data(self):

        # ram
        memory_info = CSystemInfo.get_memory_info()
        self.ui.label_ram_info.setText(f"ОЗУ: Всего: {memory_info['total'] / (1024 ** 3):.2f} | "
                                       f"Доступно: {memory_info['available'] / (1024 ** 3):.2f} | "
                                       f"Использовано: {memory_info['used'] / (1024 ** 3):.2f} ГБ")

        # BIOS
        bios_info = CSystemInfo.get_bios_info()
        self.ui.label_bios_info.setText(f"BIOS: {bios_info['manufacturer']} | {bios_info['version']} | "
                                        f"SN: {bios_info['serial_number']} | Date: {bios_info['release_date']}")

        # cpu
        self.ui.label_cpu_info.setText(f"CPU: {CSystemInfo.get_cpu_info()}")

        # OS
        self.ui.label_os_info.setText(f"OS: {platform.system()} {platform.release()} {platform.version()} | "
                                      f"{CSystemInfo.get_computer_name()}")

        # остальные тесты

        unit = self.ui.textBrowser_lan_port
        unit.clear()
        unit.append("Тестирование запущено!!")

        # lan
        response = CSystemInfo.check_lan_connectivity()
        if response:
            unit.append("LAN Test: <span style=\" font-size:14pt; font-weight:700; color:#83ff37;\">пройден успешно!</span>")
        else:
            unit.append("LAN Test: <span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">не пройден!</span>")

        # wifi test
        wifi = CSystemInfo.scan_wifi()
        print(wifi)
        unit.append(
            "WIFI Test: <span style=\" font-size:14pt; font-weight:700; color:#83ff37;\">пройден успешно!</span>")

        # # disks
        # drivers = CSystemInfo.get_drives_info()
        # unit = self.ui.tableWidget_devices
        #
        # __sortingEnabled = unit.isSortingEnabled()
        # unit.setSortingEnabled(False)
        #
        # count = len(drivers)
        # if count > 0:
        #     unit.setRowCount(count)
        #     for index, driver in enumerate(drivers):
        #
        #         print(index)
        #         item = QTableWidgetItem(f"{driver['device']}")
        #         unit.setItem(index, 0, item)
        #
        #         item = QTableWidgetItem(f"{driver['total'] / (1024 ** 3):.2f} ГБ")
        #         unit.setItem(index, 1, item)
        #
        # unit.setSortingEnabled(__sortingEnabled)
