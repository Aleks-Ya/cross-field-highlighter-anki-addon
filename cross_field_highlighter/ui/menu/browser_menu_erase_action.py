import logging
from logging import Logger

from anki.notes import NoteId
from aqt import qconnect, QWidget
from aqt.browser import Browser

from cross_field_highlighter.highlighter.types import FieldName
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.menu.browser_menu_action import BrowserMenuAction
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.erase_op import EraseOp
from cross_field_highlighter.ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenuEraseAction(BrowserMenuAction):

    def __init__(self, browser: Browser, op_factory: OpFactory,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController) -> None:
        super().__init__("Erase...", browser)
        qconnect(self.triggered, lambda: self.__on_click(browser))

        self.__op_factory: OpFactory = op_factory
        self.__adhoc_erase_dialog_controller: AdhocEraseDialogController = adhoc_erase_dialog_controller
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self, browser: Browser):
        log.debug("On highlight click")
        dialog_params: DialogParams = self._prepare_dialog_params(browser)
        self.__adhoc_erase_dialog_controller.show_dialog(dialog_params, self.__run_op)

    def __run_op(self, parent: QWidget, destination_filed: list[FieldName]):
        note_ids: set[NoteId] = set(self._browser.selectedNotes())
        op: EraseOp = self.__op_factory.create_erase_op(parent, note_ids, destination_filed, self._reload_current_note)
        op.run_in_background()
