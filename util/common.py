import os
import platform


PLATFORM = platform.system()

CONFIGS = {
    'Windows': {'cp_order': 'copy', },
    'Darwin': {'cp_order': 'cp', },
    'Linux': dict()
}


class PlatformConfig:
    def __init__(self):
        self.platform = PLATFORM
        for k, v in CONFIGS.get(self.platform).items():
            assert isinstance(k, str)
            setattr(self, k, v)

    def platform_is_block(self, cur_plat: str):
        return not cur_plat == self.platform


global_config = PlatformConfig()


if __name__ == '__main__':
    print(global_config.__dict__)
