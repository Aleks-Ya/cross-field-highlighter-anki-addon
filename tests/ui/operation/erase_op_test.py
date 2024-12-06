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
from cross_field_highlighter.ui.operation.highlight_op import HighlightOp
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.operation.op_statistics import OpStatistics, OpStatisticsKey
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter
from tests.data import Data, DefaultFields, CaseNote


def test_erase(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
               td: Data, bold_format: HighlightFormat, basic_note_type_id: NotetypeId,
               op_statistics_formatter: OpStatisticsFormatter):
    case_notes: list[CaseNote] = td.create_case_notes()
    td.assert_original_case_notes(case_notes)
    notes: Notes = Notes([case_note.note for case_note in case_notes])
    note_ids: set[NoteId] = {note.id for note in notes}
    fields: FieldNames = FieldNames([DefaultFields.basic_back])
    parent: QWidget = QWidget()
    space_delimited_language: bool = True

    source_field: FieldName = DefaultFields.basic_front
    stop_words: Text = td.stop_words()
    notes_highlighter_result: NotesHighlighterResult = notes_highlighter.highlight(
        notes, source_field, fields, stop_words, space_delimited_language, bold_format)
    col.update_notes(notes_highlighter_result.notes)
    td.assert_highlighted_case_notes(case_notes, space_delimited_language)

    progress_manager: ProgressManager = Mock()

    erase_op_params: EraseOpParams = EraseOpParams(basic_note_type_id, parent, fields)
    erase_op: EraseOp = EraseOp(col, notes_highlighter, task_manager, progress_manager, note_ids,
                                op_statistics_formatter, lambda: None, erase_op_params)
    erase_op.run_in_background()
    time.sleep(1)
    td.assert_original_case_notes(case_notes)

    statistics: OpStatistics = erase_op.get_statistics()
    assert statistics.as_dict() == {OpStatisticsKey.TARGET_NOTE_TYPE_ID: basic_note_type_id,
                                    OpStatisticsKey.NOTES_SELECTED_ALL: 17,
                                    OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE: 17,
                                    OpStatisticsKey.NOTES_PROCESSED: 17,
                                    OpStatisticsKey.NOTES_MODIFIED: 16,
                                    OpStatisticsKey.FIELDS_PROCESSED: 17,
                                    OpStatisticsKey.FIELDS_MODIFIED: 16}


def test_erase_different_note_types(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                                    td: Data, bold_format: HighlightFormat, basic_note_type_id: NotetypeId,
                                    op_statistics_formatter: OpStatisticsFormatter):
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    note_3: Note = td.create_cloze_note()
    notes: Notes = Notes([note_1, note_2, note_3])
    note_ids: set[NoteId] = {note.id for note in notes}

    stop_words: Text = td.stop_words()
    source_field: FieldName = DefaultFields.basic_front
    destination_fields: FieldNames = FieldNames([DefaultFields.basic_back, DefaultFields.basic_extra])
    parent: QWidget = QWidget()
    progress_manager: ProgressManager = Mock()
    space_delimited_language: bool = True

    highlight_op_params: HighlightOpParams = HighlightOpParams(basic_note_type_id, parent, source_field,
                                                               space_delimited_language, destination_fields, stop_words,
                                                               bold_format)
    highlight_op: HighlightOp = HighlightOp(col, notes_highlighter, task_manager, progress_manager, note_ids,
                                            op_statistics_formatter, lambda: None, highlight_op_params)
    highlight_op.run_in_background()
    time.sleep(1)
    assert col.get_note(note_1.id)[DefaultFields.basic_back] == 'Text <b class="cross-field-highlighter">content</b>'
    assert col.get_note(note_1.id)[DefaultFields.basic_extra] == 'Extra <b class="cross-field-highlighter">content</b>'
    assert col.get_note(note_2.id)[DefaultFields.basic_back] == \
           'Back <b class="cross-field-highlighter">content</b> <b class="cross-field-highlighter">2</b>'
    assert col.get_note(note_2.id)[DefaultFields.basic_extra] == \
           'Extra <b class="cross-field-highlighter">content</b> <b class="cross-field-highlighter">2</b>'
    assert col.get_note(note_3.id).fields == note_3.fields

    erase_op_params: EraseOpParams = EraseOpParams(basic_note_type_id, parent, destination_fields)
    erase_op: EraseOp = EraseOp(col, notes_highlighter, task_manager, progress_manager, set(note_ids),
                                op_statistics_formatter, lambda: None, erase_op_params)
    erase_op.run_in_background()
    time.sleep(1)
    assert col.get_note(note_1.id)[DefaultFields.basic_back] == note_1[DefaultFields.basic_back]
    assert col.get_note(note_1.id)[DefaultFields.basic_extra] == note_1[DefaultFields.basic_extra]
    assert col.get_note(note_2.id)[DefaultFields.basic_back] == note_2[DefaultFields.basic_back]
    assert col.get_note(note_2.id)[DefaultFields.basic_extra] == note_2[DefaultFields.basic_extra]
    assert col.get_note(note_3.id).fields == note_3.fields

    statistics: OpStatistics = erase_op.get_statistics()
    assert statistics.as_dict() == {OpStatisticsKey.TARGET_NOTE_TYPE_ID: basic_note_type_id,
                                    OpStatisticsKey.NOTES_SELECTED_ALL: 3,
                                    OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE: 2,
                                    OpStatisticsKey.NOTES_PROCESSED: 2,
                                    OpStatisticsKey.NOTES_MODIFIED: 2,
                                    OpStatisticsKey.FIELDS_PROCESSED: 4,
                                    OpStatisticsKey.FIELDS_MODIFIED: 4}
