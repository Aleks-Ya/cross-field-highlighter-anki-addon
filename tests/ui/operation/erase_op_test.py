import time
from unittest.mock import Mock

from anki.models import NotetypeId
from aqt import QWidget
from anki.collection import Collection
from anki.notes import NoteId, Note
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import FieldNames, Notes, FieldName, Text
from cross_field_highlighter.ui.operation.erase_op import EraseOp
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from cross_field_highlighter.ui.operation.op_statistics import OpStatistics
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter
from tests.data import Data, DefaultFields, CaseNote


def test_erase(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
               td: Data, bold_format: HighlightFormat, basic_note_type_id: NotetypeId,
               op_statistics_formatter: OpStatisticsFormatter):
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

    erase_op_params: EraseOpParams = EraseOpParams(basic_note_type_id, parent, fields)
    erase_op: EraseOp = EraseOp(col, notes_highlighter, task_manager, progress_manager, note_ids,
                                op_statistics_formatter, erase_op_params, lambda: None)
    erase_op.run_in_background()
    time.sleep(1)
    td.assert_original_case_notes(case_notes)

    statistics: OpStatistics = erase_op.get_statistics()
    assert statistics.as_dict() == {'notes_selected': len(case_notes),
                                    'notes_processed': 13,
                                    'notes_modified': 12}


def test_statistics(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                    td: Data, bold_format: HighlightFormat, basic_note_type_id: NotetypeId,
                    op_statistics_formatter: OpStatisticsFormatter):
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    notes: Notes = Notes([note_1, note_2])
    note_ids: set[NoteId] = {note.id for note in notes}

    fields: FieldNames = FieldNames([DefaultFields.basic_back_field])
    parent: QWidget = QWidget()

    source_field: FieldName = DefaultFields.basic_front_field
    stop_words: Text = td.stop_words()
    notes_highlighter_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, source_field, fields[0], stop_words, bold_format)
    col.update_notes(notes_highlighter_result.notes)

    progress_manager: ProgressManager = Mock()

    erase_op_params: EraseOpParams = EraseOpParams(basic_note_type_id, parent, fields)
    erase_op: EraseOp = EraseOp(col, notes_highlighter, task_manager, progress_manager, note_ids,
                                op_statistics_formatter, erase_op_params, lambda: None)
    erase_op.run_in_background()
    time.sleep(1)

    statistics: OpStatistics = erase_op.get_statistics()
    assert statistics.as_dict() == {'notes_selected': len(notes),
                                    'notes_processed': 2,
                                    'notes_modified': 2}
