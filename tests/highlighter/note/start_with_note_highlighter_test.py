from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlightResult, NoteEraseResult
from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.types import FieldContent, Word
from tests.data import Data, DefaultFields


def test_cases(start_with_note_highlighter: StartWithNoteHighlighter, td: Data):
    for case in td.cases():
        print(f"Case: {case.name}")

        note: Note = td.create_note_with_fields(FieldContent(case.phrase), FieldContent(case.original_text))
        stop_words: set[Word] = td.stop_words()

        # Highlight 1st time
        result: NoteHighlightResult = start_with_note_highlighter.highlight(
            note, DefaultFields.word_field_name, DefaultFields.text_field_name, stop_words, HighlightFormat.BOLD)
        note_act: Note = result.note
        assert note_act[DefaultFields.text_field_name] == case.highlighted_text

        # Highlight again
        result: NoteHighlightResult = start_with_note_highlighter.highlight(
            note, DefaultFields.word_field_name, DefaultFields.text_field_name, stop_words, HighlightFormat.BOLD)
        note_act: Note = result.note
        assert note_act[DefaultFields.text_field_name] == case.highlighted_text

        # Erase
        result: NoteEraseResult = start_with_note_highlighter.erase(note, DefaultFields.text_field_name)
        assert result.note[DefaultFields.text_field_name] == case.original_text
