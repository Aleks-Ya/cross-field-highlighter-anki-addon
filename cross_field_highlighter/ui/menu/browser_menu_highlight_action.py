import logging
from logging import Logger
from typing import Optional

from anki.notes import NoteId
from aqt import qconnect, QKeySequence
from aqt.browser import Browser

from ..operation.highlight_op import HighlightOp
from ...config.config import Config
from ...ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
from ...ui.dialog.dialog_params import DialogParams
from ...ui.menu.browser_menu_action import BrowserMenuAction
from ...ui.menu.dialog_params_factory import DialogParamsFactory
from ...ui.operation.highlight_op_params import HighlightOpParams
from ...ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenuHighlightAction(BrowserMenuAction):
    def __init__(self, browser: Browser, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 dialog_params_factory: DialogParamsFactory, config: Config) -> None:
        super().__init__("Highlight...", browser, dialog_params_factory)
        shortcut: Optional[str] = config.get_dialog_adhoc_highlight_editor_shortcut()
        if shortcut:
            log.debug(f"Set shortcut for {self.__class__.__name__}: {shortcut}")
            self.setShortcut(QKeySequence(shortcut))
        qconnect(self.triggered, lambda: self.__on_click(browser))
        self.__op_factory: OpFactory = op_factory
        self.__controller: AdhocHighlightDialogController = adhoc_highlight_dialog_controller
        self.__show_statistics: bool = False
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self, browser: Browser) -> None:
        log.debug("On highlight click")
        dialog_params: DialogParams = self._prepare_dialog_params(browser)
        self.__show_statistics = dialog_params.note_number > 1 or browser.editor is None
        self.__controller.show_dialog(dialog_params, self.__run_op)

    def __run_op(self, highlight_op_params: HighlightOpParams) -> None:
        note_ids: set[NoteId] = set(self._browser.selectedNotes())
        op: HighlightOp = self.__op_factory.create_highlight_op(note_ids, self._refresh_browser, self._browser,
                                                                highlight_op_params, self.__show_statistics)
        op.run_in_background()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
