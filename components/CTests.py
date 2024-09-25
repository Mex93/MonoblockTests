from enuuuums import TEST_TYPE, TEST_ARRAY_ID


class CTests:
    tests_params = (
        ["Информация о системе", TEST_TYPE.TEST_SYSTEM_INFO, "test_system_info"],
        ["Кнопки", TEST_TYPE.TEST_HARDWARE_BTN, "test_buttons"],
        ["Динамики и микро", TEST_TYPE.TEST_SPEAKER_MIC, "test_speaker_and_micro"],
        ["Дисплей", TEST_TYPE.TEST_DISPLAY, "test_display"],
        ["Второй дисплей", TEST_TYPE.TEST_EXTERNAL_DISPLAY, "test_external_display"],
        ["Наушники и микро", TEST_TYPE.TEST_HEADSET_MIC, "test_headset_and_micro"],
        ["Флешки", TEST_TYPE.TEST_REMOVABLE_DEVICE, "test_removable_device"],
        ["Цвета", TEST_TYPE.TEST_BRIGHTNESS, "test_brightness"],
        ["Передняя камера", TEST_TYPE.TEST_FRONT_PHOTO, "test_front_phonto"],
        ["Bluetooth", TEST_TYPE.TEST_BLUETOOTH, "test_bluetooth"],
        ["LAN", TEST_TYPE.TEST_LAN_PORT, "test_lan_port"],
        ["WIFI", TEST_TYPE.TEST_WIFI, "test_wifi"],
    )

    @classmethod
    def get_test_name_from_test_type(cls, test_type: TEST_TYPE) -> str | None:
        for test in cls.tests_params:
            if test[TEST_ARRAY_ID.ARRAY_TYPE] == test_type:
                return test[TEST_ARRAY_ID.ARRAY_NAME]

    @classmethod
    def get_test_type_from_name(cls, test_name: str) -> TEST_TYPE | None:
        for test in cls.tests_params:
            if test[TEST_ARRAY_ID.ARRAY_NAME] == test_name:
                return test[TEST_ARRAY_ID.ARRAY_TYPE]

    @classmethod
    def get_array_index_from_test_type(cls, test_type: TEST_TYPE) -> int:
        """
        -1 if not find
        :param test_type:
        :return:
        """
        for index, test in enumerate(cls.tests_params):
            if test[TEST_ARRAY_ID.ARRAY_TYPE] == test_type:
                return index

        return -1

    @classmethod
    def get_config_block_names_list(cls) -> list | None:
        rlist = list()
        for test in cls.tests_params:
            rlist.append(test[TEST_ARRAY_ID.ARRAY_CONFIG_BLOCK_NAME])

        if len(rlist):
            return rlist

    @classmethod
    def get_config_block_data(cls) -> list | None:
        rlist = list()
        for test in cls.tests_params:
            rlist.append([test[TEST_ARRAY_ID.ARRAY_NAME], test[TEST_ARRAY_ID.ARRAY_TYPE]])

        if len(rlist):
            return rlist

    @classmethod
    def get_config_block_name_from_test_type(cls, test_type: TEST_TYPE) -> str | None:
        arr_index = cls.get_array_index_from_test_type(test_type)
        if arr_index != -1:
            return cls.tests_params[arr_index][TEST_ARRAY_ID.ARRAY_CONFIG_BLOCK_NAME]

