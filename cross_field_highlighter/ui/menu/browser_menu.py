import logging
from logging import Logger

from aqt import QMenu
from aqt.browser import Browser

from cross_field_highlighter.ui.menu.browser_menu_erase_action import BrowserMenuEraseAction
from cross_field_highlighter.ui.menu.browser_menu_highlight_action import BrowserMenuHighlightAction
from cross_field_highlighter.ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenu(QMenu):

    def __init__(self, browser: Browser, op_factory: OpFactory) -> None:
        super().__init__("Cross-Field Highlighter", browser)
        highlight_action: BrowserMenuHighlightAction = BrowserMenuHighlightAction(browser, op_factory)
        self.addAction(highlight_action)

        erase_action: BrowserMenuEraseAction = BrowserMenuEraseAction(browser, op_factory)
        self.addAction(erase_action)

        log.debug(f"{self.__class__.__name__} was instantiated")
