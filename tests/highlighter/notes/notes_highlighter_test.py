from anki.collection import Collection

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import Word, Notes
from tests.data import Data, DefaultFields, CaseNote


def test_highlight_erase(notes_highlighter: NotesHighlighter, td: Data, col: Collection, bold_format: HighlightFormat):
    case_notes: list[CaseNote] = td.create_case_notes()
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    stop_words: set[Word] = td.stop_words()

    # Highlight 1st time
    notes_highlight_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front_field, DefaultFields.basic_back_field, stop_words, bold_format)
    col.update_notes(notes_highlight_result.notes)
    td.assert_highlighted_case_notes(case_notes)

    # Highlight again
    notes_highlight_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front_field, DefaultFields.basic_back_field, stop_words, bold_format)
    col.update_notes(notes_highlight_result.notes)
    td.assert_highlighted_case_notes(case_notes)

    # Erase
    notes_erase_result: NotesHighlighterResult = notes_highlighter.erase(notes, DefaultFields.basic_back_field)
    col.update_notes(notes_erase_result.notes)
    td.assert_original_case_notes(case_notes)
