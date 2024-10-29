import logging
from logging import Logger

from aqt import qconnect, QAction
from aqt.browser import Browser

log: Logger = logging.getLogger(__name__)


class BrowserMenuSearchHighlightedNotesAction(QAction):

    def __init__(self, browser: Browser) -> None:
        super().__init__("Show highlighted notes in Browser", browser)
        self.__browser: Browser = browser
        qconnect(self.triggered, self.__on_click)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self):
        log.debug("On search for highlighted notes click")
        self.__browser.search_for("cross-field-highlighter")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
