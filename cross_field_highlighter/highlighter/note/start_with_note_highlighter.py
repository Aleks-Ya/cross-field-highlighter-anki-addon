from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.highlighter.types import FieldName, Text, Word


class StartWithNoteHighlighter(NoteHighlighter):
    def __init__(self, text_highlighter: TextHighlighter):
        self.__text_highlighter: TextHighlighter = text_highlighter

    def highlight(self, note: Note, collocation_field: FieldName, destination_field: FieldName,
                  stop_words: set[Word], highlight_format: HighlightFormat) -> Note:
        collocation: str = note[collocation_field]
        original_text: str = note[destination_field]
        highlighted_text: str = self.__text_highlighter.highlight(
            collocation, original_text, stop_words, highlight_format)
        note[destination_field] = highlighted_text
        return note

    def erase(self, note: Note, destination_field: FieldName) -> Note:
        original_text: Text = Text(note[destination_field])
        erased_text: Text = self.__text_highlighter.erase(original_text)
        note[destination_field] = erased_text
        return note
