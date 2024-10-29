import logging
from logging import Logger

from aqt import QMenu
from aqt.browser import Browser

from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.menu.browser_menu_erase_action import BrowserMenuEraseAction
from cross_field_highlighter.ui.menu.browser_menu_highlight_action import BrowserMenuHighlightAction
from cross_field_highlighter.ui.menu.browser_menu_search_highlighted_notes_action import \
    BrowserMenuSearchHighlightedNotesAction
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from cross_field_highlighter.ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenu(QMenu):

    def __init__(self, browser: Browser, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController,
                 dialog_params_factory: DialogParamsFactory) -> None:
        super().__init__("Cross-Field Highlighter", browser)

        highlight_action: BrowserMenuHighlightAction = BrowserMenuHighlightAction(
            browser, op_factory, adhoc_highlight_dialog_controller, dialog_params_factory)
        self.addAction(highlight_action)

        erase_action: BrowserMenuEraseAction = BrowserMenuEraseAction(
            browser, op_factory, adhoc_erase_dialog_controller, dialog_params_factory)
        self.addAction(erase_action)

        search_action: BrowserMenuSearchHighlightedNotesAction = BrowserMenuSearchHighlightedNotesAction(browser)
        self.addAction(search_action)

        log.debug(f"{self.__class__.__name__} was instantiated")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
