import logging
from abc import abstractmethod
from logging import Logger
from typing import Optional, Callable

from anki.models import NotetypeId

from .....highlighter.formatter.highlight_format import HighlightFormats
from .....highlighter.note_type_details import NoteTypeDetails
from .....highlighter.types import FieldNames, Text
from .....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_state import AdhocHighlightDialogState

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogModelListener:
    @abstractmethod
    def highlight_model_changed(self, source: object, model: 'AdhocHighlightDialogModel'):
        pass


class AdhocHighlightDialogModel:
    def __init__(self):
        self.__all_note_types: list[NoteTypeDetails] = []
        self.__selected_note_types: list[NoteTypeDetails] = []
        self.__note_number: int = 0
        self.__formats: HighlightFormats = HighlightFormats([])
        self.__default_stop_words: Optional[str] = None
        self.__accept_callback: Optional[Callable[[], None]] = None
        self.__reject_callback: Optional[Callable[[], None]] = None
        self.__current_state: Optional[AdhocHighlightDialogState] = None
        self.__states: dict[NotetypeId, AdhocHighlightDialogState] = {}
        self.__listeners: set[AdhocHighlightDialogModelListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def fill(self, all_note_types: list[NoteTypeDetails], selected_note_types: list[NoteTypeDetails], note_number: int,
             formats: HighlightFormats, accept_callback: Optional[Callable[[], None]],
             reject_callback: Optional[Callable[[], None]]) -> None:
        log.debug(f"Model before filling: {self.as_dict()}")
        self.__all_note_types = all_note_types
        self.__selected_note_types = selected_note_types
        self.__note_number = note_number
        self.__formats = formats
        self.__accept_callback = accept_callback
        self.__reject_callback = reject_callback
        log.debug(f"Model after filling: {self.as_dict()}")

    def reset_states(self) -> None:
        for state in self.__states.values():
            state.select_format(self.__formats[0])
            state.set_stop_words(Text(self.__default_stop_words))
            state.select_destination_fields(FieldNames([]))
            state.select_first_source_field()
        self.switch_to_first_state()

    def get_all_note_types(self) -> list[NoteTypeDetails]:
        return self.__all_note_types

    def get_selected_note_types(self) -> list[NoteTypeDetails]:
        return self.__selected_note_types

    def get_note_number(self) -> int:
        return self.__note_number

    def get_formats(self) -> HighlightFormats:
        return self.__formats

    def get_current_state(self) -> AdhocHighlightDialogState:
        if not self.__current_state or self.__current_state.get_selected_note_type() not in self.__selected_note_types:
            self.switch_to_first_state()
        return self.__current_state

    def get_states(self) -> list[AdhocHighlightDialogState]:
        return list(self.__states.values())

    def set_default_stop_words(self, default_stop_words: Optional[str]) -> None:
        self.__default_stop_words = default_stop_words

    def switch_state(self, note_type_details: NoteTypeDetails) -> None:
        note_type_id: NotetypeId = note_type_details.note_type_id
        if note_type_id not in self.__states:
            state: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details)
            state.select_first_source_field()
            if len(self.__formats) > 0:
                state.select_format(self.__formats[0])
            self.__states[note_type_id] = state
        self.__current_state = self.__states[note_type_id]
        if not self.__current_state.get_selected_stop_words():
            self.__current_state.set_stop_words(Text(self.__default_stop_words))

    def switch_to_first_state(self) -> None:
        if len(self.__selected_note_types) < 1:
            raise ValueError("At least one note type should exist")
        note_type_details: NoteTypeDetails = self.__selected_note_types[0]
        log.debug(f"Switch to first state: {note_type_details}")
        self.switch_state(note_type_details)

    def call_accept_callback(self) -> None:
        if self.__accept_callback:
            self.__accept_callback()

    def call_reject_callback(self) -> None:
        if self.__reject_callback:
            self.__reject_callback()

    def add_listener(self, listener: AdhocHighlightDialogModelListener) -> None:
        self.__listeners.add(listener)

    def fire_model_changed(self, source: object) -> None:
        for listener in self.__listeners:
            listener.highlight_model_changed(source, self)

    def as_dict(self) -> dict[str, any]:
        return {
            "all_note_types": self.__all_note_types,
            "selected_note_types": self.__selected_note_types,
            "note_number": self.__note_number,
            "formats": self.__formats,
            "states": {k: v.as_dict() for k, v in self.__states.items()},
            "current_state": self.__current_state.as_dict() if self.__current_state else None,
            "default_stop_words": self.__default_stop_words,
            "accept_callback_None": not self.__accept_callback,
            "reject_callback_None": not self.__reject_callback
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.as_dict()})"

    def __eq__(self, other):
        if not isinstance(other, AdhocHighlightDialogModel):
            return False
        return self.as_dict() == other.as_dict()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
