
class CSystemInfo:

    __test_used = False
    __bios_string = ""
    __cpu_string = ""
    __ram_string = ""
    __disks_string = ""
    __bios_stats = None
    __cpu_stats = None
    __ram_stats = None
    __disks_stats = None

    @classmethod
    def is_test_used(cls) -> bool:
        return cls.__test_used

    @classmethod
    def set_test_used(cls, used: bool):
        cls.__test_used = used

    @classmethod
    def set_bios_stats(cls, value: bool):
        cls.__bios_stats = value

    @classmethod
    def get_bios_stats(cls) -> bool:
        return cls.__bios_stats

    ########
    @classmethod
    def set_cpu_stats(cls, value: bool):
        cls.__cpu_stats = value

    @classmethod
    def get_cpu_stats(cls) -> bool:
        return cls.__cpu_stats

    ########
    @classmethod
    def set_ram_stats(cls, value: bool):
        cls.__ram_stats = value

    @classmethod
    def get_ram_stats(cls) -> bool:
        return cls.__ram_stats

    @classmethod
    ########
    def set_disk_stats(cls, value: bool):
        cls.__disks_stats = value

    @classmethod
    def get_disk_stats(cls) -> bool:
        return cls.__disks_stats
