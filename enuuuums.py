from enum import IntEnum, auto


class SMBOX_ICON_TYPE(IntEnum):
    ICON_NONE = auto(),
    ICON_WARNING = auto(),
    ICON_ERROR = auto(),
    ICON_INFO = auto()


class TEST_ARRAY_ID(IntEnum):
    ARRAY_NAME = 0,
    ARRAY_TYPE = 1,
    ARRAY_CONFIG_BLOCK_NAME = 2,


class TEST_TYPE(IntEnum):
    TEST_NONE = auto(),
    TEST_SYSTEM_INFO = auto(),
    TEST_HARDWARE_BTN = auto(),
    TEST_SPEAKER_MIC = auto(),
    TEST_DISPLAY = auto(),
    TEST_EXTERNAL_DISPLAY = auto(),
    TEST_HEADSET_MIC = auto(),
    TEST_REMOVABLE_DEVICE = auto(),
    TEST_BRIGHTNESS = auto(),
    TEST_FRONT_PHOTO = auto(),
    TEST_BLUETOOTH = auto(),
    TEST_LAN_PORT = auto(),
    TEST_WIFI = auto(),


class TEST_SYSTEM_INFO_TYPES(IntEnum):
    BIOS_STATS = auto(),
    CPU_STATS = auto(),
    RAM_STATS = auto(),
    DISKS_STATS = auto(),
