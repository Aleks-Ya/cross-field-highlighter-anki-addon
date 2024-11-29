import logging
from logging import Logger
from typing import Optional

from anki.models import NotetypeId
from anki.notes import NoteId
from aqt import QWidget

from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.types import FieldName, FieldNames, Text

log: Logger = logging.getLogger(__name__)


class HighlightOpParams:
    def __init__(self, note_type_id: NotetypeId, note_ids: list[NoteId], parent: Optional[QWidget],
                 source_field: FieldName, destination_fields: FieldNames, stop_words: Text,
                 highlight_format: HighlightFormat):
        self.note_type_id: NotetypeId = note_type_id
        self.note_ids: list[NoteId] = note_ids
        self.parent: Optional[QWidget] = parent
        self.source_field: FieldName = source_field
        self.destination_fields: FieldNames = destination_fields
        self.stop_words: Text = stop_words
        self.highlight_format: HighlightFormat = highlight_format
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        fields: str = ", ".join([str(field) for field in self.destination_fields])
        return (f"HighlightOpParams(note_type_id={self.note_type_id}, note_ids={sorted(self.note_ids)}, "
                f"source_field={self.source_field}, destination_fields={fields}, stop_words='{self.stop_words}', "
                f"highlight_format={self.highlight_format})")

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, HighlightOpParams):
            return False
        return (self.note_type_id == other.note_type_id and
                self.note_ids == other.note_ids and
                self.parent == other.parent and
                self.source_field == other.source_field and
                self.destination_fields == other.destination_fields and
                self.stop_words == other.stop_words and
                self.highlight_format == other.highlight_format)

    def __hash__(self):
        return hash((self.note_type_id, tuple(self.note_ids), self.source_field,
                     tuple(self.destination_fields), tuple(self.stop_words), self.highlight_format))

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
