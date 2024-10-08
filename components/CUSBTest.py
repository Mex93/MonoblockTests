
from PySide6.QtCore import Qt, QTimer


from PySide6.QtWidgets import (QGroupBox, QHBoxLayout,
                               QLabel, QMainWindow,
                               QVBoxLayout)

from enuuuums import USB_TEST_PARAMS, TEST_TYPE
from ui.test_usb_devices import Ui_TestUSBDevicesWindow
from components.CSystemInfoTest import CSystemInfo


class CUSBDevicesTest:
    __test_used = False
    __test_dict = dict()

    @classmethod
    def get_test_stats(cls, test_name: USB_TEST_PARAMS) -> bool | str | None:
        return cls.__test_dict.get(test_name, None)

    @classmethod
    def set_test_stats(cls, test_name: USB_TEST_PARAMS, params: str | bool) -> None:
        cls.__test_dict.update({test_name: params})


class CUSBDevicesTestWindow(QMainWindow):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.__main_window = main_window
        self.ui = Ui_TestUSBDevicesWindow()
        self.ui.setupUi(self)
        self.first_load = True
        self.cdevices = DeviceWindow(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_devices)
        self.ui.pushButton_success.clicked.connect(
            lambda: self.__main_window.on_test_phb_success(TEST_TYPE.TEST_USB_DEVICES))
        self.ui.pushButton_fail.clicked.connect(
            lambda: self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_USB_DEVICES))

        self.ui.pushButton_all_test_break.clicked.connect(
            lambda: self.__main_window.on_test_phb_break_all_test(TEST_TYPE.TEST_USB_DEVICES))

        self.control_str = str()

        self.setWindowTitle(f'Меню теста')

    def update_devices(self):
        try:
            drivers = CSystemInfo.get_drives_info_usb_test()
            if len(drivers) > 0:
                set_rebuild = False

                if self.first_load:
                    self.control_str = ""
                    Table.clear()
                    Table.set_init()
                    self.first_load = False
                    set_rebuild = True

                max_size = int(CUSBDevicesTest.get_test_stats(USB_TEST_PARAMS.MAX_SIZE))
                if set_rebuild:
                    for driver in drivers:
                        total = f"{driver['total'] / (1024 ** 3):.2f}"
                        if driver['total'] / (1024 ** 3) > max_size:
                            continue

                        device = driver['device']
                        free = f"{driver['free'] / (1024 ** 3):.2f}"
                        check_string = f"{device}_{total}"

                        self.cdevices.create_element(f"Накопитель '{device}'", f"Объём: {total} ГБ",
                                                     f"Свободно: {free} ГБ")
                        self.control_str += check_string

                else:
                    devices_str = str()
                    for driver in drivers:
                        total = f"{driver['total'] / (1024 ** 3):.2f}"
                        if driver['total'] / (1024 ** 3) > max_size:
                            continue

                        device = driver['device']
                        check_string = f"{device}_{total}"
                        devices_str += check_string

                    if devices_str != self.control_str:
                        self.cdevices.destroy_elements()
                        self.first_load = True
                    else:
                        pass
        except:
            self.__main_window.on_test_phb_fail(TEST_TYPE.TEST_USB_DEVICES)

    def window_show(self) -> bool:
        try:
            drivers = CSystemInfo.get_drives_info_usb_test()
            max_size = int(CUSBDevicesTest.get_test_stats(USB_TEST_PARAMS.MAX_SIZE))
            if len(drivers) and 1 < max_size < 1000:
                self.first_load = True
                self.timer.start(1004)
                self.show()
                return True
        except:
            pass

        return False

    def closeEvent(self, e):
        self.timer.stop()
        e.accept()


class DeviceUnit:
    """
    Комплекс виджетов формирующих окошко
    """

    def __init__(self, element_index: int, main_window: CUSBDevicesTestWindow, char_disk: str, max_space: str,
                 current_space: str):
        self.__char_disk = char_disk
        self.__max_space = max_space
        self.__current_space = current_space
        self.__main_window = main_window

        self.groupBox_2_disk_1 = QGroupBox(main_window.ui.groupBox)
        self.groupBox_2_disk_1.setObjectName(f"groupBox_2_disk_{element_index}")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2_disk_1)
        self.horizontalLayout_2.setObjectName(f"horizontalLayout_2_disk_{element_index}")
        self.verticalLayout_disk_1 = QVBoxLayout()
        self.verticalLayout_disk_1.setObjectName(f"verticalLayout_disk_{element_index}")
        self.label_drive_type_disk_1 = QLabel(self.groupBox_2_disk_1)
        self.label_drive_type_disk_1.setObjectName(f"label_drive_type_disk_{element_index}")

        self.verticalLayout_disk_1.addWidget(self.label_drive_type_disk_1)

        self.label_max_space_disk_1 = QLabel(self.groupBox_2_disk_1)
        self.label_max_space_disk_1.setObjectName(f"label_max_space_disk_{element_index}")

        self.verticalLayout_disk_1.addWidget(self.label_max_space_disk_1)

        self.label_current_space_disk_1 = QLabel(self.groupBox_2_disk_1)
        self.label_current_space_disk_1.setObjectName(f"label_current_space_disk_{element_index}")

        self.verticalLayout_disk_1.addWidget(self.label_current_space_disk_1)

        self.horizontalLayout_2.addLayout(self.verticalLayout_disk_1)
        col, row = Table.get_empty_place()
        main_window.ui.gridLayout.addWidget(self.groupBox_2_disk_1, col, row, 1, 1)

        self.groupBox_2_disk_1.setTitle(char_disk)
        self.label_max_space_disk_1.setText(max_space)
        self.label_current_space_disk_1.setText(current_space)
        self.label_drive_type_disk_1.setText("LOCAL STORAGE")

    def delete_item(self):
        self.groupBox_2_disk_1.deleteLater()


class DeviceWindow:
    """
    Главная таблица с виджетами устройств
    """
    __devices_units = []
    __uniq_index = 2

    def __init__(self, main_window: CUSBDevicesTestWindow):
        self.__count_devices = 0
        self.__main = main_window

    def create_element(self, char_disk: str, max_space: str, current_space: str) -> DeviceUnit:
        unit = DeviceUnit(self.__uniq_index, self.__main, char_disk, max_space, current_space)
        self.__uniq_index += 1
        self.__devices_units.append(unit)

        return unit

    def destroy_elements(self):
        self.__uniq_index = 0
        for element in self.__devices_units:
            element.delete_item()

        self.__devices_units.clear()


class Table:
    """
    Положение виджета
    """
    __table = list()
    MAX_COLUMN = 4
    MAX_ROWS = 3

    @classmethod
    def set_init(cls):
        for column in range(0, Table.MAX_COLUMN):
            rows_list = []
            for row in range(0, Table.MAX_COLUMN):
                rows_list.append(False)
            Table.__table.append(rows_list)

    @classmethod
    def clear(cls):
        cls.__table.clear()

    @classmethod
    def get_empty_place(cls) -> tuple[int, int]:
        for col_index, col_list in enumerate(cls.__table, 0):
            for row_index, row in enumerate(col_list, 0):
                if row is False:
                    cls.__table[col_index][row_index] = True
                    return col_index, row_index
