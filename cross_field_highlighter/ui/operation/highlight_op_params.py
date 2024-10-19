from typing import Optional

from anki.models import NotetypeId
from anki.notes import NoteId
from aqt import QWidget

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import Word, FieldName, FieldNames


class HighlightOpParams:
    def __init__(self, note_type_id: NotetypeId, note_ids: set[NoteId], parent: Optional[QWidget],
                 source_field: FieldName,
                 destination_fields: FieldNames, stop_words: set[Word], highlight_format: HighlightFormat):
        self.note_type_id: NotetypeId = note_type_id
        self.note_ids: set[NoteId] = note_ids
        self.parent: Optional[QWidget] = parent
        self.source_field: FieldName = source_field
        self.destination_fields: FieldNames = destination_fields
        self.stop_words: set[Word] = stop_words
        self.highlight_format: HighlightFormat = highlight_format

    def __str__(self):
        fields: str = ", ".join([str(field) for field in self.destination_fields])
        return (f"HighlightOpParams(note_type_id={self.note_type_id}, note_ids={sorted(self.note_ids)}, "
                f"source_field={self.source_field}, destination_fields={fields}, stop_words={sorted(self.stop_words)}, "
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
