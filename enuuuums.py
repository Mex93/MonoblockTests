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


class AUDIO_CHANNEL(IntEnum):
    CHANNEL_NONE = auto(),
    CHANNEL_LEFT = auto(),
    CHANNEL_RIGHT = auto(),
    CHANNEL_ALL = auto(),


class AUDIO_TEST_RECORD_STATE(IntEnum):
    STATE_NONE = auto(),
    STATE_RECORD = auto(),
    STATE_PLAY = auto(),


class AUDIO_STATUS(IntEnum):
    STATUS_NONE = auto(),
    STATUS_PLAY = auto(),
    STATUS_STOP = auto(),

class AUDIO_TEST_STEP(IntEnum):
    STEP_NONE = auto(),
    STEP_RECORD = auto(),
    STEP_LEFT_CHANNEL = auto(),
    STEP_RIGHT_CHANNEL = auto(),

class TEST_TYPE(IntEnum):
    TEST_NONE = auto(),
    TEST_SYSTEM_INFO = auto(),
    TEST_HARDWARE_BTN = auto(),
    TEST_SPEAKER_MIC = auto(),
    TEST_PATTERNS = auto(),
    TEST_EXTERNAL_DISPLAY = auto(),
    TEST_HEADSET_MIC = auto(),
    TEST_USB_DEVICES = auto(),
    TEST_BRIGHTNESS = auto(),
    TEST_FRONT_CAMERA = auto(),
    TEST_BLUETOOTH = auto(),
    TEST_LAN_PORT = auto(),
    TEST_WIFI = auto(),


class TEST_SYSTEM_INFO_TYPES(IntEnum):
    BIOS_STATS = auto(),
    CPU_STATS = auto(),
    RAM_STATS = auto(),
    DISKS_STATS = auto(),
    OS_STATS = auto(),
    LAN_STATS = auto(),
    WIFI_STATS = auto(),
    BT_STATS = auto(),


class BLOCKS_DATA:
    PROGRAM_SETTING = "program"
    SYS_INFO_TEST = "sys_info_test"
    EXTERNAL_DISPLAY_TEST = "external_display_test"
    SPEAKER_TEST = "speaker_test"
    VIDEO_CAM_TEST = "videocam_test"
    HARDWARE_BTN_TEST = "hardw_keys_test"
    BRIGHTNESS_TEST = "brightness_test"
    USB_DEVICE_TEST = "usb_devices_test"
    PATTERNS_TEST = "patterns_test"


class CONFIG_PARAMS:
    CONFIG_NAME = "config_name"
    DISPLAY_RESOLUTION = "display_resolution"


class SYS_INFO_PARAMS:
    TEST_USED = "test_used"
    BIOS_CHECK = "bios_check"
    CPU_CHECK = "cpu_check"
    RAM_CHECK = "ram_check"
    DISK_CHECK = "disk_check"
    WLAN_CHECK = "wlan_check"
    BT_CHECK = "bt_check"
    LAN_CHECK = "lan_check"
    OS_CHECK = "os_check"

    LAN_IP = "lan_ip"

    OS_STRING = "os_string"
    BIOS_STRING = "bios_string"
    CPU_STRING = "cpu_string"
    RAM_STRING = "ram_string"
    DISK_STRING = "disk_string"
    WLAN_STRING = "wlan_string"
    BT_STRING = "bt_string"
    LAN_STRING = "lan_string"


class EXTERNAL_DISPLAY_PARAMS:
    TEST_USED = "test_used"
    VIDEO_PATCH = "video_patch"
    WINDOW_DEFAULT = "window_switch_def"
    WINDOW_SWITCH_TO = "window_switch_to"


class VIDEO_CAM_PARAMS:
    TEST_USED = "test_used"
    CAMERA_INDEX = "camera_index"


class KEYSBUTTOMS_PARAMS:
    TEST_USED = "test_used"


class BRIGHTNESS_PARAMS:
    TEST_USED = "test_used"
    FILE_PATCH = "file_patch"


class USB_TEST_PARAMS:
    TEST_USED = "test_used"
    MAX_SIZE = "max_size_find"


class PATTERNS_TEST_PARAMS:
    TEST_USED = "test_used"


class SPEAKER_PARAMS:
    SPEAKER_TEST_USED = "test_used"
    HEADSET_TEST_USED = "test_used"
    AUDIO_PATCH_LEFT = "audio_patch_left"
    AUDIO_PATCH_RIGHT = "audio_patch_right"


class TEST_RESULT(IntEnum):
    NONE = auto(),
    SUCCESS = auto(),
    FAIL = auto(),


class KEY_PRESSED_TYPE(IntEnum):
    NONE = auto(),
    KEY_VOL_PLUS = auto(),
    KEY_VOL_MINUS = auto(),