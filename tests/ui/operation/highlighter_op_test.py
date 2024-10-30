import time

from anki.models import NoteType
from aqt import QWidget
from anki.collection import Collection
from anki.notes import NoteId
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
                   td: Data, bold_format: HighlightFormat, basic_note_type: NoteType,
                   op_statistics_formatter: OpStatisticsFormatter):
    case_notes: list[CaseNote] = td.create_case_notes()
    td.assert_original_case_notes(case_notes)
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    note_ids: set[NoteId] = {note.id for note in notes}
    stop_words: Text = td.stop_words()
    source_field: FieldName = DefaultFields.basic_front_field
    fields: FieldNames = FieldNames([DefaultFields.basic_back_field])
    parent: QWidget = QWidget()
    progress_manager: ProgressManager = Mock()

    highlight_op_params: HighlightOpParams = HighlightOpParams(basic_note_type['id'], note_ids, parent, source_field,
                                                               fields, stop_words, bold_format)
    highlight_op: HighlightOp = HighlightOp(col, notes_highlighter, task_manager, progress_manager, highlight_op_params,
                                            op_statistics_formatter, lambda: None)
    highlight_op.run_in_background()
    time.sleep(1)
    td.assert_highlighted_case_notes(case_notes)
