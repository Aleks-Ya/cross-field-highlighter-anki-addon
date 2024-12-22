import logging
from logging import Logger
from typing import Optional

from aqt import qconnect, QAction, DialogManager
from aqt.addons import AddonManager, AddonsDialog, ConfigEditor
from aqt.browser import Browser

from ...config.settings import Settings

log: Logger = logging.getLogger(__name__)


class BrowserMenuOpenConfigAction(QAction):

    def __init__(self, browser: Browser, addon_manager: AddonManager, dialog_manager: DialogManager,
                 settings: Settings) -> None:
        super().__init__("Configuration...", browser)
        self.__browser: Browser = browser
        self.__addon_manager: AddonManager = addon_manager
        self.__dialog_manager: DialogManager = dialog_manager
        self.__settings: Settings = settings
        qconnect(self.triggered, self.__on_click)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self):
        log.debug("On open configuration dialog")
        addons_dialog: AddonsDialog = self.__dialog_manager.open("AddonsDialog", self.__addon_manager)
        conf: Optional[dict[str, any]] = self.__addon_manager.getConfig(self.__settings.module_name)
        ConfigEditor(addons_dialog, self.__settings.module_name, conf)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
