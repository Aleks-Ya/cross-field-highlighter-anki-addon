from anki.collection import Collection

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import Notes, Text, FieldNames
from tests.data import Data, DefaultFields, CaseNote


def test_highlight_erase_cases(notes_highlighter: NotesHighlighter, td: Data, col: Collection,
                               bold_format: HighlightFormat):
    case_notes: list[CaseNote] = td.create_case_notes()
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    stop_words: Text = td.stop_words()
    field_names: FieldNames = FieldNames([DefaultFields.basic_back])
    exp_total_notes: int = len(case_notes)
    exp_modified_notes: int = 45
    exp_total_fields: int = 48
    exp_modified_fields: int = 45

    # Highlight 1st time
    notes_highlight_result_1: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front, field_names, stop_words, bold_format)
    col.update_notes(notes_highlight_result_1.notes)
    td.assert_highlighted_case_notes(case_notes)
    assert notes_highlight_result_1.total_notes == exp_total_notes
    assert notes_highlight_result_1.modified_notes == exp_modified_notes
    assert notes_highlight_result_1.total_fields == exp_total_fields
    assert notes_highlight_result_1.modified_fields == exp_modified_fields

    # Highlight again
    notes_highlight_result_2: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front, field_names, stop_words, bold_format)
    col.update_notes(notes_highlight_result_2.notes)
    td.assert_highlighted_case_notes(case_notes)
    assert notes_highlight_result_2.total_notes == exp_total_notes
    assert notes_highlight_result_2.modified_notes == 0
    assert notes_highlight_result_2.total_fields == exp_total_fields
    assert notes_highlight_result_2.modified_fields == 0

    # Erase 1st time
    notes_erase_result_1: NotesHighlighterResult = notes_highlighter.erase(notes, field_names)
    col.update_notes(notes_erase_result_1.notes)
    td.assert_original_case_notes(case_notes)
    assert notes_erase_result_1.total_notes == exp_total_notes
    assert notes_erase_result_1.modified_notes == exp_modified_notes
    assert notes_erase_result_1.total_fields == exp_total_fields
    assert notes_erase_result_1.modified_fields == exp_modified_fields

    # Erase again
    notes_erase_result_2: NotesHighlighterResult = notes_highlighter.erase(notes, field_names)
    col.update_notes(notes_erase_result_2.notes)
    td.assert_original_case_notes(case_notes)
    assert notes_erase_result_2.total_notes == exp_total_notes
    assert notes_erase_result_2.modified_notes == 0
    assert notes_erase_result_2.total_fields == exp_total_fields
    assert notes_erase_result_2.modified_fields == 0
