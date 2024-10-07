import logging
from logging import Logger
from typing import Callable, Sequence

from anki.cards import CardId
from anki.models import NotetypeId
from anki.notes import NoteId, Note
from aqt import gui_hooks, qconnect, QAction, QMenu
from aqt.browser import Browser

from cross_field_highlighter.highlighter.highlighter_params import BulkHighlighterParams
from cross_field_highlighter.highlighter.types import FieldName
from cross_field_highlighter.ui.dialog.adhoc.adhoc_dialog import AdhocDialog
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams

log: Logger = logging.getLogger(__name__)


class BrowserHooks:

    def __init__(self) -> None:
        self.__adhoc_dialog: AdhocDialog = AdhocDialog()
        self.__hook_browser_will_show_context_menu: Callable[[Browser, QMenu], None] = self.__on_event
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.browser_will_show_context_menu.append(self.__hook_browser_will_show_context_menu)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.browser_will_show.remove(self.__hook_browser_will_show_context_menu)
        log.info(f"{self.__class__.__name__} are removed")

    def __on_event(self, browser: Browser, menu: QMenu) -> None:
        parent_menu: QMenu = QMenu("Cross-Field Highlighter", browser)
        menu.addMenu(parent_menu)

        highlight_action: QAction = QAction("Highlight...", browser)
        qconnect(highlight_action.triggered, lambda: self.__on_highlight_click(browser))
        parent_menu.addAction(highlight_action)

        erase_action: QAction = QAction("Erase...", browser)
        qconnect(erase_action.triggered, lambda: self.__on_erase_click(browser))
        parent_menu.addAction(erase_action)

    def __on_highlight_click(self, browser: Browser):
        dialog_params: DialogParams = self.__prepare_dialog_params(browser)
        self.__adhoc_dialog.show_dialog(dialog_params)

    def __on_erase_click(self, browser: Browser):
        dialog_params: DialogParams = self.__prepare_dialog_params(browser)
        self.__adhoc_dialog.show_dialog(dialog_params)

    def __prepare_dialog_params(self, browser: Browser) -> DialogParams:
        note_ids: Sequence[NoteId] = self.__get_selected_note_ids(browser)
        notes: list[Note] = [browser.col.get_note(note_id) for note_id in note_ids]
        note_types: dict[NotetypeId, list[FieldName]] = {note.mid: note.fields for note in notes}
        return DialogParams(note_types)

    def __prepare_highlighter_params(self, note_ids: Sequence[NoteId]) -> BulkHighlighterParams:
        pass
        # for note_id in note_ids:
        # return BulkHighlighterParams()

    def __get_selected_note_ids(self, browser: Browser) -> Sequence[NoteId]:
        notes_mode: bool = self.is_notes_mode(browser)
        if notes_mode:
            return browser.selectedNotes()
        else:
            card_ids: Sequence[CardId] = browser.selectedCards()
            return [browser.col.get_card(card_id).nid for card_id in card_ids]

    @staticmethod
    def is_notes_mode(browser: Browser) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return browser._switch.isChecked()
