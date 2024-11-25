import logging
from logging import Logger
from abc import abstractmethod
from typing import Optional, Callable

from anki.notes import NoteId

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_state import AdhocHighlightDialogState

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogModelListener:
    @abstractmethod
    def model_changed(self, source: object):
        pass


class AdhocHighlightDialogModel:
    def __init__(self):
        self.note_types: list[NoteTypeDetails] = []
        self.note_ids: set[NoteId] = set()
        self.formats: HighlightFormats = HighlightFormats([])
        self.default_stop_words: Optional[str] = None
        self.accept_callback: Optional[Callable[[], None]] = None
        self.reject_callback: Optional[Callable[[], None]] = None
        self.current_state: Optional[AdhocHighlightDialogState] = None
        self.__states: dict[NoteTypeName, AdhocHighlightDialogState] = {}
        self.__listeners: set[AdhocHighlightDialogModelListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def switch_state(self, note_type_details: NoteTypeDetails):
        note_type_name: NoteTypeName = note_type_details.name
        if note_type_name not in self.__states:
            self.__states[note_type_name] = AdhocHighlightDialogState(note_type_details)
        self.current_state = self.__states[note_type_name]
        if not self.current_state.selected_stop_words:
            self.current_state.selected_stop_words = self.default_stop_words

    def switch_to_first_state(self) -> None:
        if len(self.note_types) > 0:
            note_type_details: NoteTypeDetails = self.note_types[0]
            self.switch_state(note_type_details)

    def add_listener(self, listener: AdhocHighlightDialogModelListener):
        self.__listeners.add(listener)

    def fire_model_changed(self, source: object):
        for listener in self.__listeners:
            listener.model_changed(source)

    def as_dict(self) -> dict[str, any]:
        return {
            "note_types": self.note_types,
            "note_ids": self.note_ids,
            "formats": self.formats,
            "states": {k: v.as_dict() for k, v in self.__states.items()},
            "current_state": self.current_state.as_dict() if self.current_state else None,
            "default_stop_words": self.default_stop_words,
            "accept_callback_None": not self.accept_callback,
            "reject_callback_None": not self.reject_callback
        }

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
