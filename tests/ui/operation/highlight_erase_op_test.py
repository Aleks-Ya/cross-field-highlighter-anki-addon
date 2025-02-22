from unittest.mock import Mock

from anki.models import NotetypeId
from anki.notes import NoteId, Note
from aqt import QWidget
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from tenacity import retry, stop_after_attempt, wait_fixed

from cross_field_highlighter.common.collection_holder import CollectionHolder
from cross_field_highlighter.config.config import Config
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.types import FieldNames, FieldName, Text
from cross_field_highlighter.ui.operation.erase_op import EraseOp
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from cross_field_highlighter.ui.operation.highlight_op import HighlightOp
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.operation.op_statistics import OpStatistics, OpStatisticsKey
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter
from tests.data import Data, DefaultFields, CaseNote


def test_highlight_and_erase_cases(collection_holder: CollectionHolder, notes_highlighter: NotesHighlighter,
                                   task_manager: TaskManager, td: Data, bold_format: HighlightFormat,
                                   note_type_id_basic: NotetypeId, op_statistics_formatter: OpStatisticsFormatter,
                                   config: Config):
    progress_manager: ProgressManager = Mock()
    progress_manager.want_cancel = Mock(return_value=False)
    parent: QWidget = QWidget()
    case_notes: list[CaseNote] = td.create_case_notes()
    note_ids: set[NoteId] = {case_note.note.id for case_note in case_notes}
    destination_fields: FieldNames = FieldNames([DefaultFields.basic_back])
    exp_selected: int = len(case_notes)
    exp_modified: int = 44
    exp_statistics: dict[OpStatisticsKey, int] = {OpStatisticsKey.TARGET_NOTE_TYPE_ID: note_type_id_basic,
                                                  OpStatisticsKey.NOTES_SELECTED_ALL: exp_selected,
                                                  OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE: exp_selected,
                                                  OpStatisticsKey.NOTES_PROCESSED: exp_selected,
                                                  OpStatisticsKey.NOTES_MODIFIED: exp_modified,
                                                  OpStatisticsKey.FIELDS_PROCESSED: exp_selected,
                                                  OpStatisticsKey.FIELDS_MODIFIED: exp_modified}

    # Highlight
    td.assert_original_case_notes(case_notes)
    stop_words: Text = td.stop_words()
    source_field: FieldName = DefaultFields.basic_front
    highlight_op_params: HighlightOpParams = HighlightOpParams(note_type_id_basic, source_field, destination_fields,
                                                               stop_words, bold_format)
    highlight_op: HighlightOp = HighlightOp(collection_holder, notes_highlighter, task_manager, progress_manager,
                                            note_ids, op_statistics_formatter, True, lambda: None, parent,
                                            highlight_op_params, config)
    highlight_op.run_in_background()
    retry(stop=stop_after_attempt(5), wait=wait_fixed(1))(lambda: td.assert_highlighted_case_notes(case_notes))()
    highlight_statistics: OpStatistics = highlight_op.get_statistics()
    assert highlight_statistics.as_dict() == exp_statistics

    # Erase
    erase_op_params: EraseOpParams = EraseOpParams(note_type_id_basic, destination_fields)
    erase_op: EraseOp = EraseOp(collection_holder, notes_highlighter, task_manager, progress_manager, note_ids,
                                op_statistics_formatter, True, lambda: None, parent, erase_op_params, config)
    erase_op.run_in_background()
    retry(stop=stop_after_attempt(5), wait=wait_fixed(1))(lambda: td.assert_original_case_notes(case_notes))()
    td.assert_original_case_notes(case_notes)
    erase_statistics: OpStatistics = erase_op.get_statistics()
    assert erase_statistics.as_dict() == exp_statistics


