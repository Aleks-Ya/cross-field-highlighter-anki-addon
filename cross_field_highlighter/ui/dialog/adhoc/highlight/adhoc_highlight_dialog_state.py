import logging
from logging import Logger
from typing import Optional

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, FieldName, Text

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogState:
    def __init__(self, note_type_details: NoteTypeDetails):
        self.__selected_note_type: NoteTypeDetails = note_type_details
        self.__selected_source_field: Optional[FieldName] = None
        self.__selected_format: Optional[HighlightFormat] = None
        self.__selected_stop_words: Optional[Text] = None
        self.__selected_destination_fields: FieldNames = FieldNames([])
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_selected_note_type(self) -> NoteTypeDetails:
        return self.__selected_note_type

    def get_selected_source_filed(self) -> FieldName:
        if not self.__selected_source_field:
            self.select_first_source_field()
        return self.__selected_source_field

    def get_selected_format(self) -> HighlightFormat:
        return self.__selected_format

    def get_selected_stop_words(self) -> Text:
        return self.__selected_stop_words

    def get_selected_destination_fields(self) -> FieldNames:
        return self.__selected_destination_fields

    def select_destination_fields(self, field_names: FieldNames) -> None:
        self.__selected_destination_fields = field_names

    def set_stop_words(self, stop_words: Text) -> None:
        self.__selected_stop_words = stop_words

    def select_format(self, highlight_format: HighlightFormat) -> None:
        self.__selected_format = highlight_format

    def select_source_field(self, source_field_name: FieldName) -> None:
        if source_field_name in self.__selected_note_type.fields:
            self.__selected_source_field = source_field_name

    def select_first_source_field(self) -> None:
        if len(self.__selected_note_type.fields) < 1:
            raise Exception("Note type must have at least one field")
        self.__selected_source_field = self.__selected_note_type.fields[0]

    def as_dict(self) -> dict[str, any]:
        return {
            "selected_note_type": self.__selected_note_type,
            "selected_source_field": self.__selected_source_field,
            "selected_format": self.__selected_format,
            "selected_stop_words": self.__selected_stop_words,
            "selected_destination_fields": self.__selected_destination_fields
        }

    def __repr__(self):
        return str(self.as_dict())

    def __eq__(self, other):
        if not isinstance(other, AdhocHighlightDialogState):
            return False
        return self.as_dict() == other.as_dict()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
