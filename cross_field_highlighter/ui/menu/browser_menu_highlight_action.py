import logging
from logging import Logger

from anki.notes import NoteId
from aqt import qconnect
from aqt.browser import Browser

from ...ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
from ...ui.operation.highlight_op_params import HighlightOpParams
from ...ui.menu.browser_menu_action import BrowserMenuAction
from ...ui.dialog.dialog_params import DialogParams
from ...ui.menu.dialog_params_factory import DialogParamsFactory
from ...ui.operation.highlight_op import HighlightOp
from ...ui.operation.op_factory import OpFactory

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

    def __run_op(self, highlight_op_params: HighlightOpParams):
        note_ids: set[NoteId] = set(self._browser.selectedNotes())
        op: HighlightOp = self.__op_factory.create_highlight_op(note_ids, highlight_op_params,
                                                                self._reload_current_note, self._browser)
        op.run_in_background()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
