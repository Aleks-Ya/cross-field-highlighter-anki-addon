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
    model.fill(note_type_details_all, 3, lambda: None, lambda: None)
    data: dict[str, any] = {'current_state': note_type_details_cloze.name,
                            'states': [{'note_type': note_type_details_cloze.name}]}
    adhoc_erase_dialog_model_serde.deserialize_states(model, data)
    assert model.as_dict() == {'accept_callback_None': False,
                               'current_state': {'selected_fields': [],
                                                 'selected_note_type': note_type_details_cloze},
                               'selected_note_types': note_type_details_all,
                               'note_number': 3,
                               'reject_callback_None': False,
                               'states': {note_type_details_cloze.name:
                                              {'selected_fields': [],
                                               'selected_note_type': note_type_details_cloze}}}


def test_serialize_model(note_type_details_all: list[NoteTypeDetails], note_type_details_cloze: NoteTypeDetails,
                         adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    model1: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model1.fill(note_type_details_all, 3, None, None)
    model1.switch_state(note_type_details_cloze)
    model1.get_current_state().select_fields(FieldNames([DefaultFields.cloze_back_extra]))
    data: dict[str, any] = adhoc_erase_dialog_model_serde.serialize_states(model1)
    assert data == {'current_state': note_type_details_cloze.name,
                    'states': [{'fields': [DefaultFields.cloze_back_extra], 'note_type': note_type_details_cloze.name}]}
    model2: AdhocEraseDialogModel = AdhocEraseDialogModel()
    model2.fill(note_type_details_all, 3, None, None)
    adhoc_erase_dialog_model_serde.deserialize_states(model2, data)
    assert model1 == model2
    assert model2.as_dict() == {'accept_callback_None': True,
                                'current_state': {'selected_fields': [DefaultFields.cloze_back_extra],
                                                  'selected_note_type': note_type_details_cloze},
                                'selected_note_types': note_type_details_all,
                                'note_number': 3,
                                'reject_callback_None': True,
                                'states': {note_type_details_cloze.name:
                                               {'selected_fields': [DefaultFields.cloze_back_extra],
                                                'selected_note_type': note_type_details_cloze}}}
