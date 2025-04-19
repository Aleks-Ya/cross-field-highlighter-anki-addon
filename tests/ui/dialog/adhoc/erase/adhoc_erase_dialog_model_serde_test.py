from typing import Any

from pytest import raises

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from tests.conftest import note_type_details_cloze
from tests.data import DefaultFields


def test_serialize_empty_model(adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    with raises(ValueError, match="At least one note type should exist"):
        model: AdhocEraseDialogModel = AdhocEraseDialogModel()
        adhoc_erase_dialog_model_serde.serialize_states(model)


def test_deserialize_empty_state(note_type_details_all: list[NoteTypeDetails],
                                 note_type_details_cloze: NoteTypeDetails,
                                 adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model.fill(note_type_details_all, note_type_details_all, 3, lambda: None, lambda: None)
    assert model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': None,
        'states': {}}
    data: dict[str, Any] = {'current_state': note_type_details_cloze.note_type_id,
                            'states': [{'note_type_id': note_type_details_cloze.note_type_id}]}
    adhoc_erase_dialog_model_serde.deserialize_states(model, data)
    assert model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': note_type_details_cloze},
        'states': {note_type_details_cloze.note_type_id:
                       {'selected_fields': [],
                        'selected_note_type': note_type_details_cloze}}}


def test_deserialize_model(note_type_details_all: list[NoteTypeDetails],
                           note_type_details_basic: NoteTypeDetails, note_type_details_cloze: NoteTypeDetails,
                           adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model.fill(note_type_details_all, note_type_details_all, 3, lambda: None, lambda: None)
    assert model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': None,
        'states': {}}
    data: dict[str, Any] = {'current_state': note_type_details_basic.note_type_id,
                            'states': [
                                {
                                    'note_type_id': note_type_details_basic.note_type_id,
                                    'fields': [DefaultFields.basic_front]
                                },
                                {
                                    'note_type_id': note_type_details_cloze.note_type_id,
                                    'fields': [DefaultFields.cloze_back_extra]
                                }]}
    adhoc_erase_dialog_model_serde.deserialize_states(model, data)
    assert model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [DefaultFields.basic_front],
                          'selected_note_type': note_type_details_basic},
        'states': {note_type_details_basic.note_type_id:
                       {'selected_fields': [DefaultFields.basic_front],
                        'selected_note_type': note_type_details_basic},
                   note_type_details_cloze.note_type_id:
                       {'selected_fields': [DefaultFields.cloze_back_extra],
                        'selected_note_type': note_type_details_cloze}}}


# Bug: selected fields are empty after deserialization
def test_deserialize_model_selected_fields_are_empty(
        note_type_details_all: list[NoteTypeDetails], note_type_details_basic: NoteTypeDetails,
        note_type_details_cloze: NoteTypeDetails, adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model.fill(note_type_details_all, [note_type_details_basic], 3, lambda: None, lambda: None)
    assert model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': [note_type_details_basic],
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': None,
        'states': {}}
    data: dict[str, Any] = {'current_state': note_type_details_basic.note_type_id,
                            'states': [
                                {
                                    'note_type_id': note_type_details_basic.note_type_id,
                                    'fields': [DefaultFields.basic_front]
                                },
                                {
                                    'note_type_id': note_type_details_cloze.note_type_id,
                                    'fields': []
                                }]}
    adhoc_erase_dialog_model_serde.deserialize_states(model, data)
    assert model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': [note_type_details_basic],
        'note_number': 3,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [DefaultFields.basic_front],
                          'selected_note_type': note_type_details_basic},
        'states': {note_type_details_basic.note_type_id:
                       {'selected_fields': [DefaultFields.basic_front],
                        'selected_note_type': note_type_details_basic},
                   note_type_details_cloze.note_type_id:
                       {'selected_fields': [],
                        'selected_note_type': note_type_details_cloze}}}


def test_serialize_model(note_type_details_all: list[NoteTypeDetails], note_type_details_cloze: NoteTypeDetails,
                         adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    model1: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model1.fill(note_type_details_all, note_type_details_all, 3, None, None)
    model1.switch_state(note_type_details_cloze.note_type_id)
    model1.get_current_state().select_fields(FieldNames([DefaultFields.cloze_back_extra]))
    assert model1.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 3,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [DefaultFields.cloze_back_extra],
                          'selected_note_type': note_type_details_cloze},
        'states': {note_type_details_cloze.note_type_id:
                       {'selected_fields': [DefaultFields.cloze_back_extra],
                        'selected_note_type': note_type_details_cloze}}}
    data: dict[str, Any] = adhoc_erase_dialog_model_serde.serialize_states(model1)
    assert data == {'current_state': note_type_details_cloze.note_type_id,
                    'states': [{'note_type_id': note_type_details_cloze.note_type_id,
                                'fields': [DefaultFields.cloze_back_extra]}]}
    model2: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model2.fill(note_type_details_all, note_type_details_all, 3, None, None)
    adhoc_erase_dialog_model_serde.deserialize_states(model2, data)
    assert model1 == model2
    assert model2.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 3,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'current_state': {'selected_fields': [DefaultFields.cloze_back_extra],
                          'selected_note_type': note_type_details_cloze},
        'states': {note_type_details_cloze.note_type_id:
                       {'selected_fields': [DefaultFields.cloze_back_extra],
                        'selected_note_type': note_type_details_cloze}}}
