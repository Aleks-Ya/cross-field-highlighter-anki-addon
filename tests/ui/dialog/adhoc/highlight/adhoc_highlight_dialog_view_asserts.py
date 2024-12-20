from typing import Optional

from PyQtPath.path_chain_pyqt6 import path, PyQtPath
from aqt import QComboBox, QDialogButtonBox, QPushButton, QLineEdit, QCheckBox

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import \
    AdhocHighlightDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.widgets.note_type_combo_box_layout import NoteTypeComboBoxLayout
from cross_field_highlighter.ui.widgets.titled_combo_box_layout import TitledComboBoxLayout
from cross_field_highlighter.ui.widgets.titled_line_edit_layout import TitledLineEditLayout
from tests.qtget import get_items
from tests.ui.dialog.adhoc.fields_layout_asserts import assert_fields_layout


class FakeCallback:
    def __init__(self):
        self.counter: int = 0

    def call(self):
        self.counter += 1


class FakeModelListener(AdhocHighlightDialogModelListener):
    def __init__(self):
        self.counter: int = 0

    def model_changed(self, source: object):
        self.counter += 1


class FakeHighlightControllerCallback:
    def __init__(self):
        self.history: list[HighlightOpParams] = []

    def call(self, params: HighlightOpParams):
        self.history.append(params)


def assert_view(view: AdhocHighlightDialogView, window_title: str, selected_note_type: str, note_types: list[str],
                selected_source_field: str, source_fields: list[str], selected_format: Optional[HighlightFormat],
                formats: list[HighlightFormat], check_box_texts: list[str], selected_fields: list[str],
                disabled_fields: list[str], stop_words: str, space_delimited_language: bool):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == window_title, f"'{view.windowTitle()}' != '{window_title}'"
    assert_buttons(view)
    assert_source_group_box(view, selected_note_type, note_types, selected_source_field, source_fields, stop_words,
                            space_delimited_language)
    assert_format_group_box(view, selected_format, formats)
    assert_destination_group_box(view, check_box_texts, selected_fields, disabled_fields)


def assert_source_group_box(view: AdhocHighlightDialogView, selected_note_type: str, note_types: list[str],
                            selected_source_field: str, source_fields: list[str], stop_words: str,
                            space_delimited_language: bool):
    group_box: PyQtPath = path(view).group(0)

    note_type: PyQtPath = group_box.child(NoteTypeComboBoxLayout)
    assert note_type.label().get().text() == "Note Type"
    note_type_combo_box: QComboBox = note_type.combobox().get()
    assert note_type_combo_box.currentText() == selected_note_type
    assert get_items(note_type_combo_box) == note_types

    assert_source_combo_box(view, selected_source_field, source_fields)
    assert_stop_words(view, stop_words)
    assert_space_delimited_language(view, space_delimited_language)


def assert_stop_words(view: AdhocHighlightDialogView, stop_words: str):
    group_box: PyQtPath = path(view).group(0)
    act_stop_words: str = group_box.child(TitledLineEditLayout).child(QLineEdit).get().text()
    assert act_stop_words == stop_words, f"'{act_stop_words}' != '{stop_words}'"


def assert_space_delimited_language(view: AdhocHighlightDialogView, space_delimited_language: bool):
    group_box: PyQtPath = path(view).group(0)
    check_box: QCheckBox = group_box.checkbox().get()
    assert check_box.text() == "Space-delimited language"
    # noinspection PyUnresolvedReferences
    assert check_box.toolTip() == "Checked for English, Spanish, French, etc.\nUnchecked for Japanese, Chinese, Thai, etc."
    is_checked: bool = check_box.isChecked()
    assert is_checked == space_delimited_language, f"'{is_checked}' != '{space_delimited_language}'"


def assert_source_combo_box(view: AdhocHighlightDialogView, selected_source_field: str, source_fields: list[str]):
    group_box: PyQtPath = path(view).group(0)
    field_path: PyQtPath = group_box.child(TitledComboBoxLayout)
    assert field_path.label().get().text() == "Field"
    field_combo_box: QComboBox = field_path.combobox().get()
    assert field_combo_box.currentText() == selected_source_field, \
        f"current_source_field: '{selected_source_field}' != '{field_combo_box.currentText()}'"
    assert get_items(
        field_combo_box) == source_fields, f"all source fields: '{get_items(field_combo_box)}' != '{source_fields}'"


def assert_format_group_box(view: AdhocHighlightDialogView, selected_format: Optional[HighlightFormat],
                            formats: list[HighlightFormat]):
    combo_box: PyQtPath = path(view).group(1).child(TitledComboBoxLayout)
    assert combo_box.label().get().text() == "Format"
    format_combo_box: QComboBox = combo_box.combobox().get()
    assert format_combo_box.currentText() == (selected_format.name if selected_format else "")
    format_names: list[str] = [highlight_format.name for highlight_format in formats]
    assert get_items(format_combo_box) == format_names


def assert_destination_group_box(view: AdhocHighlightDialogView, check_box_texts: list[str],
                                 selected_fields: list[str], disabled_fields: list[str]):
    group_box: PyQtPath = path(view).group(2)
    assert group_box.label().get().text() == "Fields:"
    fields_layout: FieldsLayout = group_box.child(FieldsLayout).get()
    assert_fields_layout(fields_layout, check_box_texts, selected_fields, disabled_fields)


def assert_buttons(view: AdhocHighlightDialogView):
    start_button: QPushButton = path(view).child(QDialogButtonBox).button(0).get()
    assert start_button.text() == "&Start"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    act_cancel_button_text: str = cancel_button.text()
    exp_cancel_button_text: str = "&Cancel"
    assert act_cancel_button_text == exp_cancel_button_text, f"'{act_cancel_button_text}' != '{exp_cancel_button_text}'"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"
