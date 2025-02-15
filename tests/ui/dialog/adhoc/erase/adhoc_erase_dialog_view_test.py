from aqt import Qt

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from tests.conftest import basic_note_type_details
from tests.data import DefaultFields
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_asserts import FakeModelListener, FakeCallback, assert_view
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_scaffold import AdhocEraseDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


def test_show_view(adhoc_erase_dialog_view: AdhocEraseDialogView, adhoc_erase_dialog_model: AdhocEraseDialogModel,
                   basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails,
                   all_note_type_details: list[NoteTypeDetails],
                   adhoc_erase_dialog_view_scaffold: AdhocEraseDialogViewScaffold, visual_qtbot: VisualQtBot):
    callback: FakeCallback = FakeCallback()
    listener: FakeModelListener = FakeModelListener()
    adhoc_erase_dialog_model.add_listener(listener)
    # noinspection PyUnresolvedReferences
    adhoc_erase_dialog_view.show()
    visual_qtbot.wait_exposed(adhoc_erase_dialog_view)
    # Initial state
    assert_view(adhoc_erase_dialog_view, window_title="", selected_note_type=None, all_fields=[],
                selected_fields=[])
    assert len(listener.history) == 0
    assert adhoc_erase_dialog_model.as_dict() == {'selected_note_types': [],
                                                  'note_number': 0,
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}
    # Fill model without firing
    adhoc_erase_dialog_model.fill(all_note_type_details, 3, callback.call, None)
    assert_view(adhoc_erase_dialog_view, window_title="", selected_note_type=None, all_fields=[],
                selected_fields=[])
    assert len(listener.history) == 0
    assert adhoc_erase_dialog_model.as_dict() == {'selected_note_types': all_note_type_details,
                                                  'note_number': 3,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}
    # Fire model changes
    adhoc_erase_dialog_view.show_view()
    assert_view(adhoc_erase_dialog_view, window_title="Erase 3 notes", selected_note_type=basic_note_type_details,
                all_fields=DefaultFields.all_basic, selected_fields=[])
    assert len(listener.history) == 1
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [],
                          'selected_note_type': basic_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details}}}
    # Choose Note Type
    adhoc_erase_dialog_view_scaffold.select_note_type(Qt.Key.Key_Down)
    assert_view(adhoc_erase_dialog_view, window_title="Erase 3 notes", selected_note_type=cloze_note_type_details,
                all_fields=DefaultFields.all_cloze, selected_fields=[])
    assert len(listener.history) == 2
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [],
                          'selected_note_type': cloze_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details},
                   cloze_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': cloze_note_type_details}}}
    # Click Start button
    assert callback.counter == 0
    # adhoc_erase_dialog_view_scaffold.mark_destination_field()
    adhoc_erase_dialog_view_scaffold.mark_destination_field(DefaultFields.cloze_text)
    adhoc_erase_dialog_view_scaffold.click_start_button()
    assert callback.counter == 1
    assert len(listener.history) == 3
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [DefaultFields.cloze_text],
                          'selected_note_type': cloze_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details},
                   cloze_note_type_details.name: {'selected_fields': [DefaultFields.cloze_text],
                                                  'selected_note_type': cloze_note_type_details}}}
    # Click Cancel button
    adhoc_erase_dialog_view_scaffold.click_cancel_button()
    assert callback.counter == 1
    assert len(listener.history) == 3
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [DefaultFields.cloze_text],
                          'selected_note_type': cloze_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details},
                   cloze_note_type_details.name: {'selected_fields': [DefaultFields.cloze_text],
                                                  'selected_note_type': cloze_note_type_details}}}
    # Click Reset Defaults button
    adhoc_erase_dialog_view_scaffold.click_restore_defaults_button()
    assert callback.counter == 1
    assert len(listener.history) == 4
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [],
                          'selected_note_type': basic_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details},
                   cloze_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': cloze_note_type_details}}}


