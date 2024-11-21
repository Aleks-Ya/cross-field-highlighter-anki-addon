from typing import Optional

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import Text
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_state import AdhocHighlightDialogState
from tests.data import DefaultFields


def test_as_dict_empty():
    state: AdhocHighlightDialogState = AdhocHighlightDialogState()
    assert state.as_dict() == {
        'selected_destination_fields': [],
        'selected_format': None,
        'selected_note_type': None,
        'selected_source_field': None,
        'selected_stop_words': None
    }


def test_as_dict_full(basic_note_type_details: NoteTypeDetails, bold_format: HighlightFormat):
    state: AdhocHighlightDialogState = AdhocHighlightDialogState()
    state.selected_note_type = basic_note_type_details
    state.selected_source_field = DefaultFields.basic_front
    state.selected_format = bold_format
    state.selected_stop_words = Text("a an")
    state.selected_destination_fields = DefaultFields.all_basic
    assert state.as_dict() == {
        'selected_destination_fields': DefaultFields.all_basic,
        'selected_format': bold_format,
        'selected_note_type': basic_note_type_details,
        'selected_source_field': DefaultFields.basic_front,
        'selected_stop_words': Text("a an")
    }


def test_eq_empty():
    state1: AdhocHighlightDialogState = AdhocHighlightDialogState()
    state2: AdhocHighlightDialogState = AdhocHighlightDialogState()
    assert state1 == state2


def test_eq_none():
    state1: AdhocHighlightDialogState = AdhocHighlightDialogState()
    state2: Optional[AdhocHighlightDialogState] = None
    assert state1 != state2


def test_eq_full(basic_note_type_details: NoteTypeDetails, bold_format: HighlightFormat):
    state1: AdhocHighlightDialogState = AdhocHighlightDialogState()
    state1.selected_note_type = basic_note_type_details
    state1.selected_source_field = DefaultFields.basic_front
    state1.selected_format = bold_format
    state1.selected_stop_words = Text("a an")
    state1.selected_destination_fields = DefaultFields.all_basic

    state2: AdhocHighlightDialogState = AdhocHighlightDialogState()
    state2.selected_note_type = basic_note_type_details
    state2.selected_source_field = DefaultFields.basic_front
    state2.selected_format = bold_format
    state2.selected_stop_words = Text("a an")
    state2.selected_destination_fields = DefaultFields.all_basic

    assert state1 == state2