def test_highlight_and_erase_different_note_types(
        collection_holder: CollectionHolder, notes_highlighter: NotesHighlighter, task_manager: TaskManager, td: Data,
        bold_format: HighlightFormat, note_type_id_basic: NotetypeId, op_statistics_formatter: OpStatisticsFormatter,
        config: Config):
    parent: QWidget = QWidget()
    progress_manager: ProgressManager = Mock()
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    note_3: Note = td.create_cloze_note()
    note_ids: set[NoteId] = {note_1.id, note_2.id, note_3.id}
    destination_fields: FieldNames = FieldNames([DefaultFields.basic_back, DefaultFields.basic_extra])
    exp_statistics: dict[OpStatisticsKey, int] = {OpStatisticsKey.TARGET_NOTE_TYPE_ID: note_type_id_basic,
                                                  OpStatisticsKey.NOTES_SELECTED_ALL: 3,
                                                  OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE: 2,
                                                  OpStatisticsKey.NOTES_PROCESSED: 2,
                                                  OpStatisticsKey.NOTES_MODIFIED: 2,
                                                  OpStatisticsKey.FIELDS_PROCESSED: 4,
                                                  OpStatisticsKey.FIELDS_MODIFIED: 4}

    # Highlight
    stop_words: Text = td.stop_words()
    source_field: FieldName = DefaultFields.basic_front
    highlight_op_params: HighlightOpParams = HighlightOpParams(note_type_id_basic, source_field, destination_fields,
                                                               stop_words, bold_format)
    highlight_op: HighlightOp = HighlightOp(collection_holder, notes_highlighter, task_manager, progress_manager,
                                            note_ids, op_statistics_formatter, True, lambda: None, parent,
                                            highlight_op_params, config)
    highlight_op.run_in_background()

    def assert_function_highlight():
        assert collection_holder.col().get_note(note_1.id)[
                   DefaultFields.basic_back] == 'Text <b class="cross-field-highlighter">content</b>'
        assert collection_holder.col().get_note(note_1.id)[
                   DefaultFields.basic_extra] == 'Extra <b class="cross-field-highlighter">content</b>'
        assert collection_holder.col().get_note(note_2.id)[DefaultFields.basic_back] == \
               'Back <b class="cross-field-highlighter">content</b> <b class="cross-field-highlighter">2</b>'
        assert collection_holder.col().get_note(note_2.id)[DefaultFields.basic_extra] == \
               'Extra <b class="cross-field-highlighter">content</b> <b class="cross-field-highlighter">2</b>'
        assert collection_holder.col().get_note(note_3.id).fields == note_3.fields
        highlight_statistics: OpStatistics = highlight_op.get_statistics()
        assert highlight_statistics.as_dict() == exp_statistics

    retry(stop=stop_after_attempt(5), wait=wait_fixed(1))(assert_function_highlight)()

    # Erase
    erase_op_params: EraseOpParams = EraseOpParams(note_type_id_basic, destination_fields)
    erase_op: EraseOp = EraseOp(collection_holder, notes_highlighter, task_manager, progress_manager, set(note_ids),
                                op_statistics_formatter, True, lambda: None, parent, erase_op_params, config)
    erase_op.run_in_background()

    def assert_function_erase():
        assert collection_holder.col().get_note(note_1.id)[DefaultFields.basic_back] == note_1[DefaultFields.basic_back]
        assert collection_holder.col().get_note(note_1.id)[DefaultFields.basic_extra] == note_1[
            DefaultFields.basic_extra]
        assert collection_holder.col().get_note(note_2.id)[DefaultFields.basic_back] == note_2[DefaultFields.basic_back]
        assert collection_holder.col().get_note(note_2.id)[DefaultFields.basic_extra] == note_2[
            DefaultFields.basic_extra]
        assert collection_holder.col().get_note(note_3.id).fields == note_3.fields
        erase_statistics: OpStatistics = erase_op.get_statistics()
        assert erase_statistics.as_dict() == exp_statistics

    retry(stop=stop_after_attempt(5), wait=wait_fixed(1))(assert_function_erase)()
