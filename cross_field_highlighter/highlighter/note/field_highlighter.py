from abc import ABC, abstractmethod

from anki.notes import Note

from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.types import FieldName, Text


class FieldHighlightResult:
    def __init__(self, note: Note, source_field: FieldName, destination_field: FieldName, original_text: Text,
                 highlighted_text: Text):
        self.note: Note = note
        self.source_field: FieldName = source_field
        self.destination_field: FieldName = destination_field
        self.original_text: Text = original_text
        self.highlighted_text: Text = highlighted_text

    def was_modified(self):
        return self.original_text != self.highlighted_text


class NoteFieldEraseResult:
    def __init__(self, note: Note, field: FieldName, original_text: Text, highlighted_text: Text):
        self.note: Note = note
        self.field: FieldName = field
        self.original_text: Text = original_text
        self.erased_text: Text = highlighted_text

    def was_modified(self):
        return self.original_text != self.erased_text


class FieldHighlighter(ABC):
    @abstractmethod
    def highlight(self, note: Note, source_field: FieldName, destination_field: FieldName,
                  stop_words: Text, highlight_format: HighlightFormat) -> FieldHighlightResult:
        ...

    @abstractmethod
    def erase(self, note: Note, field: FieldName) -> NoteFieldEraseResult:
        ...
