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
    data: dict[str, any] = {'current_state': cloze_note_type_details.name,
                            'states': [{'note_type': cloze_note_type_details.name}]}
    adhoc_highlight_dialog_model_serde.deserialize_states(model, data)
    assert model.as_dict() == {'accept_callback_None': False,
                               'current_state': {'selected_destination_fields': [],
                                                 'selected_format': bold_format,
                                                 'selected_note_type': cloze_note_type_details,
                                                 'selected_source_field': DefaultFields.cloze_text,
                                                 'selected_stop_words': None},
                               'default_stop_words': None,
                               'note_number': 3,
                               'formats': all_highlight_formats,
                               'selected_note_types': all_note_type_details,
                               'reject_callback_None': False,
                               'states': {cloze_note_type_details.name:
                                              {'selected_destination_fields': [],
                                               'selected_format': bold_format,
                                               'selected_note_type': cloze_note_type_details,
                                               'selected_source_field': DefaultFields.cloze_text,
                                               'selected_stop_words': None}}}


def test_serialize_model(all_note_type_details: list[NoteTypeDetails], basic_note_type_details: NoteTypeDetails,
                         cloze_note_type_details: NoteTypeDetails, all_highlight_formats: HighlightFormats,
                         italic_format: HighlightFormat, mark_format: HighlightFormat,
                         adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe):
    # Save state
    model1: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model1.fill(all_note_type_details, 3, all_highlight_formats, lambda: None, lambda: None)
    model1.switch_state(cloze_note_type_details)
    model1.get_current_state().select_source_field(DefaultFields.cloze_back_extra)
    model1.get_current_state().select_format(mark_format)
    model1.get_current_state().select_destination_fields(FieldNames([DefaultFields.cloze_text]))
    model1.get_current_state().set_stop_words(Text("the"))

    # Create new model differ with all parameters
    model2: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model2.fill(all_note_type_details, 3, all_highlight_formats, lambda: None, lambda: None)
    model2.switch_state(basic_note_type_details)
    model2.get_current_state().select_source_field(DefaultFields.basic_back)
    model2.get_current_state().select_format(italic_format)
    model2.get_current_state().select_destination_fields(FieldNames([DefaultFields.basic_front]))
    model2.get_current_state().set_stop_words(Text("to"))

    # Read saved state to the new model
    data: dict[str, any] = adhoc_highlight_dialog_model_serde.serialize_states(model1)
    assert data == {'current_state': cloze_note_type_details.name,
                    'states': [{'destination_fields': [DefaultFields.cloze_text],
                                'format': 'MARK',
                                'note_type': cloze_note_type_details.name,
                                'source_field': DefaultFields.cloze_back_extra,
                                'stop_words': 'the'}]}
    adhoc_highlight_dialog_model_serde.deserialize_states(model2, data)
    assert model1 != model2
    assert model2.as_dict() == {'accept_callback_None': False,
                                'current_state': {
                                    'selected_destination_fields': [DefaultFields.cloze_text],
                                    'selected_format': mark_format,
                                    'selected_note_type': cloze_note_type_details,
                                    'selected_source_field': DefaultFields.cloze_back_extra,
                                    'selected_stop_words': 'the'},
                                'default_stop_words': None,
                                'note_number': 3,
                                'formats': all_highlight_formats,
                                'selected_note_types': all_note_type_details,
                                'reject_callback_None': False,
                                'states': {
                                    basic_note_type_details.name: {
                                        'selected_destination_fields': [DefaultFields.basic_front],
                                        'selected_format': italic_format,
                                        'selected_note_type': basic_note_type_details,
                                        'selected_source_field': DefaultFields.basic_back,
                                        'selected_stop_words': 'to'},
                                    cloze_note_type_details.name: {
                                        'selected_destination_fields': [DefaultFields.cloze_text],
                                        'selected_format': mark_format,
                                        'selected_note_type': cloze_note_type_details,
                                        'selected_source_field': DefaultFields.cloze_back_extra,
                                        'selected_stop_words': 'the'}}}
