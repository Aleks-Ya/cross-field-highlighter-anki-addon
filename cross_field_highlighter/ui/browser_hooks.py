import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks, QMenu
from aqt.browser import Browser

from ..ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from ..ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
from ..ui.menu.browser_menu import BrowserMenu
from ..ui.menu.dialog_params_factory import DialogParamsFactory
from ..ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserHooks:

    def __init__(self, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController,
                 dialog_params_factory: DialogParamsFactory) -> None:
        self.__op_factory: OpFactory = op_factory
        self.__adhoc_highlight_dialog_controller: AdhocHighlightDialogController = adhoc_highlight_dialog_controller
        self.__adhoc_erase_dialog_controller: AdhocEraseDialogController = adhoc_erase_dialog_controller
        self.__dialog_params_factory: DialogParamsFactory = dialog_params_factory
        self.__hook_browser_will_show_context_menu: Callable[[Browser, QMenu], None] = self.__on_event
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.browser_will_show_context_menu.append(self.__hook_browser_will_show_context_menu)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.browser_will_show.remove(self.__hook_browser_will_show_context_menu)
        log.info(f"{self.__class__.__name__} are removed")

    def __on_event(self, browser: Browser, menu: QMenu) -> None:
        browser_menu: BrowserMenu = BrowserMenu(browser, self.__op_factory, self.__adhoc_highlight_dialog_controller,
                                                self.__adhoc_erase_dialog_controller, self.__dialog_params_factory)
        menu.addMenu(browser_menu)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
