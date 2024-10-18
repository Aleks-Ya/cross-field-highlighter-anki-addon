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
from cross_field_highlighter.highlighter.types import Word, FieldNames, Notes, FieldName
from cross_field_highlighter.ui.operation.erase_op import EraseOp
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from tests.data import Data, DefaultFields, CaseNote


def __assert_highlighted_notes(col: Collection, case_notes: list[CaseNote]) -> None:
    for case_note in case_notes:
        act_note: Note = col.get_note(case_note.note.id)
        assert act_note[DefaultFields.basic_back_field] == case_note.highlighted_content


def __assert_original_notes(col: Collection, case_notes: list[CaseNote]) -> None:
    for case_note in case_notes:
        act_note: Note = col.get_note(case_note.note.id)
        assert act_note[DefaultFields.basic_back_field] == case_note.original_content


def test_erase(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
               progress_manager: ProgressManager, td: Data, bold_format: HighlightFormat,
               basic_note_type: NoteType):
    case_notes: list[CaseNote] = td.create_case_notes()
    __assert_original_notes(col, case_notes)
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    note_ids: set[NoteId] = {note.id for note in notes}
    fields: FieldNames = FieldNames([DefaultFields.basic_back_field])
    parent: QWidget = MagicMock()

    source_field: FieldName = DefaultFields.basic_front_field
    stop_words: set[Word] = td.stop_words()
    notes_highlighter_result: NotesHighlighterResult = notes_highlighter.highlight(notes, source_field, fields[0],
                                                                                   stop_words, bold_format)
    col.update_notes(notes_highlighter_result.notes)
    __assert_highlighted_notes(col, case_notes)

    erase_op_params: EraseOpParams = EraseOpParams(basic_note_type['id'], parent, fields)
    erase_op: EraseOp = EraseOp(col, notes_highlighter, task_manager, progress_manager, note_ids, erase_op_params,
                                lambda: None)
    erase_op.run_in_background()
    time.sleep(1)
    __assert_original_notes(col, case_notes)
