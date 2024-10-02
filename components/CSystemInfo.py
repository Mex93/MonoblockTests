import platform
from psutil import disk_partitions, virtual_memory, disk_usage, net_if_addrs
from wmi import WMI
from os import system
import subprocess, ipaddress

from socket import AF_INET
from win32com.client import GetObject
from bluetooth import discover_devices
from enuuuums import TEST_TYPE, TEST_SYSTEM_INFO_TYPES, SYS_INFO_PARAMS
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import Qt

import PySide6.QtCore as qc

from ui.test_sys_info import Ui_TestSysInfoWindow


class CSystemInfo:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: SYS_INFO_PARAMS) -> bool | str | int | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: SYS_INFO_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})

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
    def check_lan_connectivity(ip: str) -> bool | None:
        try:
            ip_object = ipaddress.ip_address(ip)
            # Пинговать известный адрес (например, 8.8.8.8 - Google DNS)
            response = system("ping -n 1 " + ip)
            if response == 0:
                return True
            else:
                return False

        except ValueError:
            print(f"check_lan_connectivity -> The IP address '{ip}' is not valid")
            return None

    @staticmethod
    def scan_wifi() -> bool | list:

        output = subprocess.check_output("netsh wlan show networks", shell=True)
        output = output.decode('cp866')  # Или 'utf-8', если это подходит
        if len(output) > 0:
            if output.find("Беспроводной интерфейс в системе отсутствует") != -1:
                raise ValueError("Беспроводной интерфейс в системе отсутствует")
            elif output.find("Сейчас видно следующее количество сетей: 0") != -1:
                return False
            else:
                networks = []
                lines = output.splitlines()
                for line in lines:
                    if "SSID" in line:
                        network_name = line.split(":")[1].strip()
                        networks.append(network_name)
                if len(networks) > 0:
                    return networks
        return False

    @staticmethod
    def scan_bluetooth_devices() -> bool | list:

        nearby_devices = discover_devices(duration=8, lookup_names=True)
        if len(nearby_devices) == 0:
            return False
        else:
            devices = list()
            for _, name in nearby_devices:
                # print(f"{name} - {addr}")
                devices.append(name)
            if len(devices) > 0:
                return devices


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
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_SYSTEM_INFO))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_SYSTEM_INFO))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_SYSTEM_INFO))

    def set_default_string(self):
        unit = self.ui.textBrowser_lan_port
        unit.clear()
        unit.append("Получение результатов...")

        self.ui.label_ram_info.setText("-")
        self.ui.label_bios_info.setText("-")
        self.ui.label_cpu_info.setText("-")
        self.ui.label_os_info.setText("-")

    @staticmethod
    def get_data() -> list | None:
        # ram
        result_list = list()
        on_test_count = 0
        ram_dict = dict()
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.RAM_CHECK) is True:
            memory_info = CSystemInfo.get_memory_info()

            ram_dict.update({"data": f"ОЗУ: Всего: {memory_info['total'] / (1024 ** 3):.2f} | "
                                     f"Доступно: {memory_info['available'] / (1024 ** 3):.2f} | "
                                     f"Использовано: {memory_info['used'] / (1024 ** 3):.2f} ГБ",

                             "check_string": f"all_{memory_info['total'] / (1024 ** 3):.2f}_"
                                             f"avalible_{memory_info['available'] / (1024 ** 3):.2f}_"
                                             f"used_{memory_info['used'] / (1024 ** 3):.2f}",
                             "test_id": TEST_SYSTEM_INFO_TYPES.RAM_STATS})
            on_test_count += 1
        else:
            ram_dict.update({"data": f"ОЗУ: Проверка отключена",

                             "check_string": f"all_none",
                             "test_id": TEST_SYSTEM_INFO_TYPES.RAM_STATS})

        result_list.append(ram_dict)

        bios_dict = dict()
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BIOS_CHECK) is True:
            # BIOS
            bios_info = CSystemInfo.get_bios_info()
            bios_dict.update({"data": f"BIOS: {bios_info['manufacturer']} | {bios_info['version']} | "
                                      f"SN: {bios_info['serial_number']} | Date: {bios_info['release_date']}",

                              "check_string":
                                  f"manufacturer_{bios_info['manufacturer']}_"
                                  f"version_{bios_info['version']}_"
                                  f"sn_{bios_info['serial_number']}_"
                                  f"releasedate_{bios_info['release_date']}",

                              "test_id": TEST_SYSTEM_INFO_TYPES.BIOS_STATS})
            on_test_count += 1
        else:
            bios_dict.update({"data": f"BIOS: Проверка отключена",

                              "check_string":
                                  f"manufacturer_none",

                              "test_id": TEST_SYSTEM_INFO_TYPES.BIOS_STATS})

        result_list.append(bios_dict)

        #
        # cpu
        cpu_dict = dict()
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.CPU_CHECK) is True:

            cpu_dict.update({"data": f"CPU: {CSystemInfo.get_cpu_info()}",

                             "check_string":
                                 f"cpu_{CSystemInfo.get_cpu_info()}",

                             "test_id": TEST_SYSTEM_INFO_TYPES.CPU_STATS})
        else:
            cpu_dict.update({"data": f"CPU: Проверка отключена",

                             "check_string":
                                 f"cpu_none",

                             "test_id": TEST_SYSTEM_INFO_TYPES.CPU_STATS})
            on_test_count += 1

        result_list.append(cpu_dict)

        #
        # OS
        os_dict = dict()
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.OS_CHECK) is True:

            os_dict.update({"data": f"OS: {platform.system()} {platform.release()} {platform.version()} | "
                                    f"{CSystemInfo.get_computer_name()}",

                            "check_string":
                                f"system_{platform.system()}_"
                                f"release_{platform.release()}_"
                                f"version_{platform.version()}_"
                                f"comp_name_{CSystemInfo.get_computer_name()}",

                            "test_id": TEST_SYSTEM_INFO_TYPES.OS_STATS})
            on_test_count += 1
        else:
            os_dict.update({"data": f"OS: Проверка отключена",

                            "check_string":
                                f"system_none",

                            "test_id": TEST_SYSTEM_INFO_TYPES.OS_STATS})

        result_list.append(os_dict)

        # # остальные тесты
        # LAN test
        lan_dict = dict()
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.LAN_CHECK) is True:
            check_ip = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.LAN_IP)
            response = CSystemInfo.check_lan_connectivity(check_ip)
            if response is None:
                string = "LAN Test: <span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">IP невалидный</span>"
                ip_check_result = "not_valid_ip"
            elif response is True:
                string = "LAN Test: <span style=\" font-size:14pt; font-weight:700; color:#83ff37;\">пройден успешно!</span>"
                ip_check_result = "success"
            else:
                string = "LAN Test: <span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">не пройден!</span>"
                ip_check_result = "fail"

            lan_dict.update({"data": string,

                             "check_string":
                                 f"result_{ip_check_result}",

                             "test_id": TEST_SYSTEM_INFO_TYPES.LAN_STATS})
            on_test_count += 1
        else:
            lan_dict.update({"data": "LAN Test: Проверка отключена",

                             "check_string":
                                 f"result_none",

                             "test_id": TEST_SYSTEM_INFO_TYPES.LAN_STATS})

        result_list.append(lan_dict)

        # WLAN test
        wifi_dict = dict()
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.WLAN_CHECK) is True:

            available_networks = None
            try:
                available_networks = CSystemInfo.scan_wifi()
                if isinstance(available_networks, list):
                    string = f"WIFI Test: <span style=\" font-size:14pt; font-weight:700; color:#83ff37;\">пройден успешно! <span style=\" color:black;\">Сети видны: [{", ".join(available_networks)}]</span>"
                else:
                    string = "WIFI Test: <span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">не пройден! <span style=\" color:black;\">Нет доступных сетей.</span>"
            except:
                string = "WIFI Test: <span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">WIFI модуль не обнаружен!</span>"

            if not available_networks:
                available_networks = list()

            wifi_dict.update({"data": string,

                              "check_string":
                                  f"result_{"success" if len(available_networks) > 0 else "fail"}",

                              "test_id": TEST_SYSTEM_INFO_TYPES.WIFI_STATS})
            on_test_count += 1
        else:
            wifi_dict.update({"data": "WIFI Test: Проверка отключена",

                              "check_string":
                                  f"result_none",

                              "test_id": TEST_SYSTEM_INFO_TYPES.WIFI_STATS})

        result_list.append(wifi_dict)

        #
        # BT test
        bt_dict = dict()
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BT_CHECK) is True:
            bt_result = None
            try:
                bt_result = CSystemInfo.scan_bluetooth_devices()
                if isinstance(bt_result, list):
                    string = f"Bluetooth Test: <span style=\" font-size:14pt; font-weight:700; color:#83ff37;\">пройден успешно! <span style=\" color:black;\">Сети видны: [{", ".join(bt_result)}].</span>"
                else:
                    string = "Bluetooth Test: <span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">не пройден! Сети не видны</span>"
            except:
                string = "Bluetooth Test: <span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">BT модуль не обнаружен!</span>"

            if not bt_result:
                bt_result = list()

            bt_dict.update({"data": string,

                            "check_string":
                                f"result_{"success" if len(bt_result) > 0 else "fail"}",

                            "test_id": TEST_SYSTEM_INFO_TYPES.BT_STATS})
            on_test_count += 1
        else:
            bt_dict.update({"data": "Bluetooth Test: Проверка отключена",

                            "check_string":
                                f"result_none",

                            "test_id": TEST_SYSTEM_INFO_TYPES.BT_STATS})

        result_list.append(bt_dict)

        if on_test_count > 0:
            return result_list

        return None

    def load_data(self, data_list: list | None):

        unit = self.ui.textBrowser_lan_port
        unit.clear()

        if data_list is None:
            unit.append("Ни один из тестов не запущен!")
            return

        unit.append("Результаты получены!")
        for item_dict in data_list:
            test_type = item_dict.get("test_id", None)
            data = item_dict.get("data", None)
            if test_type is None or data is None:
                continue

            # ram
            match test_type:
                case TEST_SYSTEM_INFO_TYPES.RAM_STATS:
                    self.ui.label_ram_info.setText(data)

                # bios
                case TEST_SYSTEM_INFO_TYPES.BIOS_STATS:
                    self.ui.label_bios_info.setText(data)

                # cpu
                case TEST_SYSTEM_INFO_TYPES.CPU_STATS:
                    self.ui.label_cpu_info.setText(data)
                # os
                case TEST_SYSTEM_INFO_TYPES.OS_STATS:
                    self.ui.label_os_info.setText(data)

                # остальные тесты
                # lan
                case TEST_SYSTEM_INFO_TYPES.LAN_STATS:
                    unit.append(data)
                # wifi
                case TEST_SYSTEM_INFO_TYPES.WIFI_STATS:
                    unit.append(data)
                # BT
                case TEST_SYSTEM_INFO_TYPES.BT_STATS:
                    unit.append(data)

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
