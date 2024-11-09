from typing import Optional

from PyQtPath.path_chain_pyqt6 import path
from aqt import QComboBox, Qt, QCheckBox, QDialogButtonBox, QPushButton

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, FieldName
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel, \
    AdhocEraseDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout
from tests.visual_qtbot import VisualQtBot


class FakeCallback:
    history: list[EraseOpParams] = []

    @staticmethod
    def call(params: EraseOpParams):
        FakeCallback.history.append(params)


class FakeModelListener(AdhocEraseDialogModelListener):
    history: list[object] = []

    def model_changed(self, source: object):
        FakeModelListener.history.append(source)


def test_show_view(adhoc_erase_dialog_view: AdhocEraseDialogView,
              adhoc_erase_dialog_model: AdhocEraseDialogModel, basic_note_type_details: NoteTypeDetails,
              cloze_note_type_details: NoteTypeDetails, visual_qtbot: VisualQtBot):
    # noinspection PyUnresolvedReferences
    adhoc_erase_dialog_view.show()
    visual_qtbot.waitExposed(adhoc_erase_dialog_view)
    adhoc_erase_dialog_model.add_listener(FakeModelListener())
    # Initial state
    __assert_view(adhoc_erase_dialog_view, check_box_texts=[], selected_fields=[])
    __assert_model(adhoc_erase_dialog_model, no_callback=True, note_types=[], selected_note_type=None,
                   selected_fields=[], model_history=[])
    # Fill model without firing
    adhoc_erase_dialog_model.note_types = [basic_note_type_details, cloze_note_type_details]
    adhoc_erase_dialog_model.run_op_callback = FakeCallback.call
    __assert_view(adhoc_erase_dialog_view, check_box_texts=[], selected_fields=[])
    __assert_model(adhoc_erase_dialog_model, no_callback=False,
                   note_types=[basic_note_type_details, cloze_note_type_details],
                   selected_note_type=None, selected_fields=[], model_history=[])
    # Fire model changes
    adhoc_erase_dialog_view.show_view()
    __assert_view(adhoc_erase_dialog_view, check_box_texts=['Front', 'Back', 'Extra'], selected_fields=[])
    __assert_model(adhoc_erase_dialog_model, no_callback=False,
                   note_types=[basic_note_type_details, cloze_note_type_details],
                   selected_note_type=None, selected_fields=[], model_history=[adhoc_erase_dialog_view])
    # Choose Note Type
    note_type_combo_box: QComboBox = path(adhoc_erase_dialog_view).child(TitledComboBoxLayout).combobox().get()
    visual_qtbot.mouseClick(note_type_combo_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(note_type_combo_box, Qt.Key.Key_Down)
    visual_qtbot.keyClick(note_type_combo_box.view(), Qt.Key.Key_Enter)
    __assert_view(adhoc_erase_dialog_view, check_box_texts=['Text', 'Back Extra'], selected_fields=[])
    __assert_model(adhoc_erase_dialog_model, no_callback=False,
                   note_types=[basic_note_type_details, cloze_note_type_details],
                   selected_note_type=None, selected_fields=[], model_history=[adhoc_erase_dialog_view])
    # Click Start button
    assert FakeCallback.history == []
    check_box: QCheckBox = path(adhoc_erase_dialog_view).child(FieldsLayout).checkbox().get()
    visual_qtbot.mouseClick(check_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(check_box, Qt.Key.Key_Space)  # Mouse click just focus on check_box, but doesn't select it
    button_box: QDialogButtonBox = path(adhoc_erase_dialog_view).child(QDialogButtonBox).get()
    start_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
    visual_qtbot.mouseClick(start_button, Qt.MouseButton.LeftButton)
    start_params: EraseOpParams = EraseOpParams(note_type_id=cloze_note_type_details.note_type_id, parent=None,
                                                fields=FieldNames([FieldName('Text')]))
    assert FakeCallback.history == [start_params]
    __assert_model(adhoc_erase_dialog_model, no_callback=False,
                   note_types=[basic_note_type_details, cloze_note_type_details],
                   selected_note_type=cloze_note_type_details, selected_fields=['Text'],
                   model_history=[adhoc_erase_dialog_view, adhoc_erase_dialog_view])
    # Click Cancel button
    cancel_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Cancel)
    visual_qtbot.mouseClick(cancel_button, Qt.MouseButton.LeftButton)
    assert FakeCallback.history == [start_params]
    __assert_model(adhoc_erase_dialog_model, no_callback=False,
                   note_types=[basic_note_type_details, cloze_note_type_details],
                   selected_note_type=cloze_note_type_details, selected_fields=['Text'],
                   model_history=[adhoc_erase_dialog_view, adhoc_erase_dialog_view, adhoc_erase_dialog_view])
    # Click Reset Defaults button
    restore_defaults_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
    visual_qtbot.mouseClick(restore_defaults_button, Qt.MouseButton.LeftButton)
    assert FakeCallback.history == [start_params]
    __assert_model(adhoc_erase_dialog_model, no_callback=False,
                   note_types=[basic_note_type_details, cloze_note_type_details],
                   selected_note_type=None, selected_fields=[],
                   model_history=[adhoc_erase_dialog_view, adhoc_erase_dialog_view, adhoc_erase_dialog_view, None])


def __assert_view(view: AdhocEraseDialogView, check_box_texts: list[str], selected_fields: list[str]):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == "Erase"
    __assert_buttons(view)
    __assert_destination_group_box(view, check_box_texts, selected_fields)


def __assert_destination_group_box(view: AdhocEraseDialogView, check_box_texts: list[str], selected_fields: list[str]):
    fields_layout: FieldsLayout = path(view).child(FieldsLayout).get()
    assert path(fields_layout).label().get().text() == "Fields:"
    assert fields_layout.get_selected_field_names() == selected_fields
    check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    texts: list[str] = [check_box.text() for check_box in check_boxes]
    assert texts == check_box_texts


def __assert_buttons(view: AdhocEraseDialogView):
    start_button: QPushButton = path(view).child(QDialogButtonBox).button(0).get()
    assert start_button.text() == "Start"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    assert cancel_button.text() == "&Cancel"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"


def __assert_model(adhoc_erase_dialog_model: AdhocEraseDialogModel, no_callback: bool,
                   note_types: list[NoteTypeDetails], selected_note_type: Optional[NoteTypeDetails],
                   selected_fields: list[str], model_history: list[object]):
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': note_types,
                                                  'run_op_callback_None': no_callback,
                                                  'selected_fields': selected_fields,
                                                  'selected_note_type': selected_note_type}
    assert FakeModelListener.history == model_history


def test_repr(adhoc_erase_dialog_view: AdhocEraseDialogView):
    assert repr(adhoc_erase_dialog_view) == "AdhocEraseDialogView"
