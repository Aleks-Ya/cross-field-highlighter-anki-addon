from anki.collection import Collection

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import Notes, Text, FieldNames
from tests.data import Data, DefaultFields, CaseNote


def test_highlight_erase_space_delimited(notes_highlighter: NotesHighlighter, td: Data, col: Collection,
                                         bold_format: HighlightFormat):
    space_delimited_language: bool = True
    __highlight_erase(bold_format, col, notes_highlighter, space_delimited_language, td)


def test_highlight_erase_non_space_delimited(notes_highlighter: NotesHighlighter, td: Data, col: Collection,
                                             bold_format: HighlightFormat):
    space_delimited_language: bool = False
    __highlight_erase(bold_format, col, notes_highlighter, space_delimited_language, td)


def __highlight_erase(bold_format: HighlightFormat, col: Collection, notes_highlighter: NotesHighlighter,
                      space_delimited_language: bool, td: Data) -> None:
    case_notes: list[CaseNote] = td.create_case_notes()
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    stop_words: Text = td.stop_words()
    field_names: FieldNames = FieldNames([DefaultFields.basic_back])
    # Highlight 1st time
    notes_highlight_result_1: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front, field_names, stop_words, space_delimited_language, bold_format)
    col.update_notes(notes_highlight_result_1.notes)
    td.assert_highlighted_case_notes(case_notes, space_delimited_language)
    # Highlight again
    notes_highlight_result_2: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front, field_names, stop_words, space_delimited_language, bold_format)
    col.update_notes(notes_highlight_result_2.notes)
    td.assert_highlighted_case_notes(case_notes, space_delimited_language)
    # Erase
    notes_erase_result: NotesHighlighterResult = notes_highlighter.erase(notes, field_names)
    col.update_notes(notes_erase_result.notes)
    td.assert_original_case_notes(case_notes)
