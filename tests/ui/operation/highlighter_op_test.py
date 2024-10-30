import time

from anki.models import NotetypeId
from aqt import QWidget
from anki.collection import Collection
from anki.notes import NoteId, Note
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from mock.mock import Mock

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.types import FieldNames, Notes, FieldName, Text
from cross_field_highlighter.ui.operation.highlight_op import HighlightOp
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter
from tests.data import Data, DefaultFields, CaseNote


def test_highlight(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                   td: Data, bold_format: HighlightFormat, basic_note_type_id: NotetypeId,
                   op_statistics_formatter: OpStatisticsFormatter):
    case_notes: list[CaseNote] = td.create_case_notes()
    td.assert_original_case_notes(case_notes)
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    note_ids: set[NoteId] = {note.id for note in notes}
    stop_words: Text = td.stop_words()
    source_field: FieldName = DefaultFields.basic_front_field
    destination_fields: FieldNames = FieldNames([DefaultFields.basic_back_field])
    parent: QWidget = QWidget()
    progress_manager: ProgressManager = Mock()

    highlight_op_params: HighlightOpParams = HighlightOpParams(basic_note_type_id, note_ids, parent, source_field,
                                                               destination_fields, stop_words, bold_format)
    highlight_op: HighlightOp = HighlightOp(col, notes_highlighter, task_manager, progress_manager, highlight_op_params,
                                            op_statistics_formatter, lambda: None)
    highlight_op.run_in_background()
    time.sleep(1)
    td.assert_highlighted_case_notes(case_notes)


def test_highlight_different_note_types(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                                        td: Data, bold_format: HighlightFormat, basic_note_type_id: NotetypeId,
                                        op_statistics_formatter: OpStatisticsFormatter):
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    note_3: Note = td.create_cloze_note()
    notes: Notes = Notes([note_1, note_2, note_3])
    note_ids: set[NoteId] = {note.id for note in notes}

    stop_words: Text = td.stop_words()
    source_field: FieldName = DefaultFields.basic_front_field
    destination_fields: FieldNames = FieldNames([DefaultFields.basic_back_field])
    parent: QWidget = QWidget()
    progress_manager: ProgressManager = Mock()

    highlight_op_params: HighlightOpParams = HighlightOpParams(basic_note_type_id, note_ids, parent, source_field,
                                                               destination_fields, stop_words, bold_format)
    highlight_op: HighlightOp = HighlightOp(col, notes_highlighter, task_manager, progress_manager, highlight_op_params,
                                            op_statistics_formatter, lambda: None)
    highlight_op.run_in_background()
    time.sleep(1)
    assert col.get_note(note_1.id)[
               DefaultFields.basic_back_field] == 'Text <b class="cross-field-highlighter">content</b>'
    assert col.get_note(note_2.id)[
               DefaultFields.basic_back_field] == 'Back <b class="cross-field-highlighter">content</b> <b class="cross-field-highlighter">2</b>'
    assert col.get_note(note_3.id).fields == note_3.fields
