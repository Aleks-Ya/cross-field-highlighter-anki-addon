from abc import ABC, abstractmethod

from anki.notes import NoteId

from cross_field_highlighter.highlighter.types import FieldName


class NoteHighlighter(ABC):
    @abstractmethod
    def highlight(self, note_id: NoteId, source_field: FieldName, destination_field: FieldName,
                  stop_words: set[str]) -> None:
        pass

    @abstractmethod
    def erase(self, note_id: NoteId, destination_field: FieldName) -> None:
        pass
