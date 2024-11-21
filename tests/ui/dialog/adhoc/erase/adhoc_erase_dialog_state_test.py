from typing import Optional

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_state import AdhocEraseDialogState
from tests.data import DefaultFields


def test_as_dict_empty():
    state: AdhocEraseDialogState = AdhocEraseDialogState()
    assert state.as_dict() == {
        'selected_note_type': None,
        'selected_fields': []}


def test_as_dict_full(basic_note_type_details: NoteTypeDetails):
    state: AdhocEraseDialogState = AdhocEraseDialogState()
    state.selected_note_type = basic_note_type_details
    state.selected_fields = DefaultFields.all_basic
    assert state.as_dict() == {
        'selected_note_type': basic_note_type_details,
        'selected_fields': DefaultFields.all_basic}


def test_eq_empty():
    state1: AdhocEraseDialogState = AdhocEraseDialogState()
    state2: AdhocEraseDialogState = AdhocEraseDialogState()
    assert state1 == state2


def test_eq_none():
    state1: AdhocEraseDialogState = AdhocEraseDialogState()
    state2: Optional[AdhocEraseDialogState] = None
    assert state1 != state2


def test_eq_full(basic_note_type_details: NoteTypeDetails, bold_format: HighlightFormat):
    state1: AdhocEraseDialogState = AdhocEraseDialogState()
    state1.selected_note_type = basic_note_type_details
    state1.selected_fields = DefaultFields.all_basic

    state2: AdhocEraseDialogState = AdhocEraseDialogState()
    state2.selected_note_type = basic_note_type_details
    state2.selected_fields = DefaultFields.all_basic

    assert state1 == state2
