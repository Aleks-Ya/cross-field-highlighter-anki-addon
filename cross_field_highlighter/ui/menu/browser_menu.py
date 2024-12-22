import logging
from logging import Logger

from aqt import QMenu, DialogManager
from aqt.addons import AddonManager
from aqt.browser import Browser

from .browser_menu_open_config import BrowserMenuOpenConfigAction
from .browser_menu_show_latest_modified_notes_action import BrowserMenuShowLatestModifiedNotesAction
from ...config.config import Config
from ...config.settings import Settings
from ...ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from ...ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
from ...ui.menu.browser_menu_erase_action import BrowserMenuEraseAction
from ...ui.menu.browser_menu_highlight_action import BrowserMenuHighlightAction
from ...ui.menu.browser_menu_show_highlighted_notes_action import BrowserMenuShowHighlightedNotesAction
from ...ui.menu.dialog_params_factory import DialogParamsFactory
from ...ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenu(QMenu):

    def __init__(self, browser: Browser, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController, dialog_params_factory: DialogParamsFactory,
                 addon_manager: AddonManager, dialog_manager: DialogManager, config: Config,
                 settings: Settings) -> None:
        super().__init__("Cross-Field Highlighter", browser)

        highlight_action: BrowserMenuHighlightAction = BrowserMenuHighlightAction(
            browser, op_factory, adhoc_highlight_dialog_controller, dialog_params_factory)
        self.addAction(highlight_action)

        erase_action: BrowserMenuEraseAction = BrowserMenuEraseAction(
            browser, op_factory, adhoc_erase_dialog_controller, dialog_params_factory)
        self.addAction(erase_action)

        search_action: BrowserMenuShowHighlightedNotesAction = BrowserMenuShowHighlightedNotesAction(browser)
        self.addAction(search_action)

        latest_modified_action: BrowserMenuShowLatestModifiedNotesAction = BrowserMenuShowLatestModifiedNotesAction(
            browser, config)
        self.addAction(latest_modified_action)

        open_config_action: BrowserMenuOpenConfigAction = BrowserMenuOpenConfigAction(
            browser, addon_manager, dialog_manager, settings)
        self.addAction(open_config_action)

        log.debug(f"{self.__class__.__name__} was instantiated")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
