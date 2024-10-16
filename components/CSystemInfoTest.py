# import ipaddress
import platform
import subprocess
from os import system
from socket import AF_INET

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QTextCursor
from PySide6.QtWidgets import QMainWindow
from bluetooth import discover_devices
from psutil import disk_partitions, virtual_memory, disk_usage, net_if_addrs
from win32com.client import GetObject
from wmi import WMI

from components.CErrorLabel import TestResultLabel

from enuuuums import TEST_TYPE, TEST_SYSTEM_INFO_TYPES, SYS_INFO_PARAMS
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
            case TEST_SYSTEM_INFO_TYPES.MB_STATS:
                return "МП"
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

    @classmethod
    def get_tests_list(cls) -> list:
        tests = [TEST_SYSTEM_INFO_TYPES.BT_STATS,
                 TEST_SYSTEM_INFO_TYPES.MB_STATS,
                 TEST_SYSTEM_INFO_TYPES.OS_STATS,
                 TEST_SYSTEM_INFO_TYPES.CPU_STATS,
                 TEST_SYSTEM_INFO_TYPES.WIFI_STATS,
                 TEST_SYSTEM_INFO_TYPES.LAN_STATS,
                 TEST_SYSTEM_INFO_TYPES.RAM_STATS,
                 TEST_SYSTEM_INFO_TYPES.BIOS_STATS,
                 TEST_SYSTEM_INFO_TYPES.DISKS_STATS]

        return tests

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
            drives.append([partition.device, partition.maxfile])

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
                # print(f"Не удалось получить информацию о диске {partition.device}: {e}")
                pass
        if len(drives_info) > 0:
            return drives_info

    @staticmethod
    def get_drives_info_usb_test() -> list | None:
        drives_info = []
        partitions = disk_partitions()
        for partition in partitions:
            try:
                partition_info = disk_usage(partition.mountpoint)
                drive_details = {
                    'device': partition.device,
                    'total': partition_info.total,
                    'free': partition_info.free,
                }
                drives_info.append(drive_details)
            except:
                pass
        if len(drives_info) > 0:
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
        c = WMI()
        # Получение информации о системе
        total_memory = 0

        for memory in c.Win32_PhysicalMemory():
            total_memory += int(memory.Capacity)

        return total_memory

    @staticmethod
    def get_memory_info_old():

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
        # logging.basicConfig(level=logging.INFO, filename="bios_params.log", filemode="a",
        #                     format="%(asctime)s %(levelname)s %(message)s")

        # bios_properties = [
        #     bios_info.BiosCharacteristics,  # Характеристики BIOS
        #     bios_info.BIOSVersion,  # Версия BIOS
        #     bios_info.BuildNumber,  # Номер сборки
        #     bios_info.Caption,  # Заголовок
        #     bios_info.CodeSet,  # Набор кодов
        #     bios_info.CurrentLanguage,  # Текущий язык
        #     bios_info.Description,  # Описание
        #     bios_info.EmbeddedControllerMajorVersion,  # Основная версия встроенного контроллера
        #     bios_info.EmbeddedControllerMinorVersion,  # Небольшая версия встроенного контроллера
        #     bios_info.IdentificationCode,  # Код идентификации
        #     bios_info.InstallableLanguages,  # Устанавливаемые языки
        #     bios_info.InstallDate,  # Дата установки
        #     bios_info.LanguageEdition,  # Версия языка
        #     bios_info.ListOfLanguages,  # Список языков
        #     bios_info.Manufacturer,  # Производитель
        #     bios_info.Name,  # Имя
        #     bios_info.OtherTargetOS,  # Другие целевые операционные системы
        #     bios_info.PrimaryBIOS,  # Основной BIOS
        #     bios_info.ReleaseDate,  # Дата выпуска
        #     bios_info.SerialNumber,  # Серийный номер
        #     bios_info.SMBIOSBIOSVersion,  # Версия BIOS SMBIOS
        #     bios_info.SMBIOSMajorVersion,  # Основная версия SMBIOS
        #     bios_info.SMBIOSMinorVersion,  # Небольшая версия SMBIOS
        #     bios_info.SMBIOSPresent,  # Наличие SMBIOS
        #     bios_info.SoftwareElementID,  # Идентификатор программного элемента
        #     bios_info.SoftwareElementState,  # Состояние программного элемента
        #     bios_info.Status,  # Статус
        #     bios_info.SystemBiosMajorVersion,  # Основная версия системного BIOS
        #     bios_info.SystemBiosMinorVersion,  # Небольшая версия системного BIOS
        #     bios_info.TargetOperatingSystem,  # Целевая операционная система
        #     bios_info.Version  # Версия
        # ]

        # # Печать списка для проверки
        # for prop in bios_properties:
        #     logging.info(f"Параметр {str(prop)} -> {prop}")
        # baseboard_attributes = [
        #     "baseboard.Caption",
        #     "baseboard.ConfigOptions",
        #     "baseboard.CreationClassName",
        #     "baseboard.Depth",
        #     "baseboard.Description",
        #     "baseboard.Height",
        #     "baseboard.HostingBoard",
        #     "baseboard.HotSwappable",
        #     "baseboard.InstallDate",
        #     "baseboard.Manufacturer",
        #     "baseboard.Model",
        #     "baseboard.Name",
        #     "baseboard.OtherIdentifyingInfo",
        #     "baseboard.PartNumber",
        #     "baseboard.PoweredOn",
        #     "baseboard.Product",
        #     "baseboard.Removable",
        #     "baseboard.Replaceable",
        #     "baseboard.RequirementsDescription",
        #     "baseboard.RequiresDaughterBoard",
        #     "baseboard.SerialNumber",
        #     "baseboard.SKU",
        #     "baseboard.SlotLayout",
        #     "baseboard.SpecialRequirements",
        #     "baseboard.Status",
        #     "baseboard.Tag",
        #     "baseboard.Version",
        #     "baseboard.Weight",
        #     "baseboard.Width"
        # ]

        # for baseboard in c.Win32_BaseBoard():
        #     logging.info(baseboard)
        #     logging.info(f"baseboard.Caption {baseboard.Caption}")
        #     logging.info(f"baseboard.ConfigOptions {baseboard.ConfigOptions}")
        #     logging.info(f"baseboard.CreationClassName {baseboard.CreationClassName}")
        #     logging.info(f"baseboard.Depth {baseboard.Depth}")
        #     logging.info(f"baseboard.Description {baseboard.Description}")
        #     logging.info(f"baseboard.Height {baseboard.Height}")
        #     logging.info(f"baseboard.HostingBoard {baseboard.HostingBoard}")
        #     logging.info(f"baseboard.HotSwappable {baseboard.HotSwappable}")
        #     logging.info(f"baseboard.InstallDate {baseboard.InstallDate}")
        #     logging.info(f"baseboard.Manufacturer {baseboard.Manufacturer}")
        #     logging.info(f"baseboard.Model {baseboard.Model}")
        #     logging.info(f"baseboard.Name {baseboard.Name}")
        #     logging.info(f"baseboard.OtherIdentifyingInfo {baseboard.OtherIdentifyingInfo}")
        #     logging.info(f"baseboard.PartNumber {baseboard.PartNumber}")
        #     logging.info(f"baseboard.PoweredOn {baseboard.PoweredOn}")
        #     logging.info(f"baseboard.Product {baseboard.Product}")
        #     logging.info(f"baseboard.Removable {baseboard.Removable}")
        #     logging.info(f"baseboard.Replaceable {baseboard.Replaceable}")
        #     logging.info(f"baseboard.RequirementsDescription {baseboard.RequirementsDescription}")
        #     logging.info(f"baseboard.RequiresDaughterBoard {baseboard.RequiresDaughterBoard}")
        #     logging.info(f"baseboard.SerialNumber {baseboard.SerialNumber}")
        #     logging.info(f"baseboard.SKU {baseboard.SKU}")
        #     logging.info(f"baseboard.SlotLayout {baseboard.SlotLayout}")
        #     logging.info(f"baseboard.SpecialRequirements {baseboard.SpecialRequirements}")
        #     logging.info(f"baseboard.Status {baseboard.Status}")
        #     logging.info(f"baseboard.Tag {baseboard.Tag}")
        #     logging.info(f"baseboard.Version {baseboard.Version}")
        #     logging.info(f"baseboard.Weight {baseboard.Weight}")
        #     logging.info(f"baseboard.Width {baseboard.Width}")

        # for systems in c.Win32_ComputerSystem():
        #     print(f"Manufacturer: {systems.Manufacturer}")
        #     print(f"Model: {systems.Model}")
        #
        # for baseboard in c.Win32_BaseBoard():
        #     print(f"Manufacturer: {baseboard.Manufacturer}")
        #     print(f"Product: {baseboard.OtherIdentifyingInfo}")
        cs_model = ""
        cs_system_family = ""
        cs_system_sku_number = ""
        for systems in c.Win32_ComputerSystem():
            cs_model = systems.Model
            cs_system_family = systems.SystemFamily
            cs_system_sku_number = systems.SystemSKUNumber

        return {
            'manufacturer': bios_info.Manufacturer,
            'version': bios_info.Version,
            'serial_number': bios_info.SerialNumber,
            'release_date': bios_info.ReleaseDate,  # bios_info.ReleaseDate
            'cs_model': cs_model,
            'cs_system_family': cs_system_family,
            'cs_system_sku_number': cs_system_sku_number,
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
            # ip_object = ipaddress.ip_address(ip)
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

    @classmethod
    def compare_two_list(cls, list_in_find: list, list_find: list) -> bool:
        # в списке list_in_find найден элеименты из list_find
        if all(isinstance(lst, list) for lst in (list_in_find, list_find)):
            count_find = 0
            count_of_list_find = len(list_find)
            if count_of_list_find:
                for item_in_find in list_in_find:
                    for item_find in list_find:
                        if item_in_find == item_find:
                            count_find += 1
                            break
                    if count_find == count_of_list_find:
                        break
                if count_find == count_of_list_find:
                    return True
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

    @classmethod
    def clear_all_test_in_error_label(cls):
        tests = CSystemInfo.get_tests_list()
        for test in tests:
            TestResultLabel.delete_test(CSystemInfo.get_sub_test_name_from_type(test))

    @classmethod
    def add_test_in_error(cls, test_params: TEST_SYSTEM_INFO_TYPES):
        TestResultLabel.add_text(CSystemInfo.get_sub_test_name_from_type(test_params))

    def set_default_string(self):
        unit = self.ui.textBrowser_lan_port
        unit.clear()
        unit.append("Получение результатов...")

        self.ui.label_ram_info.setText("-")
        self.ui.label_bios_info.setText("-")
        self.ui.label_mb_info.setText("-")
        self.ui.label_cpu_info.setText("-")
        self.ui.label_os_info.setText("-")

    @classmethod
    def get_data(cls, error_label_used=True) -> tuple[list, int, int, int] | None:
        # ram
        result_list = list()
        on_test_count = 0
        is_test_passed_count = 0
        is_test_fail_string_check_count = 0
        ram_dict = dict()

        def get_checked_string(to_check_string: str, params_type: SYS_INFO_PARAMS) -> tuple[str, bool | None]:
            saved_string = CSystemInfo.get_test_stats(params_type)
            if isinstance(saved_string, str):
                if saved_string == "-" or not len(saved_string):
                    return (""), None
                else:
                    if len(saved_string):
                        if saved_string == to_check_string:
                            return ("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Сравнение "
                                    "успешно!</span>"), True

            return (
                f"<span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">Сравнение не пройдено!</span><br>"
                f"Check_string: {saved_string}"), False

        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.RAM_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.RAM_CHECK) is True:
            total = CSystemInfo.get_memory_info()

            # total = memory_info.get("total", None)
            # available = memory_info.get("available", None)
            # used = memory_info.get("used", None)

            check_string = f"all_{total / (1024 ** 3):.0f}".replace(" ", "_")

            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.RAM_STRING)

            if total is not None:
                is_test_passed_count += 1
            else:
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.RAM_STATS)

            if result_test is False:  # не пройдено сравнение
                is_test_fail_string_check_count += 1
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.RAM_STATS)
            elif result_test is None:  # сравнение не надо
                pass

            ram_dict.update({
                "data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Всего: {total / (1024 ** 3):.0f} ГБ {test_result_string}",

                "only_data": f"Всего: {total / (1024 ** 3):.0f} ГБ",

                "check_string": check_string,
                "test_id": TEST_SYSTEM_INFO_TYPES.RAM_STATS})

            # ram_dict.update({
            #     "data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Всего: {total / (1024 ** 3):.2f} | "
            #             f"Доступно: {available / (1024 ** 3):.2f} | "
            #             f"Использовано: {used / (1024 ** 3):.2f} ГБ {test_result_string}",
            #
            #     "only_data": f"Всего: {total / (1024 ** 3):.2f} | "
            #                  f"Доступно: {available / (1024 ** 3):.2f} | "
            #                  f"Использовано: {used / (1024 ** 3):.2f} ГБ",
            #
            #     "check_string": check_string,
            #     "test_id": TEST_SYSTEM_INFO_TYPES.RAM_STATS})

            on_test_count += 1
        else:
            ram_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",

                 "only_data": f"Проверка отключена",

                 "check_string": "result_none",
                 "test_id": TEST_SYSTEM_INFO_TYPES.RAM_STATS})

        result_list.append(ram_dict)

        bios_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.BIOS_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BIOS_CHECK) is True:
            # BIOS
            bios_info = CSystemInfo.get_bios_info()
            manufacturer = bios_info.get("manufacturer", None)
            version = bios_info.get("version", None)
            serial_number = bios_info.get("serial_number", None)
            release_date = bios_info.get("release_date", None)
            # if None not in (manufacturer, version, serial_number, release_date):
            #     is_test_passed_count += 1
            if None not in (manufacturer, version, serial_number, release_date):
                is_test_passed_count += 1
            else:
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.BIOS_STATS)

            # check_string = f"m_{'-' if manufacturer is None else manufacturer}_" \
            #                f"v_{'-' if version is None else version}_" \
            #                f"sn_{'-' if serial_number is None else serial_number}_" \
            #                f"rd_{'-' if release_date is None else release_date}" \
            #                f"cm_{'-' if cs_model is None else cs_model}" \
            #                f"sf_{'-' if cs_system_family is None else cs_system_family}" \
            #                f"sskn_{'-' if cs_system_sku_number is None else cs_system_sku_number}".replace(" ", "_")

            check_string = f"m_{'-' if manufacturer is None else manufacturer}".replace(" ", "_")

            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.BIOS_STRING)

            if result_test is False:  # не пройдено сравнение
                is_test_fail_string_check_count += 1
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.BIOS_STATS)
            elif result_test is None:  # сравнение не надо
                pass

            # bios_dict.update({"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> {manufacturer} | {version} | "
            #                           f"SN: {serial_number} | Vendor: {cs_model}-{cs_system_family}-{cs_system_sku_number} <br> Date: {release_date} {test_result_string}",
            #
            #                   "only_data": f"{manufacturer} | {version} | "
            #                                f"SN: {serial_number} | Vendor: {cs_model}-{cs_system_family}-{cs_system_sku_number} | Date: {release_date}",
            #
            #                   "check_string":
            #                       check_string,
            #
            #                   "test_id": TEST_SYSTEM_INFO_TYPES.BIOS_STATS})

            bios_dict.update({
                "data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> {manufacturer} {test_result_string}",

                "only_data": f"{manufacturer}",

                "check_string":
                    check_string,

                "test_id": TEST_SYSTEM_INFO_TYPES.BIOS_STATS})

            on_test_count += 1
        else:
            bios_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",

                 "only_data": f"Проверка отключена",
                 "check_string":
                     f"result_none",

                 "test_id": TEST_SYSTEM_INFO_TYPES.BIOS_STATS})

        result_list.append(bios_dict)

        # MB Test
        mb_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.MB_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.MB_CHECK) is True:

            bios_info = CSystemInfo.get_bios_info()
            cs_model = bios_info.get("cs_model", None)
            cs_system_family = bios_info.get("cs_system_family", None)
            cs_system_sku_number = bios_info.get("cs_system_sku_number", None)

            if None not in (cs_model, cs_system_family, cs_system_sku_number):
                is_test_passed_count += 1
            else:
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.MB_STATS)

            mb_model_string = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.MB_MODEL_STRING)
            mb_family_string = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.MB_FAMILY_STRING)
            mb_sku_number_string = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.MB_SKU_NUMBER_STRING)

            not_compared_list = list()
            in_test_used_strings_list = list()

            in_result_list = [[SYS_INFO_PARAMS.MB_MODEL_STRING, cs_model],
                              [SYS_INFO_PARAMS.MB_FAMILY_STRING, cs_system_family],
                              [SYS_INFO_PARAMS.MB_SKU_NUMBER_STRING, cs_system_sku_number],
                              ]

            for string_tuple in ((mb_model_string, cs_model, "Model", SYS_INFO_PARAMS.MB_MODEL_STRING),
                                 (mb_family_string, cs_system_family, "Family", SYS_INFO_PARAMS.MB_FAMILY_STRING),
                                 (mb_sku_number_string, cs_system_sku_number, "SKUN",
                                  SYS_INFO_PARAMS.MB_SKU_NUMBER_STRING)):

                in_config_string, mb_string, block_name, string_config_name = string_tuple
                if isinstance(in_config_string, str):
                    if not len(in_config_string) or in_config_string == "-":
                        continue

                    in_test_used_strings_list.append([mb_string, string_config_name])

                    if in_config_string != mb_string:
                        not_compared_list.append([block_name, in_config_string])

            if not len(in_test_used_strings_list):
                mb_dict.update({
                    "data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Model: {cs_model} "
                            f"Family: {cs_system_family}  SKUN: {cs_system_sku_number} <span style=\"font-size:14pt;font-weight:700;color:#ff5733;\">Нет данных в файле конфигурации для проверки!</span>",

                    "only_data": f"Model: {cs_model} Family: {cs_system_family} SKUN: {cs_system_sku_number}",

                    "check_string":
                        "result_none",

                    "test_id": TEST_SYSTEM_INFO_TYPES.MB_STATS})
                on_test_count += 1
            else:
                check_string = list()
                for item in in_result_list:
                    check_string.append(f"{item[0]} = {item[1]}")

                if len(not_compared_list):  # если по сравнению у нас что то прилетело и плохо сравнилось
                    result_string = list()

                    for item in not_compared_list:
                        result_string.append(f"{item[0]}: {item[1]}")

                    mb_dict.update({
                        "data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Model: {cs_model} "
                                f"Family: {cs_system_family} SKUN: {cs_system_sku_number} "
                                f"<span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">Сравнение не пройдено!</span><br>"
                                f"Не пройдено: {', '.join(result_string)}",

                        "only_data": f"Model: {cs_model} Family: {cs_system_family} SKUN: {cs_system_sku_number}",

                        "check_string":
                            f"\n{'\n'.join(check_string)}",

                        "test_id": TEST_SYSTEM_INFO_TYPES.MB_STATS})
                    is_test_fail_string_check_count += 1
                    if error_label_used:
                        cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.MB_STATS)
                else:

                    mb_dict.update({
                        "data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Model: {cs_model} "
                                f"Family: {cs_system_family} SKUN: {cs_system_sku_number} "
                                f"<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Сравнение "
                                "успешно!</span>",

                        "only_data": f"Model: {cs_model} Family: {cs_system_family} SKUN: {cs_system_sku_number}",

                        "check_string":
                            f"\n{'\n'.join(check_string)}",

                        "test_id": TEST_SYSTEM_INFO_TYPES.MB_STATS})
                on_test_count += 1

        else:
            mb_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",

                 "only_data": f"Проверка отключена",
                 "check_string":
                     f"result_none",

                 "test_id": TEST_SYSTEM_INFO_TYPES.MB_STATS})

        result_list.append(mb_dict)

        #
        # cpu
        cpu_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.CPU_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.CPU_CHECK) is True:

            cpu_name = CSystemInfo.get_cpu_info()
            if isinstance(cpu_name, str):
                if len(cpu_name) > 0:
                    is_test_passed_count += 1

            check_string = f"cpu_{cpu_name}".replace(" ", "_")
            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.CPU_STRING)

            if result_test is False:  # не пройдено сравнение
                is_test_fail_string_check_count += 1
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.CPU_STATS)
            elif result_test is None:  # сравнение не надо
                pass

            cpu_dict.update({
                "data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> {cpu_name} {test_result_string}",

                "only_data": f"{cpu_name}",
                "check_string":
                    check_string,

                "test_id": TEST_SYSTEM_INFO_TYPES.CPU_STATS})

            on_test_count += 1

        else:
            cpu_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",

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

            csystem = platform.system()
            crelease = platform.release()
            cversion = platform.version()
            ccomputer_name = CSystemInfo.get_computer_name()

            if isinstance(csystem, str):
                if len(csystem):
                    is_test_passed_count += 1

            check_string = f"system_{csystem}_" \
                           f"release_{crelease}_" \
                           f"version_{cversion}_" \
                           f"comp_name_{ccomputer_name}".replace(" ", "_")

            test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.OS_STRING)

            if result_test is False:  # не пройдено сравнение
                is_test_fail_string_check_count += 1
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.OS_STATS)
            elif result_test is None:  # сравнение не надо
                pass

            os_dict.update({
                "data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> {csystem} {crelease} {cversion} | "
                        f"{ccomputer_name} {test_result_string}",

                "check_string":
                    check_string,
                "only_data": f"{csystem} {crelease} {cversion} | "
                             f"{ccomputer_name}",

                "test_id": TEST_SYSTEM_INFO_TYPES.OS_STATS})
            on_test_count += 1
        else:
            os_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",

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

            if response is None:
                string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">не пройден - </span> IP невалидный."
                string_not_span = f"{test_name}: не пройден - IP невалидный"
                ip_check_result = "not_valid_ip"
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.LAN_STATS)
            elif response is True:
                string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#0000ff;\">пройден успешно</span>!"
                string_not_span = f"{test_name}: пройден успешно!"
                ip_check_result = "success"
                is_test_passed_count += 1
            else:
                string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">не пройден</span>!"
                string_not_span = f"{test_name}: не пройден!"
                ip_check_result = "fail"
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.LAN_STATS)

            check_string = f"result_{ip_check_result}"
            # test_result_string, result_test = get_checked_string(check_string, SYS_INFO_PARAMS.LAN_STRING)

            # отключено полностью сравнение для лан
            # if result_test is False:  # не пройдено сравнение
            #     is_test_fail_string_check_count += 1
            #     if error_label_used:
            #         cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.LAN_STATS)
            # elif result_test is None:  # сравнение не надо
            #     pass

            lan_dict.update({"data": string,  # + test_result_string
                             "only_data": string_not_span,
                             "check_string":
                                 check_string,

                             "test_id": TEST_SYSTEM_INFO_TYPES.LAN_STATS})
            on_test_count += 1
        else:
            lan_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",
                 "only_data": "Проверка отключена",
                 "check_string":
                     f"result_none",

                 "test_id": TEST_SYSTEM_INFO_TYPES.LAN_STATS})

        result_list.append(lan_dict)

        # WLAN test --------------------------------------------
        wifi_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.WIFI_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.WLAN_CHECK) is True:
            is_any_avalable_networks = False
            available_networks = None
            wf_string = ""
            try:
                available_networks = CSystemInfo.scan_wifi()
                if isinstance(available_networks, list):
                    # : [{", ".join(available_networks)}]
                    string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#0000ff;\">пройден успешно</span>!"
                    # : [{", ".join(available_networks)}]
                    wf_string = f"Сети: {",".join(available_networks)}"
                    string_not_span = f"{test_name}: пройден успешно! Сети видны."
                    check_string = f"wlans_{",".join(available_networks)}"
                    is_test_passed_count += 1
                    is_any_avalable_networks = True
                else:
                    string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">не пройден</span>! Нет доступных сетей."
                    string_not_span = f"{test_name}: не пройден! Нет доступных сетей."
                    check_string = "wlans_none"
                    if error_label_used:
                        cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.WIFI_STATS)
            except:
                string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> WIFI модуль <span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">не обнаружен</span>!"
                string_not_span = f"{test_name}: WIFI модуль не обнаружен!"
                check_string = "wlans_error_none"
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.WIFI_STATS)

            test_result_string = ""
            saved_string = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.WLAN_STRING)
            if isinstance(saved_string, str) and (saved_string == "-" or not len(saved_string)):
                pass
            else:
                compare_check_result = False
                if is_any_avalable_networks:
                    if isinstance(saved_string, str):
                        if len(saved_string) > 0:
                            if saved_string.find("wlans_") != -1:
                                if available_networks is not None:
                                    try:
                                        find_string = saved_string.replace("wlans_", "").split(",")
                                        if CSystemInfo.compare_two_list(available_networks, find_string):
                                            compare_check_result = True
                                    except:
                                        pass
                if compare_check_result:
                    test_result_string = ("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Сравнение "
                                          "успешно!</span>")
                else:
                    test_result_string = (
                        f" {wf_string} <span style=\"font-size:14pt;font-weight:700;color:#ff5733;\">Сравнение не пройдено!</span> "
                        f"Check_string: {saved_string}")
                    is_test_fail_string_check_count += 1
                    if error_label_used:
                        cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.WIFI_STATS)

            wifi_dict.update({"data": string + " " + test_result_string,
                              "only_data": string_not_span,
                              "check_string":
                                  check_string,

                              "test_id": TEST_SYSTEM_INFO_TYPES.WIFI_STATS})
            on_test_count += 1
        else:
            wifi_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",
                 "only_data": "Проверка отключена",
                 "check_string":
                     f"result_none",

                 "test_id": TEST_SYSTEM_INFO_TYPES.WIFI_STATS})

        result_list.append(wifi_dict)

        #
        # BT test ----------------------------------------
        bt_dict = dict()
        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.BT_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BT_CHECK) is True:
            available_networks = None
            string = ""
            string_not_span = ""
            is_any_avalable_networks = False
            check_string = ""
            bts_string = ""
            try:
                available_networks = CSystemInfo.scan_bluetooth_devices()
                if isinstance(available_networks, list):
                    # : [{", ".join(available_networks)}]
                    bts_string = f"Сети: {",".join(available_networks)}"
                    string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#0000ff;\">пройден успешно</span>!"
                    # : [{", ".join(available_networks)}]
                    string_not_span = f"{test_name}: пройден успешно! Сети видны."
                    check_string = f"bts_{",".join(available_networks)}"
                    is_test_passed_count += 1
                    is_any_avalable_networks = True
                elif isinstance(available_networks, bool):
                    if available_networks is False:
                        string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">не пройден</span>! Сети не видны или модуль не подключен!"
                        string_not_span = f"{test_name}: не пройден! Сети не видны или модуль не подключен!"
                        check_string = "bts_none"
                        if error_label_used:
                            cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.BT_STATS)
            except:
                string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> BT модуль <span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">не обнаружен</span>!"
                string_not_span = f"{test_name}: BT модуль не обнаружен!"
                check_string = "bts_error_none"
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.BT_STATS)

            test_result_string = ""
            saved_string = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BT_STRING)
            if isinstance(saved_string, str) and (saved_string == "-" or not len(saved_string)):
                pass
            else:
                compare_check_result = False
                if is_any_avalable_networks:
                    if isinstance(saved_string, str):
                        if len(saved_string) > 0:
                            if saved_string.find("bts_") != -1:
                                if available_networks is not None:
                                    try:
                                        find_string = saved_string.replace("bts_", "").split(",")
                                        if CSystemInfo.compare_two_list(available_networks, find_string):
                                            compare_check_result = True
                                    except:
                                        pass
                if compare_check_result:
                    test_result_string = ("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Сравнение "
                                          "успешно!</span>")
                else:
                    test_result_string = (
                        f" {bts_string} <span style=\"font-size:14pt;font-weight:700;color:#ff5733;\">Сравнение не пройдено!</span> "
                        f"Check_string: {saved_string}")
                    is_test_fail_string_check_count += 1
                    if error_label_used:
                        cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.BT_STATS)

            bt_dict.update({"data": string + " " + test_result_string,
                            "only_data": string_not_span,
                            "check_string":
                                check_string,

                            "test_id": TEST_SYSTEM_INFO_TYPES.BT_STATS})
            on_test_count += 1
        else:
            bt_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",
                 "only_data": "Проверка отключена",
                 "check_string":
                     f"result_none",

                 "test_id": TEST_SYSTEM_INFO_TYPES.BT_STATS})

        result_list.append(bt_dict)

        #  DISK test____________________________
        disk_dict = dict()

        test_name = CSystemInfo.get_sub_test_name_from_type(TEST_SYSTEM_INFO_TYPES.DISKS_STATS)
        if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.DISK_CHECK) is True:
            disk_initials_result_list = None
            disks_string = ""
            try:
                disk_initials_result_list = CSystemInfo.get_drives_info()
                if isinstance(disk_initials_result_list, list):
                    disks_string = f"Диски: [{", ".join(disk_initials_result_list)}]"
                    string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#0000ff;\">пройден успешно</span>!"
                    # string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#0000ff;\">пройден успешно</span>! Диски видны: [{", ".join(disk_initials_result_list)}]."
                    # string_not_span = f"{test_name}: пройден успешно! Диски видны: [{", ".join(disk_initials_result_list)}]."
                    string_not_span = f"{test_name}: пройден успешно! Диски видны"
                    is_test_passed_count += 1
                else:
                    string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> <span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">не пройден</span>! Диски не видны."
                    string_not_span = f"{test_name}: не пройден! Диски не видны"
                    if error_label_used:
                        cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.DISKS_STATS)
            except:
                string = f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Диски <span style=\" font-size:14pt; font-weight:700; color:#FF0000;\">не обнаружены</span>!"
                string_not_span = f"{test_name}: Диски не обнаружены!"
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.DISKS_STATS)
            test_result_string = str()
            result_test = False
            if len(disk_initials_result_list) > 0:
                check_string = f"drivers_{",".join(disk_initials_result_list)}"
                saved_string = CSystemInfo.get_test_stats(SYS_INFO_PARAMS.DISK_STRING)
                # Список объёмов дисков приходит списокм строк. Тупо объём
                # В строке для сравнения из конфига строка с объёмом через запятую
                # Просто дробим её на отельные списик строк и потом ищем
                # в списке реальных устройств строку с объёмом для каждой строки списка строки сравнения

                if isinstance(saved_string, str) and (saved_string == "-" or not len(saved_string)):
                    result_test = None
                else:
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
                            f" {disks_string} <span style=\"font-size:14pt;font-weight:700;color:#ff5733;\">Сравнение не пройдено!</span> "
                            f"Check_string: {saved_string}")
            else:
                check_string = f"drivers_fail"

            if result_test:
                test_result_string = ("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Сравнение "
                                      "успешно!</span>")

            if result_test is False:  # не пройдено сравнение
                is_test_fail_string_check_count += 1
                if error_label_used:
                    cls.add_test_in_error(TEST_SYSTEM_INFO_TYPES.DISKS_STATS)
            elif result_test is None:  # сравнение не надо
                test_result_string = ""

            disk_dict.update({"data": string + " " + test_result_string,
                              "only_data": string_not_span,
                              "check_string": check_string,

                              "test_id": TEST_SYSTEM_INFO_TYPES.DISKS_STATS})
            on_test_count += 1
        else:
            disk_dict.update(
                {"data": f"<span style=\" font-size:14pt; font-weight:700;\">{test_name}:</span> Проверка отключена",
                 "only_data": "Проверка отключена",
                 "check_string":
                     f"result_none",

                 "test_id": TEST_SYSTEM_INFO_TYPES.DISKS_STATS})

        result_list.append(disk_dict)

        if on_test_count > 0:
            return result_list, on_test_count, is_test_passed_count, is_test_fail_string_check_count

        return None

    def load_data(self, data_list: list | None, on_test_count: int, is_test_passed_count: int,
                  is_test_fail_string_check_count: int):

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
                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.RAM_CHECK) is True:
                        self.ui.label_ram_info.setHidden(False)
                        self.ui.label_ram_info.setText(data)
                    else:
                        self.ui.label_ram_info.setHidden(True)

                # bios
                case TEST_SYSTEM_INFO_TYPES.BIOS_STATS:

                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BIOS_CHECK) is True:
                        self.ui.label_mb_info.setHidden(False)
                        self.ui.label_mb_info.setText(data)
                    else:
                        self.ui.label_mb_info.setHidden(True)

                # mb
                case TEST_SYSTEM_INFO_TYPES.MB_STATS:

                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.MB_CHECK) is True:
                        self.ui.label_bios_info.setHidden(False)
                        self.ui.label_bios_info.setText(data)
                    else:
                        self.ui.label_bios_info.setHidden(True)

                # cpu
                case TEST_SYSTEM_INFO_TYPES.CPU_STATS:
                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.CPU_CHECK) is True:
                        self.ui.label_cpu_info.setHidden(False)
                        self.ui.label_cpu_info.setText(data)
                    else:
                        self.ui.label_cpu_info.setHidden(True)
                # os
                case TEST_SYSTEM_INFO_TYPES.OS_STATS:

                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.OS_CHECK) is True:
                        self.ui.label_os_info.setHidden(False)
                        self.ui.label_os_info.setText(data)
                    else:
                        self.ui.label_os_info.setHidden(True)

                # остальные тесты
                # lan
                case TEST_SYSTEM_INFO_TYPES.LAN_STATS:
                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.LAN_CHECK) is True:
                        unit.append(data)
                # wifi
                case TEST_SYSTEM_INFO_TYPES.WIFI_STATS:
                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.WLAN_CHECK) is True:
                        unit.append(data)
                # BT
                case TEST_SYSTEM_INFO_TYPES.BT_STATS:
                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.BT_CHECK) is True:
                        unit.append(data)
                # disk
                case TEST_SYSTEM_INFO_TYPES.DISKS_STATS:
                    if CSystemInfo.get_test_stats(SYS_INFO_PARAMS.DISK_CHECK) is True:
                        unit.append(data)

        if on_test_count > 0:
            unit.append(" ")
            if is_test_passed_count == on_test_count and is_test_fail_string_check_count == 0:
                unit.append("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Тест успешно "
                            "выполнен!</span>")
            else:
                unit.append("<span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">Тест не выполнен!</span>")
        unit.append(f"Всего тестов активировано: {on_test_count}\n"
                    f"Тестов провалено: {on_test_count - is_test_passed_count}\n"
                    f"Тестов сравнений строк провалено: {is_test_fail_string_check_count}\n"
                    f"Тестов успешно: {is_test_passed_count}\n")

        unit.moveCursor(QTextCursor.MoveOperation.Start)

    def closeEvent(self, e):
        if TestResultLabel.is_any_element():
            if not TestResultLabel.is_label_show():
                TestResultLabel.set_show_status(True)
        else:
            TestResultLabel.set_show_status(False)
            TestResultLabel.clear_text()
        self.__main_window.on_call_in_close_test_window(TEST_TYPE.TEST_SYSTEM_INFO)
        e.accept()


class SysInfoMain:

    def __init__(self, test_type: TEST_SYSTEM_INFO_TYPES, is_compared: bool):
        self._test_type = test_type
        self._result = False
        self._test_compared_string = str()
        self._test_result_compared = None
        self._is_compared_activ = is_compared
        self._test_name = CSystemInfo.get_sub_test_name_from_type(test_type)

    def is_compared_activ(self) -> bool:
        return self._is_compared_activ

    def get_name(self) -> str:
        return self._test_name

    def get_result_compared(self) -> tuple[bool | None, str]:
        return self._test_result_compared, self._test_compared_string

    def get_result_test(self) -> bool:
        return self._result

    def set_test_now(self):
        raise "Не переопределён метод для теста"

    def _get_check_string(self, check_string: str, params_type: SYS_INFO_PARAMS):
        self._test_result_compared = None
        self._test_compared_string = ""

        test_result_string, result_test = self._get_checked_string(check_string, params_type)

        if result_test is False:  # не пройдено сравнение
            self._test_compared_string = test_result_string
            self._test_result_compared = False

        elif result_test is None:  # сравнение не надо
            self._test_compared_string = ""
            self._test_result_compared = None
        else:
            self._test_compared_string = test_result_string
            self._test_result_compared = True

    @classmethod
    def _get_checked_string(cls, to_check_string: str, params_type: SYS_INFO_PARAMS) -> tuple[str, bool | None]:
        saved_string = CSystemInfo.get_test_stats(params_type)
        if isinstance(saved_string, str):
            if saved_string == "-" or not len(saved_string):
                return "", None
            else:
                if len(saved_string):
                    if saved_string == to_check_string:
                        return ("<span style=\" font-size:14pt; font-weight:700; color:#8fdd60;\">Сравнение "
                                "успешно!</span>"), True

        return (
            f"<span style=\" font-size:14pt; font-weight:700; color:#ff5733;\">Сравнение не пройдено!</span><br>"
            f"Check_string: {saved_string}"), False


class SysInfoTestBIOS(SysInfoMain):

    def __init__(self, test_type: TEST_SYSTEM_INFO_TYPES, is_compared: bool):
        super().__init__(test_type, is_compared)
        self.manufacturer = None
        self.version = None
        self.serial_number = None
        self.release_date = None

    def set_test_now(self):
        bios_info = CSystemInfo.get_bios_info()
        manufacturer = bios_info.get("manufacturer", None)
        version = bios_info.get("version", None)
        serial_number = bios_info.get("serial_number", None)
        release_date = bios_info.get("release_date", None)

        self.manufacturer = manufacturer
        self.version = version
        self.serial_number = serial_number
        self.release_date = release_date
        # if None not in (manufacturer, version, serial_number, release_date):
        #     is_test_passed_count += 1
        if None not in (manufacturer, version, serial_number, release_date):
            self._result = True
        else:
            self._result = False

        if self.is_compared_activ():
            check_string = f"m_{'-' if manufacturer is None else manufacturer}".replace(" ", "_")
            self._get_check_string(check_string, SYS_INFO_PARAMS.BIOS_STRING)
