import time
from unittest.mock import Mock

from anki.models import NoteType
from aqt import QWidget
from anki.collection import Collection
from anki.notes import NoteId
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import FieldNames, Notes, FieldName, Text
from cross_field_highlighter.ui.operation.erase_op import EraseOp
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from tests.data import Data, DefaultFields, CaseNote


def test_erase(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
               td: Data, bold_format: HighlightFormat, basic_note_type: NoteType):
    case_notes: list[CaseNote] = td.create_case_notes()
    td.assert_original_case_notes(case_notes)
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    note_ids: set[NoteId] = {note.id for note in notes}
    fields: FieldNames = FieldNames([DefaultFields.basic_back_field])
    parent: QWidget = QWidget()

    source_field: FieldName = DefaultFields.basic_front_field
    stop_words: Text = td.stop_words()
    notes_highlighter_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, source_field, fields[0], stop_words, bold_format)
    col.update_notes(notes_highlighter_result.notes)
    td.assert_highlighted_case_notes(case_notes)

    progress_manager: ProgressManager = Mock()

    erase_op_params: EraseOpParams = EraseOpParams(basic_note_type['id'], parent, fields)
    erase_op: EraseOp = EraseOp(col, notes_highlighter, task_manager, progress_manager, note_ids, erase_op_params,
                                lambda: None)
    erase_op.run_in_background()
    time.sleep(1)
    td.assert_original_case_notes(case_notes)
