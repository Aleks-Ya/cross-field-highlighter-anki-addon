import logging
from logging import Logger

from aqt import qconnect, QAction, QDesktopServices, QWidget

from ..about.about_view import AboutView
from ...config.settings import Settings
from ...config.url_manager import UrlManager

log: Logger = logging.getLogger(__name__)


class BrowserMenuAboutAction(QAction):

    def __init__(self, parent: QWidget, url_manager: UrlManager, desktop_services: QDesktopServices,
                 settings: Settings) -> None:
        super().__init__("About...", parent)
        self.__about_view: AboutView = AboutView(parent, url_manager, desktop_services, settings)
        qconnect(self.triggered, self.__on_click)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self):
        log.debug("On search for notes by latest operation click")
        self.__about_view.show_view()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
