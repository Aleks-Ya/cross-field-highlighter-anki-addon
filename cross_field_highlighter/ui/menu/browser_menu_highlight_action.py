import logging
from logging import Logger

from anki.notes import NoteId
from aqt import qconnect, QWidget
from aqt.browser import Browser

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldName, Word, FieldNames
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.menu.browser_menu_action import BrowserMenuAction
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.highlight_op import HighlightOp
from cross_field_highlighter.ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenuHighlightAction(BrowserMenuAction):

    def __init__(self, browser: Browser, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController) -> None:
        super().__init__("Highlight...", browser)
        qconnect(self.triggered, lambda: self.__on_click(browser))

        self.__op_factory: OpFactory = op_factory
        self.__adhoc_highlight_dialog_controller: AdhocHighlightDialogController = adhoc_highlight_dialog_controller
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self, browser: Browser):
        log.debug("On highlight click")
        dialog_params: DialogParams = self._prepare_dialog_params(browser)
        self.__adhoc_highlight_dialog_controller.show_dialog(dialog_params, self.__run_op)

    def __run_op(self, parent: QWidget, source_filed: FieldName, destination_fileds: FieldNames,
                 stop_words: set[Word], highlight_format: HighlightFormat):
        note_ids: set[NoteId] = set(self._browser.selectedNotes())
        op: HighlightOp = self.__op_factory.create_highlight_op(
            parent, note_ids, source_filed, destination_fileds, stop_words, highlight_format, self._reload_current_note)
        op.run_in_background()