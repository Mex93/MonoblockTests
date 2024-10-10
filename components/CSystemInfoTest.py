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
from PySide6.QtGui import QFontDatabase, QTextCursor
from PySide6.QtCore import Qt

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

    @classmethod
    def get_sub_test_name_from_type(cls, sub_test_type: TEST_SYSTEM_INFO_TYPES) -> str:
        match sub_test_type:
            case TEST_SYSTEM_INFO_TYPES.BT_STATS:
                return "Bluetooth Test"
            case TEST_SYSTEM_INFO_TYPES.OS_STATS:
                return "OS"
            case TEST_SYSTEM_INFO_TYPES.CPU_STATS:
                return "CPU"
            case TEST_SYSTEM_INFO_TYPES.WIFI_STATS:
                return "WIFI Test"
            case TEST_SYSTEM_INFO_TYPES.LAN_STATS:
                return "LAN Test"
            case TEST_SYSTEM_INFO_TYPES.RAM_STATS:
                return "ОЗУ"
            case TEST_SYSTEM_INFO_TYPES.BIOS_STATS:
                return "BIOS"
            case TEST_SYSTEM_INFO_TYPES.DISKS_STATS:
                return "Drive Test"
            case _:
                return ""

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
            print(partition)
        # for partition in partitions:
        #     drives.append([partition.device, partition.maxfile])

        return drives

    @staticmethod
    def get_cpu_info():
        root_winmgmts = GetObject("winmgmts:root/cimv2")
        cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
        return cpus[0].Name

    @staticmethod
    def get_drives_info() -> list | None:
        drives_info = []
        partitions = disk_partitions()
        for partition in partitions:
            try:
                partition_info = disk_usage(partition.mountpoint)
                # drive_details = {
                #     'device': partition.device,
                #     'mountpoint': partition.mountpoint,
                #     'total': partition_info.total,
                #     'used': partition_info.used,
                #     'free': partition_info.free,
                # }
                # drives_info.append(drive_details)
                drives_info.append(f"{partition_info.total / (1024 ** 3):.2f}")
            except Exception as e:
                print(f"Не удалось получить информацию о диске {partition.device}: {e}")
        if len(drives_info) > 0:
            return drives_info

    @staticmethod
    def get_drives_info_usb_test() -> list | None:
        drives_info = []
        partitions = disk_partitions()
        for partition in partitions:
            if isinstance(partition.opts, str):
                if partition.opts.find('removable') == -1:
                    continue

            try:
                partition_info = disk_usage(partition.mountpoint)
                drive_details = {
                    'device': partition.device,
                    'total': partition_info.total,
                    'free': partition_info.free,
                }
                drives_info.append(drive_details)
            except Exception as e:
                pass
        return drives_info

    @staticmethod
    def get_uninitialized_disks():
        return []

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
    def get_data() -> tuple[list, int, int] | None:
        # ram
        result_list = list()
        on_test_count = 0
        is_test_fail_count = 0
        ram_dict = dict()

        def get_checked_string(to_check_string: str, params_type: SYS_INFO_PARAMS) -> tuple[str, bool]:
            saved_string = CSystemInfo.get_test_stats(params_type)
            if isinstance(saved_string, str):
                if len(saved_string):
                    if saved_string == to_check_string:
                        return ("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Сравнение "
                                "успешно!</span>"), True

            return (f"<span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">Сравнение не пройдено!</span> "
                    f"Check_string: {saved_string}"), False

        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.RAM_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.RAM_CHECK) is True:
            memory_info = CSystemInfo.get_memory_info()

            check_string = f"all_{memory_info['total'] / (1024 ** 3):.2f}".replace(" ", "_")

            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.RAM_STRING)

            if not result_test:
                is_test_fail_count += 1

            ram_dict.update({"data": f"{test_name}: Всего: {memory_info['total'] / (1024 ** 3):.2f} | "
                                     f"Доступно: {memory_info['available'] / (1024 ** 3):.2f} | "
                                     f"Использовано: {memory_info['used'] / (1024 ** 3):.2f} ГБ {test_result_string}",

                             "only_data": f"Всего: {memory_info['total'] / (1024 ** 3):.2f} | "
                                          f"Доступно: {memory_info['available'] / (1024 ** 3):.2f} | "
                                          f"Использовано: {memory_info['used'] / (1024 ** 3):.2f} ГБ",

                             "check_string": check_string,
                             "test_id": TEST_SYSTEM_INFO_TYPES.RAM_STATS})
            on_test_count += 1
        else:
            ram_dict.update({"data": f"{test_name}: Проверка отключена",

                             "only_data": f"Проверка отключена",

                             "check_string": "result_none",
                             "test_id": TEST_SYSTEM_INFO_TYPES.RAM_STATS})

        result_list.append(ram_dict)

        bios_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.BIOS_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BIOS_CHECK) is True:
            # BIOS
            bios_info = CSystemInfo.get_bios_info()

            check_string = f"manufacturer_{bios_info['manufacturer']}_" \
                           f"version_{bios_info['version']}_" \
                           f"sn_{bios_info['serial_number']}_" \
                           f"releasedate_{bios_info['release_date']}".replace(" ", "_")

            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.BIOS_STRING)
            if not result_test:
                is_test_fail_count += 1
            bios_dict.update({"data": f"{test_name}: {bios_info['manufacturer']} | {bios_info['version']} | "
                                      f"SN: {bios_info['serial_number']} | Date: {bios_info['release_date']} {test_result_string}",

                              "only_data": f"{bios_info['manufacturer']} | {bios_info['version']} | "
                                           f"SN: {bios_info['serial_number']} | Date: {bios_info['release_date']}",

                              "check_string":
                                  check_string,

                              "test_id": TEST_SYSTEM_INFO_TYPES.BIOS_STATS})
            on_test_count += 1
        else:
            bios_dict.update({"data": f"{test_name}: Проверка отключена",

                              "only_data": f"Проверка отключена",
                              "check_string":
                                  f"result_none",

                              "test_id": TEST_SYSTEM_INFO_TYPES.BIOS_STATS})

        result_list.append(bios_dict)

        #
        # cpu
        cpu_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.CPU_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.CPU_CHECK) is True:

            check_string = f"cpu_{CSystemInfo.get_cpu_info()}".replace(" ", "_")
            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.CPU_STRING)
            if not result_test:
                is_test_fail_count += 1
            cpu_dict.update({"data": f"{test_name}: {CSystemInfo.get_cpu_info()} {test_result_string}",

                             "only_data": f"{CSystemInfo.get_cpu_info()}",
                             "check_string":
                                 check_string,

                             "test_id": TEST_SYSTEM_INFO_TYPES.CPU_STATS})

            on_test_count += 1

        else:
            cpu_dict.update({"data": f"{test_name}: Проверка отключена",

                             "only_data": f"Проверка отключена",
                             "check_string":
                                 f"result_none",

                             "test_id": TEST_SYSTEM_INFO_TYPES.CPU_STATS})

        result_list.append(cpu_dict)

        #
        # OS
        os_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.OS_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.OS_CHECK) is True:
            check_string = f"system_{platform.system()}_" \
                           f"release_{platform.release()}_" \
                           f"version_{platform.version()}_" \
                           f"comp_name_{CSystemInfo.get_computer_name()}".replace(" ", "_")

            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.OS_STRING)
            if not result_test:
                is_test_fail_count += 1
            os_dict.update({"data": f"{test_name}: {platform.system()} {platform.release()} {platform.version()} | "
                                    f"{CSystemInfo.get_computer_name()} {test_result_string}",

                            "check_string":
                                check_string,
                            "only_data": f"{platform.system()} {platform.release()} {platform.version()} | "
                                         f"{CSystemInfo.get_computer_name()}",

                            "test_id": TEST_SYSTEM_INFO_TYPES.OS_STATS})
            on_test_count += 1
        else:
            os_dict.update({"data": f"{test_name}: Проверка отключена",

                            "only_data": f"Проверка отключена",
                            "check_string":
                                f"result_none",

                            "test_id": TEST_SYSTEM_INFO_TYPES.OS_STATS})

        result_list.append(os_dict)

        # # остальные тесты
        # LAN test
        lan_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.LAN_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.LAN_CHECK) is True:

            check_ip = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.LAN_IP)
            response = CSystemInfo.check_lan_connectivity(check_ip)
            is_on = False
            if response is None:
                string = f"{test_name}: IP невалидный"
                ip_check_result = "not_valid_ip"
            elif response is True:
                string = f"{test_name}: пройден успешно!"
                ip_check_result = "success"
                is_on = True
            else:
                string = f"{test_name}: не пройден!"
                ip_check_result = "fail"

            check_string = f"result_{ip_check_result}"
            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.LAN_STRING)
            if not result_test or not is_on:
                is_test_fail_count += 1
            lan_dict.update({"data": string + " " + test_result_string,
                             "only_data": string,
                             "check_string":
                                 check_string,

                             "test_id": TEST_SYSTEM_INFO_TYPES.LAN_STATS})
            on_test_count += 1
        else:
            lan_dict.update({"data": f"{test_name}: Проверка отключена",
                             "only_data": "Проверка отключена",
                             "check_string":
                                 f"result_none",

                             "test_id": TEST_SYSTEM_INFO_TYPES.LAN_STATS})

        result_list.append(lan_dict)

        # WLAN test
        wifi_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.WIFI_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.WLAN_CHECK) is True:

            available_networks = None
            is_on = False
            try:
                available_networks = CSystemInfo.scan_wifi()
                if isinstance(available_networks, list):
                    string = f"{test_name}: пройден успешно! Сети видны: [{", ".join(available_networks)}]"
                    is_on = True
                else:
                    string = f"{test_name}: не пройден! Нет доступных сетей."
            except:
                string = f"{test_name}: WIFI модуль не обнаружен!"

            if not available_networks:
                available_networks = list()

            check_string = f"result_{"success" if len(available_networks) > 0 else "fail"}"

            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.WLAN_STRING)
            if not result_test or not is_on:
                is_test_fail_count += 1
            wifi_dict.update({"data": string + " " + test_result_string,
                              "only_data": string,
                              "check_string":
                                  check_string,

                              "test_id": TEST_SYSTEM_INFO_TYPES.WIFI_STATS})
            on_test_count += 1
        else:
            wifi_dict.update({"data": f"{test_name}: Проверка отключена",
                              "only_data": "Проверка отключена",
                              "check_string":
                                  f"result_none",

                              "test_id": TEST_SYSTEM_INFO_TYPES.WIFI_STATS})

        result_list.append(wifi_dict)

        #
        # BT test
        bt_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.BT_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BT_CHECK) is True:
            bt_result = None
            is_on = False
            try:
                bt_result = CSystemInfo.scan_bluetooth_devices()
                if isinstance(bt_result, list):
                    string = f"{test_name}: пройден успешно! Сети видны: [{", ".join(bt_result)}]."
                    is_on = True
                else:
                    string = f"{test_name}: не пройден! Сети не видны"
            except:
                string = f"{test_name}: BT модуль не обнаружен!"

            if not bt_result:
                bt_result = list()

            check_string = f"result_{"success" if len(bt_result) > 0 else "fail"}"
            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.BT_STRING)
            if not result_test or not is_on:
                is_test_fail_count += 1
            bt_dict.update({"data": string + " " + test_result_string,
                            "only_data": string,
                            "check_string":
                                check_string,

                            "test_id": TEST_SYSTEM_INFO_TYPES.BT_STATS})
            on_test_count += 1
        else:
            bt_dict.update({"data": f"{test_name}: Проверка отключена",
                            "only_data": "Проверка отключена",
                            "check_string":
                                f"result_none",

                            "test_id": TEST_SYSTEM_INFO_TYPES.BT_STATS})

        result_list.append(bt_dict)

        disk_dict = dict()

        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.DISKS_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.DISK_CHECK) is True:
            disk_initials_result_list = None
            is_on = False

            try:
                disk_initials_result_list = CSystemInfo.get_drives_info()
                if isinstance(disk_initials_result_list, list):

                    string = f"{test_name}: пройден успешно! Диски видны: [{", ".join(disk_initials_result_list)}]."
                    is_on = True
                else:
                    string = f"{test_name}: не пройден! Диски не видны"
            except:
                string = f"{test_name}: Диски не обнаружены!"

            test_result_string = str()
            result_test = False
            if len(disk_initials_result_list) > 0:
                check_string = f"drivers_{",".join(disk_initials_result_list)}"
                saved_string = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.DISK_STRING)
                # Список объёмов дисков приходит списокм строк. Тупо объём
                # В строке для сравнения из конфига строка с объёмом через запятую
                # Просто дробим её на отельные списик строк и потом ищем
                # в списке реальных устройств строку с объёмом для каждой строки списка строки сравнения
                if isinstance(saved_string, str):
                    if len(saved_string) > 0:
                        if saved_string.find("drivers_") != -1:
                            try:
                                find_string = saved_string.replace("drivers_", "").split(",")
                                is_all_find = True
                                for find_disk in find_string:
                                    is_find = False
                                    for real_driver in disk_initials_result_list:
                                        if find_disk == real_driver:
                                            is_find = True
                                            # Нашли устройство в реальных устройствах, значит прерываем
                                            break

                                    if not is_find:
                                        # Устройство из списка строк строки сравнения не найдено
                                        # в реальных устройствах
                                        is_all_find = False
                                        break

                                if is_all_find:  # Все строки в списке реальных выданных устройств найдены
                                    result_test = True
                            except:
                                pass
                if not result_test:
                    test_result_string = (
                        f"<span style=\"font-size:14pt;font-weight:700;color:#ff5733;\">Сравнение не пройдено!</span> "
                        f"Check_string: {saved_string}")
            else:
                check_string = f"drivers_fail"

            if result_test:
                test_result_string = ("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Сравнение "
                                      "успешно!</span>")

            if not result_test or not is_on:
                is_test_fail_count += 1

            disk_dict.update({"data": string + " " + test_result_string,
                              "only_data": string,
                              "check_string": check_string,

                              "test_id": TEST_SYSTEM_INFO_TYPES.DISKS_STATS})
            on_test_count += 1
        else:
            disk_dict.update({"data": f"{test_name}: Проверка отключена",
                              "only_data": "Проверка отключена",
                              "check_string":
                                  f"result_none",

                              "test_id": TEST_SYSTEM_INFO_TYPES.DISKS_STATS})

        result_list.append(disk_dict)

        if on_test_count > 0:
            return result_list, is_test_fail_count, on_test_count

        return None

    def load_data(self, data_list: list | None, fails_count: int, all_test_count: int):

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
                # disk
                case TEST_SYSTEM_INFO_TYPES.DISKS_STATS:
                    unit.append(data)

        if all_test_count > 0:
            unit.append(" ")
            if fails_count == 0:
                unit.append("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Тест успешно "
                            "выполнен!</span>")
            else:
                unit.append("<span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">Тест не выполнен!</span>")
        unit.append(f"Всего тестов активировано: {all_test_count}\n"
                    f"Тестов провалено: {fails_count}\n"
                    f"Тестов успешно: {all_test_count - fails_count}\n")

        unit.moveCursor(QTextCursor.Start)

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
