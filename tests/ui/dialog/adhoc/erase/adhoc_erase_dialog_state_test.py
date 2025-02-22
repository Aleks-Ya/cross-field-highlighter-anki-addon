from typing import Optional

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_state import AdhocEraseDialogState
from tests.data import DefaultFields


def test_as_dict_empty(note_type_details_basic: NoteTypeDetails):
    state: AdhocEraseDialogState = AdhocEraseDialogState(note_type_details_basic)
    assert state.as_dict() == {
        'selected_note_type': note_type_details_basic,
        'selected_fields': []}


def test_as_dict_full(note_type_details_basic: NoteTypeDetails):
    state: AdhocEraseDialogState = AdhocEraseDialogState(note_type_details_basic)
    state.select_fields(FieldNames(DefaultFields.all_basic))
    assert state.as_dict() == {
        'selected_note_type': note_type_details_basic,
        'selected_fields': DefaultFields.all_basic}


def test_eq_empty(note_type_details_basic: NoteTypeDetails):
    state1: AdhocEraseDialogState = AdhocEraseDialogState(note_type_details_basic)
    state2: AdhocEraseDialogState = AdhocEraseDialogState(note_type_details_basic)
    assert state1 == state2


def test_eq_none(note_type_details_basic: NoteTypeDetails):
    state1: AdhocEraseDialogState = AdhocEraseDialogState(note_type_details_basic)
    state2: Optional[AdhocEraseDialogState] = None
    assert state1 != state2


def test_eq_full(note_type_details_basic: NoteTypeDetails, bold_format: HighlightFormat):
    state1: AdhocEraseDialogState = AdhocEraseDialogState(note_type_details_basic)
    state1.select_fields(FieldNames(DefaultFields.all_basic))

    state2: AdhocEraseDialogState = AdhocEraseDialogState(note_type_details_basic)
    state2.select_fields(FieldNames(DefaultFields.all_basic))

    assert state1 == state2
