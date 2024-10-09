from anki.notes import NoteId

from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter
from cross_field_highlighter.highlighter.types import FieldName


class NotesHighlighter:
    def __init__(self, note_highlighter: NoteHighlighter):
        self.__note_highlighter: NoteHighlighter = note_highlighter

    def highlight(self, note_ids: set[NoteId], collocation_field: FieldName, destination_field: FieldName,
                  stop_words: set[str]) -> None:
        for note_id in note_ids:
            self.__note_highlighter.highlight(note_id, collocation_field, destination_field, stop_words)

    def erase(self, note_ids: set[NoteId], destination_field: FieldName) -> None:
        for note_id in note_ids:
            self.__note_highlighter.erase(note_id, destination_field)
