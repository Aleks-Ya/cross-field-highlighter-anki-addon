from anki.collection import Collection
from anki.notes import NoteId, Note

from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.highlighter.types import FieldName


class StartWithNoteHighlighter(NoteHighlighter):
    def __init__(self, col: Collection, text_highlighter: TextHighlighter):
        self.__col: Collection = col
        self.__text_highlighter: TextHighlighter = text_highlighter

    def highlight(self, note_id: NoteId, collocation_field: FieldName, destination_field: FieldName,
                  stop_words: set[str]) -> None:
        note: Note = self.__col.get_note(note_id)
        collocation: str = note[collocation_field]
        original_text: str = note[destination_field]
        highlighted_text: str = self.__text_highlighter.highlight(collocation, original_text, stop_words)
        note[destination_field] = highlighted_text
        note.flush()

    def erase(self, note_id: NoteId, destination_field: FieldName) -> None:
        note: Note = self.__col.get_note(note_id)
        original_text: str = note[destination_field]
        erased_text: str = self.__text_highlighter.erase(original_text)
        note[destination_field] = erased_text
        note.flush()
