import logging
from logging import Logger
from typing import Optional

from anki.notes import NoteId
from aqt import qconnect, QKeySequence
from aqt.browser import Browser

from ..operation.erase_op import EraseOp
from ...config.config import Config
from ...ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from ...ui.dialog.dialog_params import DialogParams
from ...ui.menu.browser_menu_action import BrowserMenuAction
from ...ui.menu.dialog_params_factory import DialogParamsFactory
from ...ui.operation.erase_op_params import EraseOpParams
from ...ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenuEraseAction(BrowserMenuAction):
    def __init__(self, browser: Browser, op_factory: OpFactory,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController,
                 dialog_params_factory: DialogParamsFactory, config: Config) -> None:
        super().__init__("Erase...", browser, dialog_params_factory)
        qconnect(self.triggered, lambda: self.__on_click(browser))
        shortcut: Optional[str] = config.get_dialog_adhoc_erase_editor_shortcut()
        if shortcut:
            log.debug(f"Set shortcut for {self.__class__.__name__}: {shortcut}")
            self.setShortcut(QKeySequence(shortcut))
        self.__op_factory: OpFactory = op_factory
        self.__controller: AdhocEraseDialogController = adhoc_erase_dialog_controller
        self.__show_statistics: bool = False
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_click(self, browser: Browser) -> None:
        log.debug("On highlight click")
        dialog_params: DialogParams = self._prepare_dialog_params(browser)
        self.__show_statistics = dialog_params.note_number > 1 or browser.editor is None
        self.__controller.show_dialog(dialog_params, self.__run_op)

    def __run_op(self, erase_op_params: EraseOpParams) -> None:
        note_ids: set[NoteId] = set(self._browser.selectedNotes())
        op: EraseOp = self.__op_factory.create_erase_op(note_ids, self._refresh_browser, self._browser,
                                                        erase_op_params, self.__show_statistics)
        op.run_in_background()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
