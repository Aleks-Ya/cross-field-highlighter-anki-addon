import time

from anki.models import NoteType
from aqt import QWidget
from anki.collection import Collection
from anki.notes import Note, NoteId
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from mock.mock import MagicMock

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import FieldContent, Word, FieldNames, Notes, FieldName
from cross_field_highlighter.ui.operation.erase_op import EraseOp
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
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


def test_erase(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
               progress_manager: ProgressManager, td: Data, bold_format: HighlightFormat,
               basic_note_type: NoteType):
    notes_list: list[(Note, FieldContent, FieldContent)] = td.create_case_notes()
    __assert_original_notes(col, notes_list)
    notes: Notes = Notes([note_tuple[0] for note_tuple in notes_list])
    note_ids: set[NoteId] = {note.id for note in notes}
    fields: FieldNames = FieldNames([DefaultFields.basic_back_field])
    parent: QWidget = MagicMock()

    source_field: FieldName = DefaultFields.basic_front_field
    stop_words: set[Word] = td.stop_words()
    notes_highlighter_result: NotesHighlighterResult = notes_highlighter.highlight(notes, source_field, fields[0],
                                                                                   stop_words, bold_format)
    col.update_notes(notes_highlighter_result.notes)
    __assert_highlighted_notes(col, notes_list)

    erase_op_params: EraseOpParams = EraseOpParams(basic_note_type['id'], parent, fields)
    erase_op: EraseOp = EraseOp(col, notes_highlighter, task_manager, progress_manager, note_ids, erase_op_params,
                                lambda: None)
    erase_op.run_in_background()
    time.sleep(1)
    __assert_original_notes(col, notes_list)
