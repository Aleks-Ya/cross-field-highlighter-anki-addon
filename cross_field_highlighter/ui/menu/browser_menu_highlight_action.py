import logging
from logging import Logger

from aqt import qconnect
from aqt.browser import Browser

from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.menu.browser_menu_action import BrowserMenuAction
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from cross_field_highlighter.ui.operation.highlight_op import HighlightOp
from cross_field_highlighter.ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenuHighlightAction(BrowserMenuAction):

    def __init__(self, browser: Browser, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 dialog_params_factory: DialogParamsFactory) -> None:
        super().__init__("Highlight...", browser, dialog_params_factory)
        qconnect(self.triggered, lambda: self.__on_click(browser))

        self.__op_factory: OpFactory = op_factory
        self.__adhoc_highlight_dialog_controller: AdhocHighlightDialogController = adhoc_highlight_dialog_controller
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self, browser: Browser):
        log.debug("On highlight click")
        dialog_params: DialogParams = self._prepare_dialog_params(browser)
        self.__adhoc_highlight_dialog_controller.show_dialog(dialog_params, self.__run_op)

    def __run_op(self, result: HighlightOpParams):
        op: HighlightOp = self.__op_factory.create_highlight_op(result, self._reload_current_note)
        op.run_in_background()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
