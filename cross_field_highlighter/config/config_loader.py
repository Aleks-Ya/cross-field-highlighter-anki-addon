import logging
from logging import Logger
from typing import Optional

from aqt.addons import AddonManager

from ..config.config import Config, ConfigData
from ..config.settings import Settings

log: Logger = logging.getLogger(__name__)


class ConfigLoader:

    def __init__(self, addon_manager: AddonManager, settings: Settings) -> None:
        self.__module_name: str = settings.module_name
        self.__addon_manager: AddonManager = addon_manager
        log.debug(f"{self.__class__.__name__} was instantiated")

    def load_config(self) -> ConfigData:
        log.debug(f"Loading config for module {self.__module_name}")
        defaults_opts: Optional[ConfigData] = self.get_defaults()
        actual_opt: Optional[ConfigData] = self.__addon_manager.getConfig(self.__module_name)
        joined: ConfigData = Config.join(defaults_opts, actual_opt)
        self.__addon_manager.writeConfig(self.__module_name, joined)
        return joined

    def get_defaults(self) -> Optional[ConfigData]:
        defaults: Optional[ConfigData] = self.__addon_manager.addonConfigDefaults(self.__module_name)
        log.debug(f"Getting defaults for module {self.__module_name}: {defaults}")
        return defaults

    def write_config(self, config_data: ConfigData) -> None:
        log.debug(f"Writing config for module {self.__module_name}: {config_data}")
        self.__addon_manager.writeConfig(self.__module_name, config_data)
