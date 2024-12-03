from typing import Any

from pytest import raises

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from tests.conftest import cloze_note_type_details
from tests.data import DefaultFields


def test_serialize_empty_model(adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    with raises(ValueError, match="At least one note type should exist"):
        model: AdhocEraseDialogModel = AdhocEraseDialogModel()
        adhoc_erase_dialog_model_serde.serialize_states(model)


def test_deserialize_empty_state(all_note_type_details: list[NoteTypeDetails],
                                 cloze_note_type_details: NoteTypeDetails,
                                 adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model.fill(all_note_type_details, lambda: None, lambda: None)
    data: dict[str, Any] = {'current_state': 'Cloze', 'states': [{'note_type': 'Cloze'}]}
    adhoc_erase_dialog_model_serde.deserialize_states(model, data)
    assert model.as_dict() == {'accept_callback_None': False,
                               'current_state': {'selected_fields': [],
                                                 'selected_note_type': cloze_note_type_details},
                               'note_types': all_note_type_details,
                               'reject_callback_None': False,
                               'states': {'Cloze': {'selected_fields': [],
                                                    'selected_note_type': cloze_note_type_details}}}


def test_serialize_model(all_note_type_details: list[NoteTypeDetails], cloze_note_type_details: NoteTypeDetails,
                         adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    model1: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model1.fill(all_note_type_details, None, None)
    model1.switch_state(cloze_note_type_details)
    model1.get_current_state().select_fields(FieldNames([DefaultFields.cloze_extra]))
    data: dict[str, Any] = adhoc_erase_dialog_model_serde.serialize_states(model1)
    assert data == {'current_state': 'Cloze',
                    'states': [{'fields': [DefaultFields.cloze_extra], 'note_type': 'Cloze'}]}
    model2: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model2.fill(all_note_type_details, None, None)
    adhoc_erase_dialog_model_serde.deserialize_states(model2, data)
    assert model1 == model2
    assert model2.as_dict() == {'accept_callback_None': True,
                                'current_state': {'selected_fields': [DefaultFields.cloze_extra],
                                                  'selected_note_type': cloze_note_type_details},
                                'note_types': all_note_type_details,
                                'reject_callback_None': True,
                                'states': {'Cloze': {'selected_fields': [DefaultFields.cloze_extra],
                                                     'selected_note_type': cloze_note_type_details}}}
