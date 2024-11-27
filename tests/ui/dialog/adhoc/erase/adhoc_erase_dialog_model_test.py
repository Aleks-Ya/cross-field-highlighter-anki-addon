from typing import Any

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from tests.conftest import cloze_note_type_details
from tests.data import DefaultFields


def test_serialize_empty_model():
    model1: AdhocEraseDialogModel = AdhocEraseDialogModel()
    data: dict[str, Any] = model1.serialize_states()
    assert data == {'current_state': None, 'states': []}
    model2: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model2.deserialize_states(data)
    assert model1 == model2
    assert model2.as_dict() == {'accept_callback_None': True,
                                'current_state': None,
                                'note_types': [],
                                'reject_callback_None': True,
                                'states': {}}


def test_serialize_model(all_note_type_details: list[NoteTypeDetails], cloze_note_type_details: NoteTypeDetails):
    model1: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model1.fill(all_note_type_details, None, None)
    model1.switch_state(cloze_note_type_details)
    model1.get_current_state().select_fields(FieldNames([DefaultFields.cloze_extra]))
    data: dict[str, Any] = model1.serialize_states()
    assert data == {'current_state': 'Cloze',
                    'states': [{'fields': ['Back Extra'], 'note_type': 'Cloze'}]}
    model2: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model2.fill(all_note_type_details, None, None)
    model2.deserialize_states(data)
    assert model1 == model2
    assert model2.as_dict() == {'accept_callback_None': True,
                                'current_state': {'selected_fields': ['Back Extra'],
                                                  'selected_note_type': cloze_note_type_details},
                                'note_types': all_note_type_details,
                                'reject_callback_None': True,
                                'states': {'Cloze': {'selected_fields': ['Back Extra'],
                                                     'selected_note_type': cloze_note_type_details}}}
