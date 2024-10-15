import logging
from logging import Logger
from typing import Sequence, Optional

from anki.cards import CardId
from anki.notes import NoteId, Note
from aqt import QAction
from aqt.browser import Browser

from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory

log: Logger = logging.getLogger(__name__)


class BrowserMenuAction(QAction):

    def __init__(self, title: str, browser: Browser, dialog_params_factory: DialogParamsFactory) -> None:
        super().__init__(title, browser)
        self._browser: Optional[Browser] = browser
        self.__dialog_params_factory: DialogParamsFactory = dialog_params_factory
        log.debug(f"{self.__class__.__name__} was instantiated")

    def _prepare_dialog_params(self, browser: Browser) -> DialogParams:
        notes_mode: bool = self.__is_notes_mode(browser)
        if notes_mode:
            selected_note_ids: Sequence[NoteId] = browser.selectedNotes()
            dialog_params: DialogParams = self.__dialog_params_factory.create_from_note_ids(selected_note_ids)
        else:
            card_ids: Sequence[CardId] = browser.selectedCards()
            dialog_params: DialogParams = self.__dialog_params_factory.create_from_card_ids(card_ids)
        log.debug(f"Created DialogParams: {dialog_params}")
        return dialog_params

    def _reload_current_note(self):
        log.debug("Reload current note in Editor")
        if self._browser.editor and self._browser.editor.note:
            note_id: NoteId = self._browser.editor.note.id
            note: Note = self._browser.col.get_note(note_id)
            self._browser.editor.set_note(note)

    @staticmethod
    def __is_notes_mode(browser: Browser) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return browser._switch.isChecked()
