from typing import Any

from anki.notes import NoteId

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormats, HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, Text
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from tests.conftest import cloze_note_type_details
from tests.data import DefaultFields


def test_serialize_empty_model():
    model1: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    data: dict[str, Any] = model1.serialize_states()
    assert data == {'current_state': None, 'states': []}
    model2: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model2.deserialize_states(data)
    assert model1 == model2
    assert model2.as_dict() == {'accept_callback_None': True,
                                'current_state': None,
                                'default_stop_words': None,
                                'formats': [],
                                'note_ids': [],
                                'note_types': [],
                                'reject_callback_None': True,
                                'states': {}}


def test_serialize_model(all_note_type_details: list[NoteTypeDetails], cloze_note_type_details: NoteTypeDetails,
                         all_highlight_formats: HighlightFormats, mark_format: HighlightFormat):
    model1: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model1.fill(all_note_type_details, [NoteId(1), NoteId(2)], all_highlight_formats, lambda: None, lambda: None)
    model1.switch_state(cloze_note_type_details)
    model1.get_current_state().select_source_field(DefaultFields.cloze_extra)
    model1.get_current_state().select_format(mark_format)
    model1.get_current_state().select_destination_fields(FieldNames([DefaultFields.cloze_text]))
    model1.get_current_state().set_stop_words(Text("the"))

    data: dict[str, Any] = model1.serialize_states()
    assert data == {'current_state': 'Cloze',
                    'states': [{'destination_fields': ['Text'],
                                'format': 'MARK',
                                'note_type': 'Cloze',
                                'source_field': 'Back Extra',
                                'stop_words': 'the'}]}
    model2: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    model2.fill(all_note_type_details, [NoteId(1), NoteId(2)], all_highlight_formats, lambda: None, lambda: None)
    model2.switch_state(cloze_note_type_details)
    model2.get_current_state().select_source_field(DefaultFields.cloze_extra)
    model2.get_current_state().select_format(mark_format)
    model2.get_current_state().select_destination_fields(FieldNames([DefaultFields.cloze_text]))
    model2.get_current_state().set_stop_words(Text("the"))

    model2.deserialize_states(data)
    assert model1 == model2
    assert model2.as_dict() == {'accept_callback_None': False,
                                'current_state': {'selected_destination_fields': [DefaultFields.cloze_text],
                                                  'selected_format': mark_format,
                                                  'selected_note_type': cloze_note_type_details,
                                                  'selected_source_field': DefaultFields.cloze_extra,
                                                  'selected_stop_words': 'the'},
                                'default_stop_words': None,
                                'formats': all_highlight_formats,
                                'note_ids': [1, 2],
                                'note_types': all_note_type_details,
                                'reject_callback_None': False,
                                'states': {'Cloze': {'selected_destination_fields': [DefaultFields.cloze_text],
                                                     'selected_format': mark_format,
                                                     'selected_note_type': cloze_note_type_details,
                                                     'selected_source_field': DefaultFields.cloze_extra,
                                                     'selected_stop_words': 'the'}}}
