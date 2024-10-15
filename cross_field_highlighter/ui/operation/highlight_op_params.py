from anki.models import NotetypeId
from anki.notes import NoteId
from aqt import QWidget

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import Word, FieldName, FieldNames


class HighlightOpParams:
    def __init__(self, note_type_id: NotetypeId, note_ids: set[NoteId], parent: QWidget, source_filed: FieldName,
                 destination_fields: FieldNames, stop_words: set[Word], highlight_format: HighlightFormat):
        self.note_type_id: NotetypeId = note_type_id
        self.note_ids: set[NoteId] = note_ids
        self.parent: QWidget = parent
        self.source_field: FieldName = source_filed
        self.destination_fields: FieldNames = destination_fields
        self.stop_words: set[Word] = stop_words
        self.highlight_format: HighlightFormat = highlight_format
