from typing import Optional

from PyQtPath.path_chain_pyqt6 import path, PyQtPath
from aqt import QComboBox, QDialogButtonBox, QPushButton, QLineEdit

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
        self.history: list[object] = []

    def model_changed(self, source: object):
        self.history.append(source)


class FakeHighlightControllerCallback:
    def __init__(self):
        self.history: list[HighlightOpParams] = []

    def call(self, params: HighlightOpParams):
        self.history.append(params)


def assert_view(view: AdhocHighlightDialogView, current_note_type: str, note_types: list[str],
                current_field: str, source_fields: list[str], selected_format: Optional[HighlightFormat],
                formats: list[HighlightFormat], check_box_texts: list[str], selected_fields: list[str],
                disabled_fields: list[str], stop_words: str):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == "Highlight"
    assert_buttons(view)
    assert_source_group_box(view, current_note_type, note_types, current_field, source_fields, stop_words)
    assert_format_group_box(view, selected_format, formats)
    assert_destination_group_box(view, check_box_texts, selected_fields, disabled_fields)


def assert_source_group_box(view: AdhocHighlightDialogView, current_note_type: str, note_types: list[str],
                            current_source_field: str, source_fields: list[str], stop_words: str):
    group_box: PyQtPath = path(view).group(0)

    note_type: PyQtPath = group_box.child(NoteTypeComboBoxLayout)
    assert note_type.label().get().text() == "Note Type"
    note_type_combo_box: QComboBox = note_type.combobox().get()
    assert note_type_combo_box.currentText() == current_note_type
    assert get_items(note_type_combo_box) == note_types

    assert_source_combo_box(view, current_source_field, source_fields)

    act_stop_words: str = group_box.child(TitledLineEditLayout).child(QLineEdit).get().text()
    assert act_stop_words == stop_words, f"'{act_stop_words}' != '{stop_words}'"


def assert_source_combo_box(view: AdhocHighlightDialogView, current_source_field: str, source_fields: list[str]):
    group_box: PyQtPath = path(view).group(0)
    field_path: PyQtPath = group_box.child(TitledComboBoxLayout)
    assert field_path.label().get().text() == "Field"
    field_combo_box: QComboBox = field_path.combobox().get()
    assert field_combo_box.currentText() == current_source_field, f"current_source_field: '{current_source_field}' != '{field_combo_box.currentText()}'"
    assert get_items(
        field_combo_box) == source_fields, f"all source fields: '{get_items(field_combo_box)}' != '{source_fields}'"


def assert_format_group_box(view: AdhocHighlightDialogView, current_format: Optional[HighlightFormat],
                            formats: list[HighlightFormat]):
    combo_box: PyQtPath = path(view).group(1).child(TitledComboBoxLayout)
    assert combo_box.label().get().text() == "Format"
    format_combo_box: QComboBox = combo_box.combobox().get()
    assert format_combo_box.currentText() == (current_format.name if current_format else "")
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
    assert start_button.text() == "Start"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    assert cancel_button.text() == "&Cancel"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"
