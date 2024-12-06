import logging
from logging import Logger

from anki.models import NotetypeId

from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.types import FieldName, FieldNames, Text

log: Logger = logging.getLogger(__name__)


class HighlightOpParams:
    def __init__(self, note_type_id: NotetypeId,
                 source_field: FieldName, space_delimited_language: bool, destination_fields: FieldNames,
                 stop_words: Text, highlight_format: HighlightFormat):
        self.note_type_id: NotetypeId = note_type_id
        self.source_field: FieldName = source_field
        self.space_delimited_language: bool = space_delimited_language
        self.destination_fields: FieldNames = destination_fields
        self.stop_words: Text = stop_words
        self.highlight_format: HighlightFormat = highlight_format
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        fields: str = ", ".join([str(field) for field in self.destination_fields])
        return (f"HighlightOpParams(note_type_id={self.note_type_id}, "
                f"source_field={self.source_field}, space_delimited_language={self.space_delimited_language}, "
                f"destination_fields={fields}, stop_words='{self.stop_words}', highlight_format={self.highlight_format})")

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, HighlightOpParams):
            return False
        return (self.note_type_id == other.note_type_id and
                self.source_field == other.source_field and
                self.space_delimited_language == other.space_delimited_language and
                self.destination_fields == other.destination_fields and
                self.stop_words == other.stop_words and
                self.highlight_format == other.highlight_format)

    def __hash__(self):
        return hash((self.note_type_id, self.source_field, self.space_delimited_language,
                     tuple(self.destination_fields), tuple(self.stop_words), self.highlight_format))

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
