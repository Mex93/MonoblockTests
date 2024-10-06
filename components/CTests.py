from enuuuums import TEST_TYPE, TEST_ARRAY_ID, TEST_RESULT


class CTests:
    tests_params = (
        ["Информация о системе", TEST_TYPE.TEST_SYSTEM_INFO, "test_system_info"],
        ["Кнопки", TEST_TYPE.TEST_HARDWARE_BTN, "test_buttons"],
        ["Динамики и микрофон", TEST_TYPE.TEST_SPEAKER_MIC, "test_speaker_and_micro"],
        ["Дисплей", TEST_TYPE.TEST_DISPLAY, "test_display"],
        ["Второй дисплей", TEST_TYPE.TEST_EXTERNAL_DISPLAY, "test_external_display"],
        ["Наушники и микрофон", TEST_TYPE.TEST_HEADSET_MIC, "test_headset_and_micro"],
        ["Флешки", TEST_TYPE.TEST_REMOVABLE_DEVICE, "test_removable_device"],
        ["Цвета", TEST_TYPE.TEST_BRIGHTNESS, "test_brightness"],
        ["Передняя камера", TEST_TYPE.TEST_FRONT_CAMERA, "test_front_camera"],
    )

    @classmethod
    def get_avalible_test_list(cls) -> list:
        return [TEST_TYPE.TEST_SYSTEM_INFO,
                TEST_TYPE.TEST_EXTERNAL_DISPLAY,
                TEST_TYPE.TEST_SPEAKER_MIC,
                TEST_TYPE.TEST_FRONT_CAMERA,
                TEST_TYPE.TEST_HEADSET_MIC,
                TEST_TYPE.TEST_HARDWARE_BTN,

               ]

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


class CTestUnit:
    def __init__(self, test_type: TEST_TYPE, test_name: str):
        self.__test_type = test_type
        self.__test_name = test_name
        self.Test_result = TEST_RESULT.NONE

    def get_test_type(self) -> TEST_TYPE:
        return self.__test_type

    @property
    def Test_result(self) -> TEST_RESULT:
        """This is 'value' property."""
        return self.__test_result

    @Test_result.setter
    def Test_result(self, test_result: TEST_RESULT):
        self.__test_result = test_result

    # @Test_result.deleter
    # def Test_result(self):
    #     del self.__test_result


class CTestProcess:
    __test_units = list()

    def __init__(self):
        self.__test_launch = False
        self.__current_test_launch = TEST_TYPE.TEST_NONE
        self.__test_avalible_list = list()

        for test in CTests.get_config_block_data():
            test_name, test_type = test

            self.__test_units.append(CTestUnit(test_type, test_name))

    def get_next_test(self, current_test: TEST_TYPE) -> TEST_TYPE | None:

        end_element = self.__test_avalible_list[-1]
        if end_element == current_test:
            return None
        else:
            for index, test in enumerate(self.__test_avalible_list, 0):
                if test == current_test:
                    return self.__test_avalible_list[index + 1]

    def add_test_in_launch(self, test_type: TEST_TYPE):
        self.__test_avalible_list.append(test_type)

    def is_test_launch(self) -> TEST_TYPE:
        if self.__test_launch:
            return self.__current_test_launch

        return TEST_TYPE.TEST_NONE

    def switch_launch_test(self, test_type: TEST_TYPE) -> bool:
        if self.__test_launch:
            if test_type != self.__current_test_launch:
                self.__current_test_launch = test_type
                return True

        return False

    def is_test_in_launch(self, test_type: TEST_TYPE) -> bool:
        for test in self.__test_avalible_list:
            if test == test_type:
                return True

    def remove_test_in_launch(self, test_type: TEST_TYPE):
        # for test in self.__test_avalible_list:
        #     if test == test_type:
        #         is_find = True
        #         continue
        #     new_set.add(test)

        new_list = list(test for test in self.__test_avalible_list if test != test_type)
        self.__test_avalible_list = new_list

    def clear_test_launch(self):
        self.__test_avalible_list.clear()

    def start_test(self, first_start_test: TEST_TYPE) -> bool:
        if not self.__test_launch:
            self.__current_test_launch = first_start_test
            self.__test_launch = True

            return True

    def stop_test(self) -> bool:
        if self.__test_launch:
            self.__test_launch = False
            self.set_default_value()
            return True

    def set_default_value(self):
        self.clear_test_launch()
        self.__current_test_launch = TEST_TYPE.TEST_NONE

    def get_unit_test_id_from_test_type(self, test_type: TEST_TYPE) -> CTestUnit | None:
        for unit in self.__test_units:
            if unit.get_test_type() == test_type:
                return unit

    def get_result_test(self, test_type: TEST_TYPE) -> TEST_RESULT | None:
        unit = self.get_unit_test_id_from_test_type(test_type)
        if unit is not None:
            return unit.Test_result

    def set_result_test(self, test_type: TEST_TYPE, result_status: TEST_RESULT) -> bool:
        unit = self.get_unit_test_id_from_test_type(test_type)
        if unit is not None:
            unit.Test_result = result_status
            return True

    def clear_result_test(self) -> None:
        for unit in self.__test_units:
            unit.Test_result = TEST_RESULT.NONE
