from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from tests.data import DefaultFields
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_asserts import FakeModelListener, FakeCallback, assert_view
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
    assert listener.history == []
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None,
                                                  'current_state': None,
                                                  'states': {}}
    # Fill model without firing
    adhoc_erase_dialog_model.note_types = all_note_type_details
    adhoc_erase_dialog_model.accept_callback = callback.call
    assert_view(adhoc_erase_dialog_view, check_box_texts=[], selected_fields=[])
    assert listener.history == []
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None,
                                                  'current_state': None,
                                                  'states': {}}
    # Fire model changes
    adhoc_erase_dialog_view.show_view()
    assert_view(adhoc_erase_dialog_view, check_box_texts=DefaultFields.all_basic, selected_fields=[])
    assert listener.history == [adhoc_erase_dialog_view]
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None,
                                                  'current_state': None,
                                                  'states': {}}
    # Choose Note Type
    adhoc_erase_dialog_view_scaffold.select_2nd_note_type()
    assert_view(adhoc_erase_dialog_view, check_box_texts=DefaultFields.all_cloze, selected_fields=[])
    assert listener.history == [adhoc_erase_dialog_view]
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None,
                                                  'current_state': None,
                                                  'states': {}}
    # Click Start button
    assert callback.counter == 0
    adhoc_erase_dialog_view_scaffold.mark_destination_field()
    adhoc_erase_dialog_view_scaffold.click_start_button()
    assert callback.counter == 1
    assert listener.history == [adhoc_erase_dialog_view, adhoc_erase_dialog_view]
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': True,
                                                  'selected_fields': [DefaultFields.cloze_text],
                                                  'selected_note_type': cloze_note_type_details,
                                                  'current_state': None,
                                                  'states': {}}
    # Click Cancel button
    adhoc_erase_dialog_view_scaffold.click_cancel_button()
    assert callback.counter == 1
    assert listener.history == [adhoc_erase_dialog_view, adhoc_erase_dialog_view, adhoc_erase_dialog_view]
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': True,
                                                  'selected_fields': [DefaultFields.cloze_text],
                                                  'selected_note_type': cloze_note_type_details,
                                                  'current_state': None,
                                                  'states': {}}
    # Click Reset Defaults button
    adhoc_erase_dialog_view_scaffold.click_restore_defaults_button()
    assert callback.counter == 1
    assert listener.history == [adhoc_erase_dialog_view, adhoc_erase_dialog_view, adhoc_erase_dialog_view, None]
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None,
                                                  'current_state': None,
                                                  'states': {}}


def test_repr(adhoc_erase_dialog_view: AdhocEraseDialogView):
    assert repr(adhoc_erase_dialog_view) == "AdhocEraseDialogView"
