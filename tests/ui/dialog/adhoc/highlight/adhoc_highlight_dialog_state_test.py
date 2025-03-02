from typing import Optional

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import Text, FieldNames
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_state import AdhocHighlightDialogState
from tests.data import DefaultFields, DefaultConfig


def test_as_dict_empty(note_type_details_basic: NoteTypeDetails):
    default_stop_words: Optional[str] = DefaultConfig.default_stop_words
    state: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details_basic, default_stop_words)
    assert state.as_dict() == {
        'selected_destination_fields': [],
        'selected_format': None,
        'selected_note_type': note_type_details_basic,
        'selected_source_field': None,
        'selected_stop_words': DefaultConfig.default_stop_words
    }


def test_as_dict_full(note_type_details_basic: NoteTypeDetails, bold_format: HighlightFormat):
    default_stop_words: Optional[str] = DefaultConfig.default_stop_words
    state: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details_basic, default_stop_words)
    state.select_source_field(DefaultFields.basic_front)
    state.select_format(bold_format)
    state.set_stop_words(Text("a an"))
    state.select_destination_fields(FieldNames(DefaultFields.all_basic))
    assert state.as_dict() == {
        'selected_destination_fields': DefaultFields.all_basic,
        'selected_format': bold_format,
        'selected_note_type': note_type_details_basic,
        'selected_source_field': DefaultFields.basic_front,
        'selected_stop_words': Text("a an")
    }


def test_eq_empty(note_type_details_basic: NoteTypeDetails):
    default_stop_words: Optional[str] = DefaultConfig.default_stop_words
    state1: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details_basic, default_stop_words)
    state2: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details_basic, default_stop_words)
    assert state1 == state2


def test_eq_none(note_type_details_basic: NoteTypeDetails):
    default_stop_words: Optional[str] = DefaultConfig.default_stop_words
    state1: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details_basic, default_stop_words)
    state2: Optional[AdhocHighlightDialogState] = None
    assert state1 != state2


def test_eq_full(note_type_details_basic: NoteTypeDetails, bold_format: HighlightFormat):
    default_stop_words: Optional[str] = DefaultConfig.default_stop_words
    state1: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details_basic, default_stop_words)
    state1.select_source_field(DefaultFields.basic_front)
    state1.select_format(bold_format)
    state1.set_stop_words(Text("a an"))
    state1.select_destination_fields(FieldNames(DefaultFields.all_basic))

    state2: AdhocHighlightDialogState = AdhocHighlightDialogState(note_type_details_basic, default_stop_words)
    state2.select_source_field(DefaultFields.basic_front)
    state2.select_format(bold_format)
    state2.set_stop_words(Text("a an"))
    state2.select_destination_fields(FieldNames(DefaultFields.all_basic))

    assert state1 == state2
