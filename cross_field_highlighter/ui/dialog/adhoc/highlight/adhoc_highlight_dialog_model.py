import logging
from logging import Logger
from abc import abstractmethod
from typing import Optional, Callable

from anki.notes import NoteId

from .....highlighter.formatter.highlight_format import HighlightFormats, HighlightFormatCode, HighlightFormat
from .....highlighter.note_type_details import NoteTypeDetails
from .....highlighter.types import NoteTypeName, FieldNames, Text, FieldName
from .....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_state import AdhocHighlightDialogState

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogModelListener:
    @abstractmethod
    def model_changed(self, source: object):
        pass


class AdhocHighlightDialogModel:
    __source_field: str = "source_field"
    __space_delimited_language: str = "space_delimited_language"
    __format: str = "format"
    __stop_words: str = "stop_words"
    __destination_fields: str = "destination_fields"

    def __init__(self):
        self.__note_types: list[NoteTypeDetails] = []
        self.__note_ids: list[NoteId] = []
        self.__formats: HighlightFormats = HighlightFormats([])
        self.__default_stop_words: Optional[str] = None
        self.__accept_callback: Optional[Callable[[], None]] = None
        self.__reject_callback: Optional[Callable[[], None]] = None
        self.__current_state: Optional[AdhocHighlightDialogState] = None
        self.__states: dict[NoteTypeName, AdhocHighlightDialogState] = {}
        self.__listeners: set[AdhocHighlightDialogModelListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def fill(self, note_types: list[NoteTypeDetails], note_ids: list[NoteId], formats: HighlightFormats,
             accept_callback: Optional[Callable[[], None]], reject_callback: Optional[Callable[[], None]]) -> None:
        self.__note_types = note_types
        self.__note_ids = note_ids
        self.__formats = formats
        self.__accept_callback = accept_callback
        self.__reject_callback = reject_callback

    def reset_states(self) -> None:
        for state in self.__states.values():
            state.select_format(self.__formats[0])
            state.set_stop_words(Text(self.__default_stop_words))
            state.select_destination_fields(FieldNames([]))
            state.select_first_source_field()
        self.switch_to_first_state()

    def get_note_types(self) -> list[NoteTypeDetails]:
        return self.__note_types

    def get_formats(self) -> HighlightFormats:
        return self.__formats

    def get_current_state(self) -> AdhocHighlightDialogState:
        if not self.__current_state:
            self.switch_to_first_state()
        return self.__current_state

    def get_states(self) -> list[AdhocHighlightDialogState]:
        return list(self.__states.values())

    def get_note_ids(self) -> list[NoteId]:
        return self.__note_ids

    def set_default_stop_words(self, default_stop_words: Optional[str]) -> None:
        self.__default_stop_words = default_stop_words

    def switch_state(self, note_type_details: NoteTypeDetails):
        note_type_name: NoteTypeName = note_type_details.name
        if note_type_name not in self.__states:
            state: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details)
            state.select_first_source_field()
            if len(self.__formats) > 0:
                state.select_format(self.__formats[0])
            self.__states[note_type_name] = state
        self.__current_state = self.__states[note_type_name]
        if not self.__current_state.get_selected_stop_words():
            self.__current_state.set_stop_words(Text(self.__default_stop_words))

    def switch_to_first_state(self) -> None:
        if len(self.__note_types) < 1:
            raise Exception("At least one note type should exist")
        note_type_details: NoteTypeDetails = self.__note_types[0]
        self.switch_state(note_type_details)

    def call_accept_callback(self) -> None:
        if self.__accept_callback:
            self.__accept_callback()

    def call_reject_callback(self) -> None:
        if self.__reject_callback:
            self.__reject_callback()

    def add_listener(self, listener: AdhocHighlightDialogModelListener):
        self.__listeners.add(listener)

    def fire_model_changed(self, source: object):
        for listener in self.__listeners:
            listener.model_changed(source)

    def as_dict(self) -> dict[str, any]:
        return {
            "note_types": self.__note_types,
            "note_ids": self.__note_ids,
            "formats": self.__formats,
            "states": {k: v.as_dict() for k, v in self.__states.items()},
            "current_state": self.__current_state.as_dict() if self.__current_state else None,
            "default_stop_words": self.__default_stop_words,
            "accept_callback_None": not self.__accept_callback,
            "reject_callback_None": not self.__reject_callback
        }

    def serialize_states(self) -> dict[str, any]:
        states: list[dict[str, any]] = [{
            "note_type": state.get_selected_note_type().name,
            self.__source_field: state.get_selected_source_filed(),
            self.__space_delimited_language: state.get_space_delimited_language(),
            self.__format: state.get_selected_format().code.value,
            self.__stop_words: state.get_selected_stop_words(),
            self.__destination_fields: state.get_selected_destination_fields()
        } for state in self.get_states()]
        result: dict[str, any] = {
            "current_state": self.get_current_state().get_selected_note_type().name,
            "states": states}
        return result

    def deserialize_states(self, json: dict[str, any]) -> None:
        note_type_dict: [NoteTypeName, NoteTypeDetails] = {note_type.name: note_type for note_type in
                                                           self.get_note_types()}
        highlight_formats: [HighlightFormatCode, HighlightFormat] = {highlight_format.code: highlight_format for
                                                                     highlight_format in self.get_formats()}
        if json and "states" in json:
            for state_obj in json["states"]:
                saved_note_type_name: NoteTypeName = state_obj["note_type"]
                if saved_note_type_name in note_type_dict:
                    saved_note_type_details: NoteTypeDetails = note_type_dict[saved_note_type_name]
                    self.switch_state(saved_note_type_details)
                    if self.__source_field in state_obj:
                        saved_source_field: FieldName = FieldName(state_obj[self.__source_field])
                        self.get_current_state().select_source_field(saved_source_field)
                    if self.__space_delimited_language in state_obj:
                        space_delimited_language: bool = state_obj[self.__space_delimited_language]
                        self.get_current_state().set_space_delimited_language(space_delimited_language)
                    if self.__format in state_obj:
                        saved_highlight_format_code: HighlightFormatCode = HighlightFormatCode(state_obj[self.__format])
                        saved_highlight_format: HighlightFormat = highlight_formats[saved_highlight_format_code]
                        self.get_current_state().select_format(saved_highlight_format)
                    if self.__stop_words in state_obj:
                        saved_stop_words: Text = Text(state_obj[self.__stop_words])
                        self.get_current_state().set_stop_words(saved_stop_words)
                    if self.__destination_fields in state_obj:
                        saved_destination_fields: FieldNames = FieldNames(state_obj[self.__destination_fields])
                        self.get_current_state().select_destination_fields(saved_destination_fields)
        if json and "current_state" in json:
            current_state_name: NoteTypeName = json["current_state"]
            if current_state_name in note_type_dict:
                current_note_type_details: NoteTypeDetails = note_type_dict[current_state_name]
                self.switch_state(current_note_type_details)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.as_dict()})"

    def __eq__(self, other):
        if not isinstance(other, AdhocHighlightDialogModel):
            return False
        return self.as_dict() == other.as_dict()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
