import logging
from logging import Logger
from abc import abstractmethod
from typing import Optional, Callable

from anki.notes import NoteId

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldName, FieldNames, NoteTypeName

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
        self.destination_fields: FieldNames = FieldNames([])
        self.selected_note_type: Optional[NoteTypeDetails] = None
        self.selected_source_field: dict[NoteTypeName, FieldName] = {}
        self.selected_format: Optional[HighlightFormat] = None
        self.selected_stop_words: Optional[str] = None
        self.selected_destination_fields: FieldNames = FieldNames([])
        self.accept_callback: Optional[Callable[[], None]] = None
        self.reject_callback: Optional[Callable[[], None]] = None
        self.__listeners: set[AdhocHighlightDialogModelListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

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
            "destination_fields": self.destination_fields,
            "selected_note_type": self.selected_note_type,
            "selected_source_field": self.selected_source_field,
            "selected_format": self.selected_format,
            "selected_stop_words": self.selected_stop_words,
            "selected_destination_fields": self.selected_destination_fields,
            "default_stop_words": self.default_stop_words,
            "accept_callback_None": not self.accept_callback,
            "reject_callback_None": not self.reject_callback
        }

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
