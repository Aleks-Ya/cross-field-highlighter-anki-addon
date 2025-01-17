import logging
from logging import Logger
from typing import Callable

from aqt.browser import Browser

from ...config.config import Config
from ...ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from ...ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
from ...ui.menu.browser_menu_erase_action import BrowserMenuEraseAction
from ...ui.menu.browser_menu_highlight_action import BrowserMenuHighlightAction
from ...ui.menu.dialog_params_factory import DialogParamsFactory
from ...ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserWillShowHook(Callable[[Browser], None]):

    def __init__(self, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController, dialog_params_factory: DialogParamsFactory,
                 config: Config) -> None:
        self.__op_factory: OpFactory = op_factory
        self.__adhoc_highlight_dialog_controller: AdhocHighlightDialogController = adhoc_highlight_dialog_controller
        self.__adhoc_erase_dialog_controller: AdhocEraseDialogController = adhoc_erase_dialog_controller
        self.__dialog_params_factory: DialogParamsFactory = dialog_params_factory
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __call__(self, browser: Browser) -> None:
        log.debug("On Browser will show")
        highlight_action: BrowserMenuHighlightAction = BrowserMenuHighlightAction(
            browser, self.__op_factory, self.__adhoc_highlight_dialog_controller, self.__dialog_params_factory,
            self.__config)
        erase_action: BrowserMenuEraseAction = BrowserMenuEraseAction(
            browser, self.__op_factory, self.__adhoc_erase_dialog_controller, self.__dialog_params_factory,
            self.__config)
        browser.form.tableView.addAction(highlight_action)
        browser.form.tableView.addAction(erase_action)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
