from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlightResult, NoteEraseResult
from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.types import FieldContent, Word
from tests.data import Data, DefaultFields


def test_cases(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, bold_format: HighlightFormat):
    for case in td.cases():
        print(f"Case: {case.name}")

        note: Note = td.create_basic_note_1(FieldContent(case.phrase), FieldContent(case.original_text))
        stop_words: set[Word] = td.stop_words()

        # Highlight 1st time
        result: NoteHighlightResult = start_with_note_highlighter.highlight(
            note, DefaultFields.basic_front_field, DefaultFields.basic_back_field, stop_words, bold_format)
        note_act: Note = result.note
        assert note_act[DefaultFields.basic_back_field] == case.highlighted_text

        # Highlight again
        result: NoteHighlightResult = start_with_note_highlighter.highlight(
            note, DefaultFields.basic_front_field, DefaultFields.basic_back_field, stop_words, bold_format)
        note_act: Note = result.note
        assert note_act[DefaultFields.basic_back_field] == case.highlighted_text

        # Erase
        result: NoteEraseResult = start_with_note_highlighter.erase(note, DefaultFields.basic_back_field)
        assert result.note[DefaultFields.basic_back_field] == case.original_text
