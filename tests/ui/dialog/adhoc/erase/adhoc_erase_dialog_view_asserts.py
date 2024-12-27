from typing import Optional

from PyQt6.QtWidgets import QComboBox
from PyQtPath.path_chain_pyqt6 import path
from aqt import QCheckBox, QDialogButtonBox, QPushButton

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from cross_field_highlighter.ui.widgets.note_type_combo_box_layout import NoteTypeComboBoxLayout


class FakeCallback:
    def __init__(self):
        self.counter: int = 0

    def call(self):
        self.counter += 1


class FakeModelListener(AdhocEraseDialogModelListener):
    def __init__(self):
        self.history: list[object] = []

    def model_changed(self, source: object):
        self.history.append(source)


class FakeEraseControllerCallback:
    def __init__(self):
        self.history: list[EraseOpParams] = []

    def call(self, params: EraseOpParams):
        self.history.append(params)


def assert_view(view: AdhocEraseDialogView, window_title: str, selected_note_type: Optional[NoteTypeDetails],
                all_fields: list[str], selected_fields: list[str]):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == window_title, f"'{view.windowTitle()}' != '{window_title}'"
    assert_buttons(view)
    assert_destination_group_box(view, selected_note_type, all_fields, selected_fields)


def assert_destination_group_box(view: AdhocEraseDialogView, selected_note_type: NoteTypeDetails,
                                 all_fields: list[str], selected_fields: list[str]):
    fields_layout: FieldsLayout = path(view).child(FieldsLayout).get()
    note_type: QComboBox = path(view).child(NoteTypeComboBoxLayout).combobox().get()
    exp_selected_note_type_name: str = selected_note_type.name if selected_note_type else ""
    act_selected_note_type_name: str = note_type.currentText()
    assert act_selected_note_type_name == exp_selected_note_type_name, f"'{act_selected_note_type_name}' != '{exp_selected_note_type_name}'"
    act_note_type_data: NoteTypeDetails = note_type.currentData()
    assert act_note_type_data == selected_note_type, f"'{act_note_type_data}' != '{selected_note_type}'"
    assert path(fields_layout).label().get().text() == "Fields:"
    check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    act_all_fields: list[str] = [check_box.text() for check_box in check_boxes]
    assert act_all_fields == all_fields, f"'{act_all_fields}' != '{all_fields}'"
    act_selected_fields: list[str] = [check_box.text() for check_box in check_boxes if check_box.isChecked()]
    assert act_selected_fields == selected_fields, f"selected_fields: '{act_selected_fields}' != '{selected_fields}'"


def assert_buttons(view: AdhocEraseDialogView):
    start_button: QPushButton = path(view).child(QDialogButtonBox).button(0).get()
    assert start_button.text() == "&Start"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    act_cancel_button_text: str = cancel_button.text()
    exp_cancel_button_text: str = "&Cancel"
    assert act_cancel_button_text == exp_cancel_button_text, f"'{act_cancel_button_text}' != '{exp_cancel_button_text}'"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"
