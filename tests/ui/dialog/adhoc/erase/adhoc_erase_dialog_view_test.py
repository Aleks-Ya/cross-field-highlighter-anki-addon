from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, FieldName
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_asserts import FakeModelListener, FakeCallback, assert_model, \
    assert_view
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_scaffold import AdhocEraseDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


def test_show_view(adhoc_erase_dialog_view: AdhocEraseDialogView, adhoc_erase_dialog_model: AdhocEraseDialogModel,
                   cloze_note_type_details: NoteTypeDetails, all_note_type_details: list[NoteTypeDetails],
                   adhoc_erase_dialog_view_scaffold: AdhocEraseDialogViewScaffold,
                   visual_qtbot: VisualQtBot):
    callback: FakeCallback = FakeCallback()
    listener: FakeModelListener = FakeModelListener()
    # noinspection PyUnresolvedReferences
    adhoc_erase_dialog_view.show()
    visual_qtbot.waitExposed(adhoc_erase_dialog_view)
    adhoc_erase_dialog_model.add_listener(listener)
    # Initial state
    assert_view(adhoc_erase_dialog_view, check_box_texts=[], selected_fields=[])
    assert_model(adhoc_erase_dialog_model, listener, no_accept_callback=True, note_types=[], selected_note_type=None,
                 selected_fields=[], model_history=[])
    # Fill model without firing
    adhoc_erase_dialog_model.note_types = all_note_type_details
    adhoc_erase_dialog_model.accept_callback = callback.call
    assert_view(adhoc_erase_dialog_view, check_box_texts=[], selected_fields=[])
    assert_model(adhoc_erase_dialog_model, listener, no_accept_callback=False,
                 note_types=all_note_type_details,
                 selected_note_type=None, selected_fields=[], model_history=[])
    # Fire model changes
    adhoc_erase_dialog_view.show_view()
    assert_view(adhoc_erase_dialog_view, check_box_texts=['Front', 'Back', 'Extra'], selected_fields=[])
    assert_model(adhoc_erase_dialog_model, listener, no_accept_callback=False,
                 note_types=all_note_type_details,
                 selected_note_type=None, selected_fields=[], model_history=[adhoc_erase_dialog_view])
    # Choose Note Type
    adhoc_erase_dialog_view_scaffold.select_2nd_note_type()
    assert_view(adhoc_erase_dialog_view, check_box_texts=['Text', 'Back Extra'], selected_fields=[])
    assert_model(adhoc_erase_dialog_model, listener, no_accept_callback=False,
                 note_types=all_note_type_details,
                 selected_note_type=None, selected_fields=[], model_history=[adhoc_erase_dialog_view])
    # Click Start button
    assert callback.counter == 0
    adhoc_erase_dialog_view_scaffold.mark_destination_field()
    adhoc_erase_dialog_view_scaffold.click_start_button()
    start_params: EraseOpParams = EraseOpParams(note_type_id=cloze_note_type_details.note_type_id, parent=None,
                                                fields=FieldNames([FieldName('Text')]))
    assert callback.counter == 1
    assert_model(adhoc_erase_dialog_model, listener, no_accept_callback=False,
                 note_types=all_note_type_details,
                 selected_note_type=cloze_note_type_details, selected_fields=['Text'],
                 model_history=[adhoc_erase_dialog_view, adhoc_erase_dialog_view])
    # Click Cancel button
    adhoc_erase_dialog_view_scaffold.click_cancel_button()
    assert callback.counter == 1
    assert_model(adhoc_erase_dialog_model, listener, no_accept_callback=False,
                 note_types=all_note_type_details,
                 selected_note_type=cloze_note_type_details, selected_fields=['Text'],
                 model_history=[adhoc_erase_dialog_view, adhoc_erase_dialog_view, adhoc_erase_dialog_view])
    # Click Reset Defaults button
    adhoc_erase_dialog_view_scaffold.click_restore_defaults_button()
    assert callback.counter == 1
    assert_model(adhoc_erase_dialog_model, listener, no_accept_callback=False,
                 note_types=all_note_type_details,
                 selected_note_type=None, selected_fields=[],
                 model_history=[adhoc_erase_dialog_view, adhoc_erase_dialog_view, adhoc_erase_dialog_view, None])


def test_repr(adhoc_erase_dialog_view: AdhocEraseDialogView):
    assert repr(adhoc_erase_dialog_view) == "AdhocEraseDialogView"
