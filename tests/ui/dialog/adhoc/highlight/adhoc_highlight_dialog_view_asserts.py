from typing import Optional

from PyQtPath.path_chain_pyqt6 import path, PyQtPath
from aqt import QComboBox, QCheckBox, QDialogButtonBox, QPushButton

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, \
    HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldName, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel, \
    AdhocHighlightDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout, TitledLineEditLayout
from tests.qtget import get_items


class FakeCallback:
    history: list[HighlightOpParams] = []

    @staticmethod
    def call(params: HighlightOpParams):
        FakeCallback.history.append(params)


class FakeModelListener(AdhocHighlightDialogModelListener):
    history: list[object] = []

    def model_changed(self, source: object):
        FakeModelListener.history.append(source)


def assert_view(view: AdhocHighlightDialogView, current_note_type: str, note_types: list[str],
                current_field: str, source_fields: list[str], selected_format: Optional[HighlightFormat],
                formats: list[HighlightFormat], check_box_texts: list[str], selected_fields: list[str],
                disabled_field: str):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == "Highlight"
    assert_buttons(view)
    assert_source_group_box(view, current_note_type, note_types, current_field, source_fields, "a an to")
    assert_format_group_box(view, selected_format, formats)
    assert_destination_group_box(view, check_box_texts, selected_fields, disabled_field)


def assert_source_group_box(view: AdhocHighlightDialogView, current_note_type: str, note_types: list[str],
                            current_source_field: str, source_fields: list[str], stop_words: str):
    group_box: PyQtPath = path(view).group(0)

    note_type: PyQtPath = group_box.child(TitledComboBoxLayout, 0)
    assert note_type.label().get().text() == "Note Type"
    note_type_combo_box: QComboBox = note_type.combobox().get()
    assert note_type_combo_box.currentText() == current_note_type
    assert get_items(note_type_combo_box) == note_types

    assert_source_combo_box(view, current_source_field, source_fields)

    assert group_box.child(TitledLineEditLayout).get().get_text() == stop_words


def assert_source_combo_box(view: AdhocHighlightDialogView, current_source_field: str, source_fields: list[str]):
    group_box: PyQtPath = path(view).group(0)
    field_path: PyQtPath = group_box.child(TitledComboBoxLayout, 1)
    assert field_path.label().get().text() == "Field"
    field_combo_box: QComboBox = field_path.combobox().get()
    assert field_combo_box.currentText() == current_source_field
    assert get_items(field_combo_box) == source_fields


def assert_format_group_box(view: AdhocHighlightDialogView, current_format: Optional[HighlightFormat],
                            formats: list[HighlightFormat]):
    combo_box: PyQtPath = path(view).group(1).child(TitledComboBoxLayout)
    assert combo_box.label().get().text() == "Format"
    format_combo_box: QComboBox = combo_box.combobox().get()
    assert format_combo_box.currentText() == (current_format.name if current_format else "")
    format_names: list[str] = [highlight_format.name for highlight_format in formats]
    assert get_items(format_combo_box) == format_names


def assert_destination_group_box(view: AdhocHighlightDialogView, check_box_texts: list[str],
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


def assert_buttons(view: AdhocHighlightDialogView):
    start_button: QPushButton = path(view).child(QDialogButtonBox).button(0).get()
    assert start_button.text() == "Start"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    assert cancel_button.text() == "&Cancel"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"


def assert_model(adhoc_highlight_dialog_model: AdhocHighlightDialogModel, no_callback: bool,
                 note_types: list[NoteTypeDetails], formats: HighlightFormats,
                 destination_fields: list[str], disabled_destination_fields: list[str],
                 selected_note_type: Optional[NoteTypeDetails], selected_format: Optional[HighlightFormat],
                 selected_source_field: dict[NoteTypeName, FieldName], selected_stop_words: Optional[str],
                 selected_destination_fields: list[str], model_history_counter: int):
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an',
        'destination_fields': destination_fields,
        'disabled_destination_fields': disabled_destination_fields,
        'formats': formats,
        'note_ids': set(),
        'note_types': note_types,
        'run_op_callback_None': no_callback,
        'selected_destination_fields': selected_destination_fields,
        'selected_format': selected_format,
        'selected_note_type': selected_note_type,
        'selected_source_field': selected_source_field,
        'selected_stop_words': selected_stop_words}
    assert len(FakeModelListener.history) == model_history_counter
