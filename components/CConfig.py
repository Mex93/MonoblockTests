import configparser
from os import path, listdir
from components.CExternalDisplay import CExternalDisplay
from enuuuums import CONFIG_PARAMS, SYS_INFO_PARAMS, BLOCKS_DATA, EXTERNAL_DISPLAY_PARAMS


class ConfigError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class CParameters:
    __blocks_sets = set()
    __parameters_sets = set()

    def __init__(self, block_name: str, params_name: str, data_type: type, default_value: str):
        self.__blocks_sets.add(block_name)
        self.__parameters_sets.add(params_name)

        self.__blockname = block_name
        self.__param_name = params_name
        self.__data_type = data_type
        self.__default_value = default_value

    def get_params_name(self) -> str:
        return self.__param_name

    def get_blocks_name(self) -> str:
        return self.__blockname

    def get_data_type(self) -> type:
        return self.__data_type

    def get_default_value(self) -> str:
        return self.__default_value

    @classmethod
    def get_blocks_list(cls) -> list:
        return list(cls.__blocks_sets)


class CNewConfig:
    __folder_name = "configs"
    __data_units: list[CParameters] = list()

    def __init__(self):
        self.__config_file_name = ""
        config_unit = configparser.ConfigParser()
        self.__config_unit = config_unit
        self.__data_dict = dict()
        self.__load_sections = False

    def set_init_config(self, config_file_name: str) -> bool:
        config_path = f'{self.get_folder_name()}/{config_file_name}'

        if self.is_config_created(config_path):
            self.__config_file_name = config_file_name

            return True
        return False

    def set_config_file_name(self, config_name: str):
        self.__config_file_name = config_name

    def get_config_file_name(self) -> str:
        return self.__config_file_name

    def get_config_patch(self) -> str:
        return f"{self.get_folder_name()}/{self.__config_file_name}"

    def get_config_handler(self) -> configparser:
        return self.__config_unit

    def is_config_created(self, file_patch=None) -> bool:
        if file_patch is not None:
            if path.isfile(file_patch):
                return True
        else:
            if path.isfile(self.get_config_patch()):
                return True
        return False

    def load_config(self):
        patch = self.get_config_patch()
        handler = self.get_config_handler()
        handler.read(patch, encoding="utf-8")
        self.__data_dict.clear()
        for unit in self.__data_units:
            bname = unit.get_blocks_name()
            pname = unit.get_params_name()
            dtype = unit.get_data_type()

            var = dtype(handler.get(bname, pname))
            self.__data_dict.update({f'{bname}-{pname}': var})

    def get_config_value(self, block_name: str, param_name: str) -> None | int | str | bool:
        return self.__data_dict.get(f'{block_name}-{param_name}', None)

    def create_config_data(self):
        patch = self.get_config_patch()
        handler = self.get_config_handler()
        with open(patch, 'w') as config_file:
            for unit in self.__data_units:
                bname = unit.get_blocks_name()
                pname = unit.get_params_name()
                dvalue = unit.get_default_value()
                handler.set(bname, pname, dvalue)
            ##
            handler.write(config_file)

    def save_config(self):
        with open(self.get_config_patch(), 'w') as config_file:
            self.get_config_handler().write(config_file)

    @classmethod
    def get_configs_list_in_folder(cls) -> list | None:
        files = listdir(cls.get_folder_name())

        filtred_files = list()
        for file in files:
            if len(file):
                if file.find(".ini") != -1:
                    filtred_files.append(file)
        if len(filtred_files):
            return filtred_files

        return None

    def init_params(self):

        self.add_params(BLOCKS_DATA.PROGRAM_SETTING, CONFIG_PARAMS.CONFIG_NAME, str, "-")

        #sys info
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.SYS_INFO_TEST_USED, bool, "true")

        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.BIOS_CHECK, bool, "true")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.CPU_CHECK, bool, "true")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.RAM_CHECK, bool, "true")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.DISK_CHECK, bool, "true")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.WLAN_CHECK, bool, "true")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.BT_CHECK, bool, "true")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.LAN_CHECK, bool, "true")

        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.BIOS_STRING, str, "-")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.CPU_STRING, str, "-")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.RAM_STRING, str, "-")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.DISK_STRING, str, "-")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.WLAN_STRING, str, "-")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.BT_STRING, str, "-")
        self.add_params(BLOCKS_DATA.SYS_INFO_TEST, SYS_INFO_PARAMS.LAN_STRING, str, "-")

        # external display
        self.add_params(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST, EXTERNAL_DISPLAY_PARAMS.EXTD_TEST_USED, bool, "true")
        self.add_params(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST, EXTERNAL_DISPLAY_PARAMS.VIDEO_PATCH, str, "content/external_display_vid.mp4")

        monitor_mode_list = CExternalDisplay.get_monitor_mode_avalible()
        self.add_params(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST, EXTERNAL_DISPLAY_PARAMS.WINDOW_DEFAULT, str,
                        f"extend \n; {",".join(monitor_mode_list)}")
        self.add_params(BLOCKS_DATA.EXTERNAL_DISPLAY_TEST, EXTERNAL_DISPLAY_PARAMS.WINDOW_SWITCH_TO, str,
                        f"clone \n; {",".join(monitor_mode_list)}")

        blist = CParameters.get_blocks_list()
        for block in blist:
            self.__config_unit.add_section(block)

    @classmethod
    def get_folder_name(cls) -> str:
        return cls.__folder_name

    @classmethod
    def add_params(cls, block_name: str, params_name: str, data_type: type, default_value: str):
        new_block = CParameters(block_name, params_name, data_type, default_value)
        cls.__data_units.append(new_block)