def test_remember_selected_fields_when_changing_note_type(
        adhoc_erase_dialog_view: AdhocEraseDialogView, adhoc_erase_dialog_model: AdhocEraseDialogModel,
        basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails,
        all_note_type_details: list[NoteTypeDetails], adhoc_erase_dialog_view_scaffold: AdhocEraseDialogViewScaffold,
        visual_qtbot: VisualQtBot):
    callback: FakeCallback = FakeCallback()
    listener: FakeModelListener = FakeModelListener()
    adhoc_erase_dialog_model.add_listener(listener)
    # noinspection PyUnresolvedReferences
    adhoc_erase_dialog_view.show()
    visual_qtbot.wait_exposed(adhoc_erase_dialog_view)
    # Initial state
    adhoc_erase_dialog_model.fill(all_note_type_details, 3, callback.call, None)
    adhoc_erase_dialog_view.show_view()
    assert_view(adhoc_erase_dialog_view, window_title="Erase 3 notes", selected_note_type=basic_note_type_details,
                all_fields=DefaultFields.all_basic, selected_fields=[])
    assert len(listener.history) == 1
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [],
                          'selected_note_type': basic_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details}}}

    # Choose fields for basic
    adhoc_erase_dialog_view_scaffold.mark_destination_field(DefaultFields.basic_front)
    adhoc_erase_dialog_view_scaffold.mark_destination_field(DefaultFields.basic_back)
    assert_view(adhoc_erase_dialog_view, window_title="Erase 3 notes", selected_note_type=basic_note_type_details,
                all_fields=DefaultFields.all_basic,
                selected_fields=[DefaultFields.basic_front, DefaultFields.basic_back])
    assert len(listener.history) == 3
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [DefaultFields.basic_front, DefaultFields.basic_back],
                          'selected_note_type': basic_note_type_details},
        'states': {basic_note_type_details.name: {
            'selected_fields': [DefaultFields.basic_front, DefaultFields.basic_back],
            'selected_note_type': basic_note_type_details}}}

    # Choose Note Type: cloze
    adhoc_erase_dialog_view_scaffold.select_note_type(Qt.Key.Key_Down)
    assert_view(adhoc_erase_dialog_view, window_title="Erase 3 notes", selected_note_type=cloze_note_type_details,
                all_fields=DefaultFields.all_cloze, selected_fields=[])
    assert len(listener.history) == 4
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [],
                          'selected_note_type': cloze_note_type_details},
        'states': {basic_note_type_details.name: {
            'selected_fields': [DefaultFields.basic_front, DefaultFields.basic_back],
            'selected_note_type': basic_note_type_details},
            cloze_note_type_details.name: {'selected_fields': [],
                                           'selected_note_type': cloze_note_type_details}}}

    # Choose field for cloze
    adhoc_erase_dialog_view_scaffold.mark_destination_field(DefaultFields.cloze_text)
    assert_view(adhoc_erase_dialog_view, window_title="Erase 3 notes", selected_note_type=cloze_note_type_details,
                all_fields=DefaultFields.all_cloze, selected_fields=[DefaultFields.cloze_text])
    assert len(listener.history) == 5
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [DefaultFields.cloze_text],
                          'selected_note_type': cloze_note_type_details},
        'states': {basic_note_type_details.name: {
            'selected_fields': [DefaultFields.basic_front, DefaultFields.basic_back],
            'selected_note_type': basic_note_type_details},
            cloze_note_type_details.name: {'selected_fields': [DefaultFields.cloze_text],
                                           'selected_note_type': cloze_note_type_details}}}

    # Choose Note Type: basic
    adhoc_erase_dialog_view_scaffold.select_note_type(Qt.Key.Key_Up)
    assert_view(adhoc_erase_dialog_view, window_title="Erase 3 notes", selected_note_type=basic_note_type_details,
                all_fields=DefaultFields.all_basic,
                selected_fields=[DefaultFields.basic_front, DefaultFields.basic_back])
    assert len(listener.history) == 6
    assert adhoc_erase_dialog_model.as_dict() == {
        'selected_note_types': all_note_type_details,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [DefaultFields.basic_front, DefaultFields.basic_back],
                          'selected_note_type': basic_note_type_details},
        'states': {basic_note_type_details.name: {
            'selected_fields': [DefaultFields.basic_front, DefaultFields.basic_back],
            'selected_note_type': basic_note_type_details},
            cloze_note_type_details.name: {'selected_fields': [DefaultFields.cloze_text],
                                           'selected_note_type': cloze_note_type_details}}}


def test_repr(adhoc_erase_dialog_view: AdhocEraseDialogView):
    assert repr(adhoc_erase_dialog_view) == "AdhocEraseDialogView"
