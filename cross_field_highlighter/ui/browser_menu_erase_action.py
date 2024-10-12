import logging
from logging import Logger

from anki.notes import NoteId
from aqt import qconnect, QWidget
from aqt.browser import Browser

from cross_field_highlighter.highlighter.types import FieldName
from cross_field_highlighter.ui.browser_menu_action import BrowserMenuAction
from cross_field_highlighter.ui.dialog.adhoc.adhoc_erase_dialog import AdhocEraseDialog
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.erase_op import EraseOp
from cross_field_highlighter.ui.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenuEraseAction(BrowserMenuAction):

    def __init__(self, browser: Browser, op_factory: OpFactory) -> None:
        super().__init__("Erase...", browser)
        qconnect(self.triggered, lambda: self.__on_erase_click(browser))

        self.__op_factory: OpFactory = op_factory
        self.__adhoc_erase_dialog: AdhocEraseDialog = AdhocEraseDialog()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_erase_click(self, browser: Browser):
        log.debug("On highlight click")
        self.__browser: Browser = browser
        dialog_params: DialogParams = self._prepare_dialog_params(browser)
        self.__adhoc_erase_dialog.show_dialog(dialog_params, self.__run_erase_op)

    def __run_erase_op(self, parent: QWidget, destination_filed: FieldName):
        note_ids: set[NoteId] = set(self.__browser.selectedNotes())
        op: EraseOp = self.__op_factory.create_erase_op(parent, note_ids, destination_filed)
        op.run_in_background()
