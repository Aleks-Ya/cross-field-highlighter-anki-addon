from PyQt6.QtWidgets import QCheckBox, QDialogButtonBox, QPushButton
from PyQtPath.path_chain_pyqt6 import path, PyQtPath
from pytestqt.qtbot import QtBot
from aqt import QComboBox, Qt

from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormatCode, HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldName, FieldNames, Word
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout, TitledLineEditLayout
from tests.qtget import get_items


class FakeCallback:
    params = None

    @staticmethod
    def call(params: HighlightOpParams):
        FakeCallback.params = params


def test_view(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
              adhoc_highlight_dialog_model: AdhocHighlightDialogModel, basic_note_type_details: NoteTypeDetails,
              cloze_note_type_details: NoteTypeDetails, formatter_facade: FormatterFacade, qtbot: QtBot):
    # Initial state
    __assert_view(adhoc_highlight_dialog_view, current_note_type="", note_types=[], current_field="", source_fields=[],
                  formats=[], check_box_texts=[], selected_fields=[], disabled_field="")
    # Fill model without firing
    adhoc_highlight_dialog_model.note_types = [basic_note_type_details, cloze_note_type_details]
    adhoc_highlight_dialog_model.formats = formatter_facade.get_all_formats()
    adhoc_highlight_dialog_model.run_op_callback = FakeCallback.call
    __assert_view(adhoc_highlight_dialog_view, current_note_type="", note_types=[], current_field="", source_fields=[],
                  formats=[], check_box_texts=[], selected_fields=[], disabled_field="")
    # Fire model changes
    adhoc_highlight_dialog_model.fire_model_changed(None)
    __assert_view(adhoc_highlight_dialog_view, current_note_type="Basic", note_types=['Basic', 'Cloze'],
                  current_field="Front", source_fields=['Front', 'Back'],
                  formats=['Bold', 'Italic', 'Underline', 'Yellow background'],
                  check_box_texts=['Front', 'Back'], selected_fields=[], disabled_field="Front")
    # Choose Note Type
    note_type_combo_box: QComboBox = path(adhoc_highlight_dialog_view).group(0).child(
        TitledComboBoxLayout, 0).combobox().get()
    qtbot.mouseClick(note_type_combo_box, Qt.MouseButton.LeftButton)
    qtbot.keyClick(note_type_combo_box, Qt.Key.Key_Down)
    qtbot.keyClick(note_type_combo_box, Qt.Key.Key_Enter)
    __assert_view(adhoc_highlight_dialog_view, current_note_type="Cloze", note_types=['Basic', 'Cloze'],
                  current_field="Text", source_fields=['Text', 'Back Extra'],
                  formats=['Bold', 'Italic', 'Underline', 'Yellow background'],
                  check_box_texts=['Text', 'Back Extra'], selected_fields=[], disabled_field="Text")
    # Choose Field
    filed_combo_box: QComboBox = path(adhoc_highlight_dialog_view).group(0).child(
        TitledComboBoxLayout, 1).combobox().get()
    qtbot.mouseClick(filed_combo_box, Qt.MouseButton.LeftButton)
    qtbot.keyClick(filed_combo_box, Qt.Key.Key_Down)
    qtbot.keyClick(filed_combo_box, Qt.Key.Key_Enter)
    __assert_view(adhoc_highlight_dialog_view, current_note_type="Cloze", note_types=['Basic', 'Cloze'],
                  current_field="Back Extra", source_fields=['Text', 'Back Extra'],
                  formats=['Bold', 'Italic', 'Underline', 'Yellow background'],
                  check_box_texts=['Text', 'Back Extra'], selected_fields=[], disabled_field="Back Extra")
    # Click Start button
    assert FakeCallback.params is None
    button_box: QDialogButtonBox = path(adhoc_highlight_dialog_view).child(QDialogButtonBox).get()
    start_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
    qtbot.mouseClick(start_button, Qt.MouseButton.LeftButton)
    bold_format: HighlightFormat = formatter_facade.get_format_by_code(HighlightFormatCode.BOLD)
    assert FakeCallback.params == HighlightOpParams(note_type_id=cloze_note_type_details.note_type_id,
                                                    note_ids=set(), parent=None, source_field=FieldName("Back Extra"),
                                                    destination_fields=FieldNames([]),
                                                    stop_words={Word("a"), Word("an"), Word("to")},
                                                    highlight_format=bold_format)


def __assert_view(view: AdhocHighlightDialogView, current_note_type: str, note_types: list[str],
                  current_field: str, source_fields: list[str], formats: list[str], check_box_texts: list[str],
                  selected_fields: list[str], disabled_field: str):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == "Highlight"
    __assert_source_group_box(view, current_note_type, note_types, current_field, source_fields, "a an to")
    __assert_format_group_box(view, formats)
    __assert_destination_group_box(view, check_box_texts, selected_fields, disabled_field)


def __assert_source_group_box(view: AdhocHighlightDialogView, current_note_type: str, note_types: list[str],
                              current_field: str, source_fields: list[str], stop_words: str):
    group_box: PyQtPath = path(view).group(0)

    note_type: PyQtPath = group_box.child(TitledComboBoxLayout, 0)
    assert note_type.label().get().text() == "Note Type"
    note_type_combo_box: QComboBox = note_type.combobox().get()
    assert note_type_combo_box.currentText() == current_note_type
    assert get_items(note_type_combo_box) == note_types

    field_path: PyQtPath = group_box.child(TitledComboBoxLayout, 1)
    assert field_path.label().get().text() == "Field"
    field_combo_box: QComboBox = field_path.combobox().get()
    assert field_combo_box.currentText() == current_field
    assert get_items(field_combo_box) == source_fields

    assert group_box.child(TitledLineEditLayout).get().get_text() == stop_words


def __assert_format_group_box(view: AdhocHighlightDialogView, formats: list[str]):
    combo_box: PyQtPath = path(view).group(1).child(TitledComboBoxLayout)
    assert combo_box.label().get().text() == "Format"
    assert get_items(combo_box.combobox().get()) == formats


def __assert_destination_group_box(view: AdhocHighlightDialogView, check_box_texts: list[str],
                                   selected_fields: list[str], disabled_field: str):
    group_box: PyQtPath = path(view).group(2)
    assert group_box.label().get().text() == "Fields:"
    fields_layout: FieldsLayout = group_box.child(FieldsLayout).get()
    assert fields_layout.get_selected_field_names() == selected_fields
    check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    texts: list[str] = [check_box.text() for check_box in check_boxes]
    assert texts == check_box_texts
    for check_box in check_boxes:
        should_be_enabled: bool = check_box.text() != disabled_field
        assert check_box.isEnabled() == should_be_enabled


def test_repr(adhoc_highlight_dialog_view: AdhocHighlightDialogView):
    assert repr(adhoc_highlight_dialog_view) == "AdhocHighlightDialogView"
