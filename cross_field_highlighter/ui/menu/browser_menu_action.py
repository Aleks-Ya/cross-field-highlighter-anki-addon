import logging
from logging import Logger
from typing import Sequence, Optional

from anki.cards import CardId
from anki.collection import Collection
from anki.models import NotetypeId, NoteType
from anki.notes import NoteId, Note
from aqt import QAction
from aqt.browser import Browser

from cross_field_highlighter.highlighter.types import NoteTypeDetails
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams

log: Logger = logging.getLogger(__name__)


class BrowserMenuAction(QAction):

    def __init__(self, title: str, browser: Browser) -> None:
        super().__init__(title, browser)
        self._browser: Optional[Browser] = browser
        log.debug(f"{self.__class__.__name__} was instantiated")

    def _prepare_dialog_params(self, browser: Browser) -> DialogParams:
        col: Collection = browser.col
        note_ids: Sequence[NoteId] = self.__get_selected_note_ids(browser)
        note_type_ids: set[NotetypeId] = {col.get_note(note_id).mid for note_id in note_ids}
        note_types: list[NoteTypeDetails] = []
        for note_type_id in note_type_ids:
            note_type: NoteType = col.models.get(note_type_id)
            note_types.append(NoteTypeDetails(note_type_id, note_type["name"], col.models.field_names(note_type)))
        params: DialogParams = DialogParams(note_types)
        log.debug(f"Created DialogParams: {params}")
        return params

    def _reload_current_note(self):
        log.debug("Reload current note in Editor")
        note_id: NoteId = self._browser.editor.note.id
        note: Note = self._browser.col.get_note(note_id)
        self._browser.editor.set_note(note)

    def __get_selected_note_ids(self, browser: Browser) -> Sequence[NoteId]:
        notes_mode: bool = self.__is_notes_mode(browser)
        if notes_mode:
            selected_note_ids: Sequence[NoteId] = browser.selectedNotes()
        else:
            card_ids: Sequence[CardId] = browser.selectedCards()
            selected_note_ids: Sequence[NoteId] = [browser.col.get_card(card_id).nid for card_id in card_ids]
        log.debug(f"Selected note ids count: {len(selected_note_ids)}")
        return selected_note_ids

    @staticmethod
    def __is_notes_mode(browser: Browser) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return browser._switch.isChecked()
