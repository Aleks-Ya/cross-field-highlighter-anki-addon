from typing import Optional

from PyQtPath.path_chain_pyqt6 import path, PyQtPath
from aqt import QComboBox, QDialogButtonBox, QPushButton, QLineEdit

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import \
    AdhocHighlightDialogModelListener, AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.widgets.note_type_combo_box_layout import NoteTypeComboBoxLayout
from cross_field_highlighter.ui.widgets.titled_combo_box_layout import TitledComboBoxLayout
from cross_field_highlighter.ui.widgets.titled_line_edit_layout import TitledLineEditLayout
from tests.qtget import get_item_texts, get_item_datas
from tests.ui.dialog.adhoc.fields_layout_asserts import assert_fields_layout


class FakeCallback:
    def __init__(self):
        self.counter: int = 0

    def call(self):
        self.counter += 1


class HighlightFakeModelListener(AdhocHighlightDialogModelListener):
    def __init__(self):
        self.counter: int = 0

    def highlight_model_changed(self, source: object, _: AdhocHighlightDialogModel):
        self.counter += 1


class FakeHighlightControllerCallback:
    def __init__(self):
        self.history: list[HighlightOpParams] = []

    def call(self, params: HighlightOpParams):
        self.history.append(params)


def assert_view(view: AdhocHighlightDialogView, window_title: str, selected_note_type: Optional[NoteTypeDetails],
                note_types: list[NoteTypeDetails], selected_source_field: str, source_fields: list[str],
                selected_format: Optional[HighlightFormat], formats: list[HighlightFormat], check_box_texts: list[str],
                selected_destination_fields: list[str], disabled_fields: list[str], stop_words: str):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == window_title, f"'{view.windowTitle()}' != '{window_title}'"
    exp_start_button_enabled: bool = len(list(set(selected_destination_fields) - set(disabled_fields))) > 0
    assert_source_group_box(view, selected_note_type, note_types, selected_source_field, source_fields, stop_words)
    assert_format_group_box(view, selected_format, formats)
    assert_destination_group_box(view, check_box_texts, selected_destination_fields, disabled_fields)
    assert_buttons(view, exp_start_button_enabled)


def assert_source_group_box(view: AdhocHighlightDialogView, selected_note_type: Optional[NoteTypeDetails],
                            note_types: list[NoteTypeDetails], selected_source_field: str, source_fields: list[str],
                            stop_words: str):
    group_box: PyQtPath = path(view).group(0)

    note_type: PyQtPath = group_box.child(NoteTypeComboBoxLayout)
    assert note_type.label().get().text() == "Note type:"
    note_type_combo_box: QComboBox = note_type.combobox().get()
    act_selected_note_type: NoteTypeDetails = note_type_combo_box.currentData()
    assert act_selected_note_type == selected_note_type, f"'{act_selected_note_type}' != '{selected_note_type}'"
    act_note_types: list[NoteTypeDetails] = get_item_datas(note_type_combo_box)
    assert act_note_types == note_types, f"all note types: '{act_note_types}' != '{note_types}'"

    assert_source_combo_box(view, selected_source_field, source_fields)
    assert_stop_words(view, stop_words)


def assert_stop_words(view: AdhocHighlightDialogView, stop_words: str):
    group_box: PyQtPath = path(view).group(0)
    act_stop_words: str = group_box.child(TitledLineEditLayout).child(QLineEdit).get().text()
    assert act_stop_words == stop_words, f"'{act_stop_words}' != '{stop_words}'"


def assert_source_combo_box(view: AdhocHighlightDialogView, selected_source_field: str, source_fields: list[str]):
    group_box: PyQtPath = path(view).group(0)
    field_path: PyQtPath = group_box.child(TitledComboBoxLayout)
    assert field_path.label().get().text() == "Field:"
    field_combo_box: QComboBox = field_path.combobox().get()
    assert field_combo_box.currentText() == selected_source_field, \
        f"current_source_field: '{selected_source_field}' != '{field_combo_box.currentText()}'"
    assert get_item_texts(
        field_combo_box) == source_fields, f"all source fields: '{get_item_texts(field_combo_box)}' != '{source_fields}'"


def assert_format_group_box(view: AdhocHighlightDialogView, selected_format: Optional[HighlightFormat],
                            formats: list[HighlightFormat]):
    combo_box: PyQtPath = path(view).group(1).child(TitledComboBoxLayout)
    assert combo_box.label().get().text() == "Format:"
    format_combo_box: QComboBox = combo_box.combobox().get()
    act_current_text: str = format_combo_box.currentText()
    exp_current_text: str = (selected_format.name if selected_format else "")
    assert act_current_text == exp_current_text, f"'{act_current_text}' != '{exp_current_text}'"
    format_names: list[str] = [highlight_format.name for highlight_format in formats]
    act_format_names: list[str] = get_item_texts(format_combo_box)
    assert act_format_names == format_names, f"all format names: '{act_format_names}' != '{format_names}'"


def assert_destination_group_box(view: AdhocHighlightDialogView, check_box_texts: list[str],
                                 selected_destination_fields: list[str], disabled_fields: list[str]):
    group_box: PyQtPath = path(view).group(2)
    assert group_box.label().get().text() == "Fields:"
    fields_layout: FieldsLayout = group_box.child(FieldsLayout).get()
    assert_fields_layout(fields_layout, check_box_texts, selected_destination_fields, disabled_fields)


def assert_buttons(view: AdhocHighlightDialogView, start_button_enabled: bool):
    start_button: QPushButton = path(view).child(QDialogButtonBox).button(0).get()
    assert start_button.text() == "&Start"
    assert start_button.isEnabled() == start_button_enabled, f"'{start_button.isEnabled()}' != '{start_button_enabled}'"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    act_cancel_button_text: str = cancel_button.text()
    exp_cancel_button_text: str = "&Cancel"
    assert act_cancel_button_text == exp_cancel_button_text, f"'{act_cancel_button_text}' != '{exp_cancel_button_text}'"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"
