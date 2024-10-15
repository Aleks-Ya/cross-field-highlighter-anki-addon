import time

from aqt import QWidget
from anki.collection import Collection
from anki.notes import Note, NoteId
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from mock.mock import MagicMock

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.types import FieldContent, Word, FieldNames, Notes, FieldName
from cross_field_highlighter.ui.operation.highlight_op import HighlightOp
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
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


def test_highlight_erase(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                         progress_manager: ProgressManager, td: Data, bold_format: HighlightFormat):
    notes_list: list[(Note, FieldContent, FieldContent)] = td.create_case_notes()
    notes: Notes = Notes([note_tuple[0] for note_tuple in notes_list])
    note_ids: set[NoteId] = {note.id for note in notes}
    stop_words: set[Word] = td.stop_words()
    source_field: FieldName = DefaultFields.basic_front_field
    fields: FieldNames = FieldNames([DefaultFields.basic_back_field])
    parent: QWidget = MagicMock()

    highlight_op_params: HighlightOpParams = HighlightOpParams(note_ids, parent, source_field, fields, stop_words,
                                                               bold_format)
    highlight_op: HighlightOp = HighlightOp(col, notes_highlighter, task_manager, progress_manager, highlight_op_params,
                                            lambda: None)
    highlight_op.run_in_background()
    time.sleep(1)
    __assert_highlighted_notes(col, notes_list)
