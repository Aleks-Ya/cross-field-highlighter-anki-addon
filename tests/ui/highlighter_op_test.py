import time

from anki.collection import Collection
from anki.notes import Note, NoteId
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from mock.mock import MagicMock

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.types import FieldContent, Word, FieldNames
from cross_field_highlighter.ui.operation.highlight_op import HighlightOp
from tests.data import Data, DefaultFields


def __assert_highlighted_notes(col: Collection, contents: list[(Note, FieldContent, FieldContent)]) -> None:
    for content_tuple in contents:
        exp_note: Note = content_tuple[0]
        act_note: Note = col.get_note(exp_note.id)
        highlighted_content: FieldContent = content_tuple[2]
        assert act_note[DefaultFields.text_field_name] == highlighted_content


def __assert_original_notes(col: Collection, contents: list[(Note, FieldContent, FieldContent)]) -> None:
    for content_tuple in contents:
        exp_note: Note = content_tuple[0]
        act_note: Note = col.get_note(exp_note.id)
        original_content: FieldContent = content_tuple[1]
        assert act_note[DefaultFields.text_field_name] == original_content


def test_highlight_erase(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                         progress_manager: ProgressManager, td: Data):
    notes_list: list[(Note, FieldContent, FieldContent)] = td.create_case_notes()
    notes: list[Note] = [note_tuple[0] for note_tuple in notes_list]
    note_ids: set[NoteId] = {note.id for note in notes}
    stop_words: set[Word] = td.stop_words()
    highlight_format: HighlightFormat = HighlightFormat.BOLD
    highlight_op: HighlightOp = HighlightOp(col, notes_highlighter, task_manager, progress_manager,
                                            MagicMock(), note_ids, DefaultFields.word_field_name,
                                            FieldNames([DefaultFields.text_field_name]), stop_words, highlight_format,
                                            lambda: None)

    highlight_op.run_in_background()
    time.sleep(1)
    __assert_highlighted_notes(col, notes_list)
