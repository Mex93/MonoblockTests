import configparser
from os import path


class ConfigError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class CMainConfig:

    def __init__(self):
        self.__LAST_CONFIG = ""
        self.__ONLY_CONFIG = ""

        self.__config = configparser.ConfigParser()
        self.__config.add_section('program')
        self.__folder_name = "configs"
        self.__patch = "configs/main.ini"

    def set_default_for_values(self):
        self.__LAST_CONFIG = ''
        self.__ONLY_CONFIG = ''

    def get_config(self):
        self.__config.read(self.__patch, encoding="utf-8")

        self.__LAST_CONFIG = self.__config.get('program', 'LAST_CONFIG_NAME')
        self.__ONLY_CONFIG = self.__config.get('program', 'ONLY_CONFIG_NAME')

    def is_config_created(self):
        if path.isfile(self.__patch) is True:
            return True
        return False

    def save_last_config(self, last_config_name: str):
        with open(self.__patch, 'w') as config_file:
            self.__config.set("program", "LAST_CONFIG_NAME", last_config_name)
            self.__config.write(config_file)

    def create_config(self):
        with open(self.__patch, 'w') as config_file:
            self.__config.set('program', 'LAST_CONFIG_NAME', "-")
            self.__config.set('program', 'ONLY_CONFIG_NAME', "-")

            self.set_default_for_values()
            self.__config.write(config_file)


    def get_only_config_name(self) -> str:
        if self.__ONLY_CONFIG.find("-") != -1:
            return ""
        return self.__ONLY_CONFIG

    def get_last_config_name(self) -> str:
        if self.__LAST_CONFIG.find("-") != -1:
            return ""
        return self.__LAST_CONFIG

    def save_config(self):
        if self.is_config_created() is False:
            with open(self.__patch, 'w') as config_file:
                self.__config.write(config_file)

    def load_data(self):
        if self.is_config_created():
            self.get_config()
        else:
            self.create_config()
            self.get_config()

        return True
