import logging
from logging import Logger

from aqt import qconnect, QAction
from aqt.browser import Browser
from aqt.utils import show_warning

from ...config.config import Config

log: Logger = logging.getLogger(__name__)


class BrowserMenuShowLatestModifiedNotesAction(QAction):

    def __init__(self, browser: Browser, config: Config) -> None:
        super().__init__("Show notes modified by latest run", browser)
        self.__browser: Browser = browser
        self.__config: Config = config
        qconnect(self.triggered, self.__on_click)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self):
        log.debug("On search for notes by latest operation click")
        if self.__config.get_latest_modified_notes_enabled():
            self.__browser.search_for(f"tag:{self.__config.get_latest_modified_notes_tag()}")
        else:
            show_warning("Marking latest modified notes is disabled in configuration.")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
