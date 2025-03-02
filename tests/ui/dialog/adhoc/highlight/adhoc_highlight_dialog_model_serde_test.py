from pytest import raises

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormats, HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, Text
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model_serde import \
    AdhocHighlightDialogModelSerDe
from tests.conftest import note_type_details_cloze
from tests.data import DefaultFields, DefaultConfig


def test_serialize_empty_model(adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe):
    with raises(ValueError, match="At least one note type should exist"):
        model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
        adhoc_highlight_dialog_model_serde.serialize_states(model)


def test_deserialize_empty_state(note_type_details_all: list[NoteTypeDetails], note_type_details_cloze: NoteTypeDetails,
                                 bold_format: HighlightFormat, all_highlight_formats: HighlightFormats,
                                 adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe):
    model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model.fill(note_type_details_all, note_type_details_all, 3, all_highlight_formats,
               Text(DefaultConfig.stop_words), lambda: None, lambda: None)
    data: dict[str, any] = {'current_state': note_type_details_cloze.note_type_id,
                            'states': [{'note_type_id': note_type_details_cloze.note_type_id}]}
    adhoc_highlight_dialog_model_serde.deserialize_states(model, data)
    assert model.as_dict() == {'all_note_types': note_type_details_all,
                               'selected_note_types': note_type_details_all,
                               'accept_callback_None': False,
                               'default_stop_words': Text(DefaultConfig.stop_words),
                               'note_number': 3,
                               'formats': all_highlight_formats,
                               'reject_callback_None': False,
                               'current_state': {'selected_destination_fields': [],
                                                 'selected_format': bold_format,
                                                 'selected_note_type': note_type_details_cloze,
                                                 'selected_source_field': DefaultFields.cloze_text,
                                                 'selected_stop_words': Text(DefaultConfig.stop_words)},
                               'states': {note_type_details_cloze.note_type_id:
                                              {'selected_destination_fields': [],
                                               'selected_format': bold_format,
                                               'selected_note_type': note_type_details_cloze,
                                               'selected_source_field': DefaultFields.cloze_text,
                                               'selected_stop_words': Text(DefaultConfig.stop_words)}}}


def test_serialize_model(note_type_details_all: list[NoteTypeDetails], note_type_details_basic: NoteTypeDetails,
                         note_type_details_cloze: NoteTypeDetails, all_highlight_formats: HighlightFormats,
                         italic_format: HighlightFormat, mark_format: HighlightFormat,
                         adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe):
    # Save state
    model1: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model1.fill(note_type_details_all, note_type_details_all, 3, all_highlight_formats,
                Text(DefaultConfig.stop_words), lambda: None, lambda: None)
    model1.switch_state(note_type_details_cloze)
    model1.get_current_state().select_source_field(DefaultFields.cloze_back_extra)
    model1.get_current_state().select_format(mark_format)
    model1.get_current_state().select_destination_fields(FieldNames([DefaultFields.cloze_text]))
    model1.get_current_state().set_stop_words(Text("the"))

    # Create new model differ with all parameters
    model2: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model2.fill(note_type_details_all, note_type_details_all, 3, all_highlight_formats,
                Text(DefaultConfig.stop_words), lambda: None, lambda: None)
    model2.switch_state(note_type_details_basic)
    model2.get_current_state().select_source_field(DefaultFields.basic_back)
    model2.get_current_state().select_format(italic_format)
    model2.get_current_state().select_destination_fields(FieldNames([DefaultFields.basic_front]))
    model2.get_current_state().set_stop_words(Text("to"))

    # Read saved state to the new model
    data: dict[str, any] = adhoc_highlight_dialog_model_serde.serialize_states(model1)
    assert data == {'current_state': note_type_details_cloze.note_type_id,
                    'states': [{'destination_fields': [DefaultFields.cloze_text],
                                'format': 'MARK',
                                'note_type_id': note_type_details_cloze.note_type_id,
                                'source_field': DefaultFields.cloze_back_extra,
                                'stop_words': 'the'}]}
    adhoc_highlight_dialog_model_serde.deserialize_states(model2, data)
    assert model1 != model2
    assert model2.as_dict() == {'all_note_types': note_type_details_all,
                                'selected_note_types': note_type_details_all,
                                'accept_callback_None': False,
                                'default_stop_words': Text(DefaultConfig.stop_words),
                                'note_number': 3,
                                'formats': all_highlight_formats,
                                'reject_callback_None': False,
                                'current_state': {
                                    'selected_destination_fields': [DefaultFields.cloze_text],
                                    'selected_format': mark_format,
                                    'selected_note_type': note_type_details_cloze,
                                    'selected_source_field': DefaultFields.cloze_back_extra,
                                    'selected_stop_words': 'the'},
                                'states': {
                                    note_type_details_basic.note_type_id: {
                                        'selected_destination_fields': [DefaultFields.basic_front],
                                        'selected_format': italic_format,
                                        'selected_note_type': note_type_details_basic,
                                        'selected_source_field': DefaultFields.basic_back,
                                        'selected_stop_words': 'to'},
                                    note_type_details_cloze.note_type_id: {
                                        'selected_destination_fields': [DefaultFields.cloze_text],
                                        'selected_format': mark_format,
                                        'selected_note_type': note_type_details_cloze,
                                        'selected_source_field': DefaultFields.cloze_back_extra,
                                        'selected_stop_words': 'the'}}}
