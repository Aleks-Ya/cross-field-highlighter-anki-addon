from abc import ABC, abstractmethod

from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldName


class NoteHighlighter(ABC):
    @abstractmethod
    def highlight(self, note: Note, source_field: FieldName, destination_field: FieldName,
                  stop_words: set[str], highlight_format: HighlightFormat) -> Note:
        pass

    @abstractmethod
    def erase(self, note: Note, destination_field: FieldName) -> Note:
        pass
