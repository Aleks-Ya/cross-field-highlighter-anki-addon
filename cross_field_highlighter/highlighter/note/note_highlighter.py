from abc import ABC, abstractmethod

from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldName, Word, Text


class NoteHighlighterResult:
    note: Note
    source_field_name: FieldName
    destination_field_name: FieldName
    original_text: Text
    highlighted_text: Text

    def was_modified(self):
        return self.original_text != self.highlighted_text


class NoteHighlighter(ABC):
    @abstractmethod
    def highlight(self, note: Note, source_field: FieldName, destination_field: FieldName,
                  stop_words: set[Word], highlight_format: HighlightFormat) -> NoteHighlighterResult:
        pass

    @abstractmethod
    def erase(self, note: Note, destination_field: FieldName) -> Note:
        pass
