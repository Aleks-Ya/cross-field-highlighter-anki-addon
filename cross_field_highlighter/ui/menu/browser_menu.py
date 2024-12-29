import logging
from logging import Logger

from aqt import QMenu, DialogManager, QDesktopServices
from aqt.addons import AddonManager
from aqt.browser import Browser

from .browser_menu_about_action import BrowserMenuAboutAction
from .browser_menu_open_config import BrowserMenuOpenConfigAction
from .browser_menu_show_latest_modified_notes_action import BrowserMenuShowLatestModifiedNotesAction
from ...config.config import Config
from ...config.settings import Settings
from ...config.url_manager import UrlManager
from ...ui.menu.browser_menu_erase_action import BrowserMenuEraseAction
from ...ui.menu.browser_menu_highlight_action import BrowserMenuHighlightAction
from ...ui.menu.browser_menu_show_highlighted_notes_action import BrowserMenuShowHighlightedNotesAction

log: Logger = logging.getLogger(__name__)


class BrowserMenu(QMenu):

    def __init__(self, browser: Browser, highlight_action: BrowserMenuHighlightAction,
                 erase_action: BrowserMenuEraseAction, addon_manager: AddonManager, dialog_manager: DialogManager,
                 url_manager: UrlManager, desktop_services: QDesktopServices, config: Config,
                 settings: Settings) -> None:
        super().__init__("Cross-Field Highlighter", browser)
        self.addAction(highlight_action)
        self.addAction(erase_action)

        search_action: BrowserMenuShowHighlightedNotesAction = BrowserMenuShowHighlightedNotesAction(browser)
        self.addAction(search_action)

        latest_modified_action: BrowserMenuShowLatestModifiedNotesAction = BrowserMenuShowLatestModifiedNotesAction(
            browser, config)
        self.addAction(latest_modified_action)

        open_config_action: BrowserMenuOpenConfigAction = BrowserMenuOpenConfigAction(
            browser, addon_manager, dialog_manager, settings)
        self.addAction(open_config_action)

        about_action: BrowserMenuAboutAction = BrowserMenuAboutAction(browser, url_manager, desktop_services, settings)
        self.addAction(about_action)

        log.debug(f"{self.__class__.__name__} was instantiated")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
