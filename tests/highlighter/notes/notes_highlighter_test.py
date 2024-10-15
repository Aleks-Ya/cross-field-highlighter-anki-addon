from anki.collection import Collection
from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import FieldContent, Word, Notes
from tests.data import Data, DefaultFields


def __assert_highlighted_notes(col: Collection, contents: list[(Note, FieldContent, FieldContent)]) -> None:
    for content_tuple in contents:
        exp_note: Note = content_tuple[0]
        act_note: Note = col.get_note(exp_note.id)
        highlighted_content: FieldContent = content_tuple[2]
        assert act_note[DefaultFields.basic_back_field] == highlighted_content


def __assert_original_notes(col: Collection, contents: list[(Note, FieldContent, FieldContent)]) -> None:
    for content_tuple in contents:
        exp_note: Note = content_tuple[0]
        act_note: Note = col.get_note(exp_note.id)
        original_content: FieldContent = content_tuple[1]
        assert act_note[DefaultFields.basic_back_field] == original_content


def test_highlight_erase(notes_highlighter: NotesHighlighter, td: Data, col: Collection, bold_format: HighlightFormat):
    notes_list: list[(Note, FieldContent, FieldContent)] = td.create_case_notes()
    notes: Notes = Notes([note_tuple[0] for note_tuple in notes_list])
    stop_words: set[Word] = td.stop_words()

    # Highlight 1st time
    notes_highlight_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front_field, DefaultFields.basic_back_field, stop_words, bold_format)
    col.update_notes(notes_highlight_result.notes)
    __assert_highlighted_notes(col, notes_list)

    # Highlight again
    notes_highlight_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, DefaultFields.basic_front_field, DefaultFields.basic_back_field, stop_words, bold_format)
    col.update_notes(notes_highlight_result.notes)
    __assert_highlighted_notes(col, notes_list)

    # Erase
    notes_erase_result: NotesHighlighterResult = notes_highlighter.erase(notes, DefaultFields.basic_back_field)
    col.update_notes(notes_erase_result.notes)
    __assert_original_notes(col, notes_list)
