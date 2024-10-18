from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter, NoteHighlightResult, \
    NoteEraseResult
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.highlighter.types import FieldName, Text, Word


class StartWithNoteHighlighter(NoteHighlighter):
    def __init__(self, text_highlighter: TextHighlighter):
        self.__text_highlighter: TextHighlighter = text_highlighter

    def highlight(self, note: Note, source_field: FieldName, destination_field: FieldName,
                  stop_words: set[Word], highlight_format: HighlightFormat) -> NoteHighlightResult:
        super().highlight(note, source_field, destination_field, stop_words, highlight_format)
        phrase: Text = Text(note[source_field])
        original_text: Text = Text(note[destination_field])
        highlighted_text: Text = self.__text_highlighter.highlight(phrase, original_text, stop_words, highlight_format)
        note[destination_field] = highlighted_text
        return NoteHighlightResult(note, source_field, destination_field, original_text, highlighted_text)

    def erase(self, note: Note, field: FieldName) -> NoteEraseResult:
        super().erase(note, field)
        original_text: Text = Text(note[field])
        erased_text: Text = self.__text_highlighter.erase(original_text)
        note[field] = erased_text
        return NoteEraseResult(note, field, original_text, erased_text)
