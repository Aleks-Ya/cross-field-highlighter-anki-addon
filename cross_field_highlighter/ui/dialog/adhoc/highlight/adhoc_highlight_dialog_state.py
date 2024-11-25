import logging
from logging import Logger
from typing import Optional

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, FieldName, Text

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogState:
    def __init__(self, note_type_details: NoteTypeDetails):
        self.selected_note_type: NoteTypeDetails = note_type_details
        self.selected_source_field: Optional[FieldName] = None
        self.selected_format: Optional[HighlightFormat] = None
        self.selected_stop_words: Optional[Text] = None
        self.selected_destination_fields: FieldNames = FieldNames([])
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_selected_note_type(self) -> NoteTypeDetails:
        return self.selected_note_type

    def as_dict(self) -> dict[str, any]:
        return {
            "selected_note_type": self.selected_note_type,
            "selected_source_field": self.selected_source_field,
            "selected_format": self.selected_format,
            "selected_stop_words": self.selected_stop_words,
            "selected_destination_fields": self.selected_destination_fields
        }

    def __repr__(self):
        return str(self.as_dict())

    def __eq__(self, other):
        if not isinstance(other, AdhocHighlightDialogState):
            return False
        return self.as_dict() == other.as_dict()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
