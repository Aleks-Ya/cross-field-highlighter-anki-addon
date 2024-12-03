from anki.notes import Note

from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.note.note_field_highlighter import NoteFieldHighlighter, NoteFieldHighlightResult, \
    NoteFieldEraseResult
from ...highlighter.text.text_highlighter import TextHighlighter
from ...highlighter.types import FieldName, Text


class StartWithNoteFieldHighlighter(NoteFieldHighlighter):
    def __init__(self, text_highlighter: TextHighlighter):
        self.__text_highlighter: TextHighlighter = text_highlighter

    def highlight(self, note: Note, source_field: FieldName, destination_field: FieldName,
                  stop_words: Text, space_delimited_language: bool,
                  highlight_format: HighlightFormat) -> NoteFieldHighlightResult:
        super().highlight(note, source_field, destination_field, stop_words, space_delimited_language, highlight_format)
        phrase: Text = Text(note[source_field])
        original_text: Text = Text(note[destination_field])
        highlighted_text: Text = self.__text_highlighter.highlight(phrase, original_text, stop_words,
                                                                   space_delimited_language, highlight_format)
        note[destination_field] = highlighted_text
        return NoteFieldHighlightResult(note, source_field, destination_field, original_text, highlighted_text)

    def erase(self, note: Note, field: FieldName) -> NoteFieldEraseResult:
        super().erase(note, field)
        original_text: Text = Text(note[field])
        erased_text: Text = self.__text_highlighter.erase(original_text)
        note[field] = erased_text
        return NoteFieldEraseResult(note, field, original_text, erased_text)
