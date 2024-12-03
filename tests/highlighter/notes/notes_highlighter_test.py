from anki.collection import Collection

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import Notes, Text, FieldNames
from tests.data import Data, DefaultFields, CaseNote


def test_highlight_erase(notes_highlighter: NotesHighlighter, td: Data, col: Collection, bold_format: HighlightFormat):
    case_notes: list[CaseNote] = td.create_case_notes()
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    stop_words: Text = td.stop_words()
    field_names: FieldNames = FieldNames([DefaultFields.basic_back])

    # Highlight 1st time
    notes_highlight_result_1: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front, field_names, stop_words, bold_format)
    col.update_notes(notes_highlight_result_1.notes)
    td.assert_highlighted_case_notes(case_notes)

    # Highlight again
    notes_highlight_result_2: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front, field_names, stop_words, bold_format)
    col.update_notes(notes_highlight_result_2.notes)
    td.assert_highlighted_case_notes(case_notes)

    # Erase
    notes_erase_result: NotesHighlighterResult = notes_highlighter.erase(notes, field_names)
    col.update_notes(notes_erase_result.notes)
    td.assert_original_case_notes(case_notes)
