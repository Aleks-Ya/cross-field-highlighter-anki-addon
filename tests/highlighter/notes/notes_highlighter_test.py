from anki.collection import Collection
from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import Word, Notes
from tests.data import Data, DefaultFields, CaseNote


def __assert_highlighted_notes(col: Collection, case_notes: list[CaseNote]) -> None:
    for case_note in case_notes:
        act_note: Note = col.get_note(case_note.note.id)
        assert act_note[DefaultFields.basic_back_field] == case_note.highlighted_content


def __assert_original_notes(col: Collection, case_notes: list[CaseNote]) -> None:
    for case_note in case_notes:
        act_note: Note = col.get_note(case_note.note.id)
        assert act_note[DefaultFields.basic_back_field] == case_note.original_content


def test_highlight_erase(notes_highlighter: NotesHighlighter, td: Data, col: Collection, bold_format: HighlightFormat):
    case_notes: list[CaseNote] = td.create_case_notes()
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    stop_words: set[Word] = td.stop_words()

    # Highlight 1st time
    notes_highlight_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front_field, DefaultFields.basic_back_field, stop_words, bold_format)
    col.update_notes(notes_highlight_result.notes)
    __assert_highlighted_notes(col, case_notes)

    # Highlight again
    notes_highlight_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front_field, DefaultFields.basic_back_field, stop_words, bold_format)
    col.update_notes(notes_highlight_result.notes)
    __assert_highlighted_notes(col, case_notes)

    # Erase
    notes_erase_result: NotesHighlighterResult = notes_highlighter.erase(notes, DefaultFields.basic_back_field)
    col.update_notes(notes_erase_result.notes)
    __assert_original_notes(col, case_notes)
