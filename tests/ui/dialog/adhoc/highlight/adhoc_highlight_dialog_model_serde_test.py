from typing import Any

from pytest import raises

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormats, HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, Text
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model_serde import \
    AdhocHighlightDialogModelSerDe
from tests.conftest import cloze_note_type_details
from tests.data import DefaultFields


def test_serialize_empty_model(adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe):
    with raises(ValueError, match="At least one note type should exist"):
        model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
        adhoc_highlight_dialog_model_serde.serialize_states(model)


def test_deserialize_empty_state(all_note_type_details: list[NoteTypeDetails], cloze_note_type_details: NoteTypeDetails,
                                 bold_format: HighlightFormat, all_highlight_formats: HighlightFormats,
                                 adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe):
    model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model.fill(all_note_type_details, 3, all_highlight_formats, lambda: None, lambda: None)
    data: dict[str, Any] = {'current_state': 'Cloze', 'states': [{'note_type': 'Cloze'}]}
    adhoc_highlight_dialog_model_serde.deserialize_states(model, data)
    assert model.as_dict() == {'accept_callback_None': False,
                               'current_state': {'selected_destination_fields': [],
                                                 'selected_format': bold_format,
                                                 'selected_note_type': cloze_note_type_details,
                                                 'selected_source_field': 'Text',
                                                 'selected_stop_words': None,
                                                 'space_delimited_language': True},
                               'default_stop_words': None,
                               'note_number': 3,
                               'formats': all_highlight_formats,
                               'note_types': all_note_type_details,
                               'reject_callback_None': False,
                               'states': {'Cloze': {'selected_destination_fields': [],
                                                    'selected_format': bold_format,
                                                    'selected_note_type': cloze_note_type_details,
                                                    'selected_source_field': 'Text',
                                                    'selected_stop_words': None,
                                                    'space_delimited_language': True}}}


def test_serialize_model(all_note_type_details: list[NoteTypeDetails], cloze_note_type_details: NoteTypeDetails,
                         all_highlight_formats: HighlightFormats, mark_format: HighlightFormat,
                         adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe):
    model1: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model1.fill(all_note_type_details, 3, all_highlight_formats, lambda: None, lambda: None)
    model1.switch_state(cloze_note_type_details)
    model1.get_current_state().select_source_field(DefaultFields.cloze_extra)
    model1.get_current_state().select_format(mark_format)
    model1.get_current_state().select_destination_fields(FieldNames([DefaultFields.cloze_text]))
    model1.get_current_state().set_stop_words(Text("the"))

    data: dict[str, Any] = adhoc_highlight_dialog_model_serde.serialize_states(model1)
    assert data == {'current_state': 'Cloze',
                    'states': [{'destination_fields': ['Text'],
                                'format': 'MARK',
                                'note_type': 'Cloze',
                                'source_field': 'Back Extra',
                                'stop_words': 'the',
                                'space_delimited_language': True}]}
    model2: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model2.fill(all_note_type_details, 3, all_highlight_formats, lambda: None, lambda: None)
    model2.switch_state(cloze_note_type_details)
    model2.get_current_state().select_source_field(DefaultFields.cloze_extra)
    model2.get_current_state().select_format(mark_format)
    model2.get_current_state().select_destination_fields(FieldNames([DefaultFields.cloze_text]))
    model2.get_current_state().set_stop_words(Text("the"))

    adhoc_highlight_dialog_model_serde.deserialize_states(model2, data)
    assert model1 == model2
    assert model2.as_dict() == {'accept_callback_None': False,
                                'current_state': {'selected_destination_fields': [DefaultFields.cloze_text],
                                                  'selected_format': mark_format,
                                                  'selected_note_type': cloze_note_type_details,
                                                  'selected_source_field': DefaultFields.cloze_extra,
                                                  'selected_stop_words': 'the',
                                                  'space_delimited_language': True},
                                'default_stop_words': None,
                                'note_number': 3,
                                'formats': all_highlight_formats,
                                'note_types': all_note_type_details,
                                'reject_callback_None': False,
                                'states': {'Cloze': {'selected_destination_fields': [DefaultFields.cloze_text],
                                                     'selected_format': mark_format,
                                                     'selected_note_type': cloze_note_type_details,
                                                     'selected_source_field': DefaultFields.cloze_extra,
                                                     'selected_stop_words': 'the',
                                                     'space_delimited_language': True}}}