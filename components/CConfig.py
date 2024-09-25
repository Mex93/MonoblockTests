import configparser
from os import path, listdir

from components.CTests import TEST_TYPE, CTests


class ConfigError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class CConfig:
    __folder_name = "configs"
    __config_path = ""
    __config_name = ""
    __main_config = None

    __in_config_name = ""

    #####
    sys_info_test_used = ""
    bios_string = ""
    cpu_string = ""
    ram_string = ""
    disks_string = ""
    bios_stats = None
    cpu_stats = None
    ram_stats = None
    disks_stats = None
    #####
    __config_handler = None

    @classmethod
    def set_init_config(cls, config_file_name: str) -> bool:
        config_path = f'{cls.get_folder_name()}/{config_file_name}'

        if cls.is_config_created(config_path):
            cls.__config_name = config_file_name
            cls.__config_path = config_path

            handler = cls.create_config_handler()
            handler.add_section('program_settings')
            block_name = CTests.get_config_block_name_from_test_type(TEST_TYPE.TEST_SYSTEM_INFO)
            handler.add_section(block_name)

            cls.__main_config = handler
            return True
        return False

    @classmethod
    def get_config_path(cls) -> str:
        return cls.__config_path

    @classmethod
    def get_config_text_name(cls) -> str:
        return cls.__in_config_name

    @classmethod
    def get_folder_name(cls) -> str:
        return cls.__folder_name

    @classmethod
    def is_config_created(cls, file_patch=None) -> bool:
        if file_patch is not None:
            if path.isfile(file_patch):
                return True
        else:
            if path.isfile(cls.__config_path):
                return True
        return False

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

    @classmethod
    def create_config_handler(cls) -> configparser:
        return configparser.ConfigParser()

    @classmethod
    def get_config_handler(cls) -> configparser:
        return cls.__main_config

    @classmethod
    def load_config(cls):
        handler = cls.get_config_handler()
        if handler is not None:

            if not CConfig.is_config_created():
                return
            cpatch = CConfig.get_config_path()

            handler.read(cpatch, encoding="utf-8")

            cls.__in_config_name = handler.get("program_settings", "config_name")

            ###
            block_name = CTests.get_config_block_name_from_test_type(TEST_TYPE.TEST_SYSTEM_INFO)
            cls.sys_info_test_used = bool(handler.get(block_name, "sys_info_test_used"))
            cls.bios_stats = bool(handler.get(block_name, "bios_check"))
            cls.cpu_stats = bool(handler.get(block_name, "cpu_check"))
            cls.ram_stats = bool(handler.get(block_name, "ram_check"))
            cls.disks_stats = bool(handler.get(block_name, "disk_check"))
            cls.bios_string = handler.get(block_name, "bios_string")
            cls.cpu_string = handler.get(block_name, "cpu_string")
            cls.ram_string = handler.get(block_name, "ram_string")
            cls.disks_string = handler.get(block_name, "disk_string")

    @classmethod
    def create_config_data(cls):
        handler = cls.get_config_handler()
        if handler is not None:

            if not CConfig.is_config_created():
                return

            cpatch = CConfig.get_config_path()
            with open(cpatch, 'w') as config_file:

                handler.set("program_settings", "config_name", "-")
                ##

                block_name = CTests.get_config_block_name_from_test_type(TEST_TYPE.TEST_SYSTEM_INFO)
                handler.set(block_name, "sys_info_test_used", "true")
                handler.set(block_name, "bios_check", "true")
                handler.set(block_name, "cpu_check", "true")
                handler.set(block_name, "ram_check", "true")
                handler.set(block_name, "disk_check", "true")
                handler.set(block_name, "bios_string", "-")
                handler.set(block_name, "cpu_string", "-")
                handler.set(block_name, "ram_string", "-")
                handler.set(block_name, "disk_string", "-")
                handler.write(config_file)

    @classmethod
    def save_config(cls):
        handler = cls.get_config_handler()
        if handler is not None:
            cpatch = CConfig.get_config_path()
            with open(cpatch, 'w') as config_file:
                handler.write(config_file)



