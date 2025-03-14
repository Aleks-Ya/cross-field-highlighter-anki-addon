import logging
from logging import Logger
from typing import Sequence, Optional

from anki.cards import CardId
from anki.notes import NoteId, Note
from aqt import QAction
from aqt.browser import Browser

from ...ui.dialog.dialog_params import DialogParams
from ...ui.menu.dialog_params_factory import DialogParamsFactory

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
            selected_card_ids: Sequence[CardId] = browser.selectedCards()
            dialog_params: DialogParams = self.__dialog_params_factory.create_from_card_ids(selected_card_ids)
        log.debug(f"Created DialogParams: {dialog_params}")
        return dialog_params

    def _refresh_browser(self) -> None:
        self.__reload_current_note()
        self.__refresh_tags()

    def __reload_current_note(self) -> None:
        log.debug("Reload current note in Editor")
        if self._browser.editor and self._browser.editor.note:
            note_id: NoteId = self._browser.editor.note.id
            note: Note = self._browser.col.get_note(note_id)
            self._browser.editor.set_note(note)

    def __refresh_tags(self) -> None:
        self._browser.sidebar.refresh()

    @staticmethod
    def __is_notes_mode(browser: Browser) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return browser._switch.isChecked()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
