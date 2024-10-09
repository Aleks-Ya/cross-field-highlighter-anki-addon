from anki.notes import Note

from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter
from cross_field_highlighter.highlighter.types import FieldName


class NotesHighlighter:
    def __init__(self, note_highlighter: NoteHighlighter):
        self.__note_highlighter: NoteHighlighter = note_highlighter

    def highlight(self, notes: list[Note], collocation_field: FieldName, destination_field: FieldName,
                  stop_words: set[str]) -> list[Note]:
        for note in notes:
            yield self.__note_highlighter.highlight(note, collocation_field, destination_field, stop_words)

    def erase(self, notes: list[Note], destination_field: FieldName) -> list[Note]:
        for note in notes:
            yield self.__note_highlighter.erase(note, destination_field)
