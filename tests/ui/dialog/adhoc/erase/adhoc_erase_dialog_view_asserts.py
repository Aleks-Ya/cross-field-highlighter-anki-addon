from typing import Optional

from PyQtPath.path_chain_pyqt6 import path
from aqt import QCheckBox, QDialogButtonBox, QPushButton

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel, \
    AdhocEraseDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams


class FakeCallback:
    history: list[EraseOpParams] = []

    @staticmethod
    def call(params: EraseOpParams):
        FakeCallback.history.append(params)


class FakeModelListener(AdhocEraseDialogModelListener):
    history: list[object] = []

    def model_changed(self, source: object):
        FakeModelListener.history.append(source)


def assert_view(view: AdhocEraseDialogView, check_box_texts: list[str], selected_fields: list[str]):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == "Erase"
    assert_buttons(view)
    assert_destination_group_box(view, check_box_texts, selected_fields)


def assert_destination_group_box(view: AdhocEraseDialogView, check_box_texts: list[str], selected_fields: list[str]):
    fields_layout: FieldsLayout = path(view).child(FieldsLayout).get()
    assert path(fields_layout).label().get().text() == "Fields:"
    assert fields_layout.get_selected_field_names() == selected_fields
    check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    texts: list[str] = [check_box.text() for check_box in check_boxes]
    assert texts == check_box_texts


def assert_buttons(view: AdhocEraseDialogView):
    start_button: QPushButton = path(view).child(QDialogButtonBox).button(0).get()
    assert start_button.text() == "Start"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    assert cancel_button.text() == "&Cancel"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"


def assert_model(adhoc_erase_dialog_model: AdhocEraseDialogModel, no_callback: bool,
                 note_types: list[NoteTypeDetails], selected_note_type: Optional[NoteTypeDetails],
                 selected_fields: list[str], model_history: list[object]):
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': note_types,
                                                  'run_op_callback_None': no_callback,
                                                  'selected_fields': selected_fields,
                                                  'selected_note_type': selected_note_type}
    assert FakeModelListener.history == model_history
