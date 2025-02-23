from aqt import Qt

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, \
    HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from tests.conftest import note_type_details_basic, note_type_details_cloze
from tests.data import DefaultFields, DefaultConfig
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_asserts import assert_format_group_box, \
    assert_source_combo_box, assert_view, HighlightFakeModelListener, FakeCallback
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_scaffold import AdhocHighlightDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


def test_show_view(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                   adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                   note_type_details_all: list[NoteTypeDetails], note_type_details_cloze: NoteTypeDetails,
                   note_type_details_basic: NoteTypeDetails,
                   all_highlight_formats: HighlightFormats, bold_format: HighlightFormat,
                   adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold, visual_qtbot: VisualQtBot,
                   highlight_model_listener: HighlightFakeModelListener):
    callback: FakeCallback = FakeCallback()
    exp_default_stop_words: str = "a an"
    selected_note_types: list[NoteTypeDetails] = [note_type_details_basic, note_type_details_cloze]
    adhoc_highlight_dialog_model.fill(note_type_details_all, selected_note_types, 3, all_highlight_formats,
                                      callback.call, None)
    adhoc_highlight_dialog_model.set_default_stop_words(exp_default_stop_words)
    adhoc_highlight_dialog_model.switch_state(note_type_details_basic)
    # Initial state
    assert highlight_model_listener.counter == 0
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.stop_words)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'default_stop_words': 'a an',
        'note_number': 3,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'a an'},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': 'a an'}}}
    # Fill model without firing
    adhoc_highlight_dialog_model.set_default_stop_words(exp_default_stop_words)
    assert highlight_model_listener.counter == 0
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.stop_words)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'accept_callback_None': False,
        'default_stop_words': 'a an',
        'note_number': 3,
        'formats': all_highlight_formats,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'a an'},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': 'a an'}}}
    # Fire model changes
    adhoc_highlight_dialog_view.show_view()
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert highlight_model_listener.counter == 1
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 3 notes",
                selected_note_type=note_type_details_basic,
                note_types=selected_note_types,
                selected_source_field=DefaultFields.basic_front,
                source_fields=DefaultFields.all_basic, selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=[DefaultFields.basic_front, DefaultFields.basic_back, DefaultFields.basic_extra],
                selected_destination_fields=[],
                disabled_fields=[DefaultFields.basic_front], stop_words=exp_default_stop_words)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'accept_callback_None': False,
        'default_stop_words': 'a an',
        'note_number': 3,
        'formats': all_highlight_formats,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': exp_default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': exp_default_stop_words}}}
    # Choose Note Type
    adhoc_highlight_dialog_view_scaffold.select_note_type(Qt.Key.Key_Down)
    assert highlight_model_listener.counter == 2
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 3 notes",
                selected_note_type=note_type_details_cloze,
                note_types=selected_note_types,
                selected_source_field=DefaultFields.cloze_text,
                source_fields=DefaultFields.all_cloze, selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=[DefaultFields.cloze_text, DefaultFields.cloze_back_extra],
                selected_destination_fields=[],
                disabled_fields=[DefaultFields.cloze_text],
                stop_words=exp_default_stop_words)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'accept_callback_None': False,
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_number': 3,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_cloze,
                          'selected_source_field': DefaultFields.cloze_text,
                          'selected_stop_words': exp_default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': exp_default_stop_words},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_text,
                                                          'selected_stop_words': exp_default_stop_words}}}
    # Choose Field
    adhoc_highlight_dialog_view_scaffold.select_source_field(Qt.Key.Key_Down)
    assert highlight_model_listener.counter == 3
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 3 notes",
                selected_note_type=note_type_details_cloze,
                note_types=selected_note_types,
                selected_source_field=DefaultFields.cloze_back_extra,
                source_fields=DefaultFields.all_cloze, selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=[DefaultFields.cloze_text, DefaultFields.cloze_back_extra],
                selected_destination_fields=[],
                disabled_fields=[DefaultFields.cloze_back_extra],
                stop_words=exp_default_stop_words)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'accept_callback_None': False,
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_number': 3,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_cloze,
                          'selected_source_field': DefaultFields.cloze_back_extra,
                          'selected_stop_words': exp_default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': exp_default_stop_words},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_back_extra,
                                                          'selected_stop_words': exp_default_stop_words}}}

    assert highlight_model_listener.counter == 3
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 3 notes",
                selected_note_type=note_type_details_cloze,
                note_types=selected_note_types,
                selected_source_field=DefaultFields.cloze_back_extra,
                source_fields=DefaultFields.all_cloze, selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=[DefaultFields.cloze_text, DefaultFields.cloze_back_extra],
                selected_destination_fields=[],
                disabled_fields=[DefaultFields.cloze_back_extra],
                stop_words=exp_default_stop_words)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'accept_callback_None': False,
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_number': 3,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_cloze,
                          'selected_source_field': DefaultFields.cloze_back_extra,
                          'selected_stop_words': exp_default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': exp_default_stop_words},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_back_extra,
                                                          'selected_stop_words': exp_default_stop_words}}}

    # Click Start button
    assert callback.counter == 0
    adhoc_highlight_dialog_view_scaffold.mark_destination_field(DefaultFields.cloze_text)
    adhoc_highlight_dialog_view_scaffold.click_start_button()
    assert callback.counter == 1
    assert highlight_model_listener.counter == 4
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'accept_callback_None': False,
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_number': 3,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [DefaultFields.cloze_text],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_cloze,
                          'selected_source_field': DefaultFields.cloze_back_extra,
                          'selected_stop_words': exp_default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': exp_default_stop_words},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [DefaultFields.cloze_text],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_back_extra,
                                                          'selected_stop_words': exp_default_stop_words}}}
    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    assert callback.counter == 1
    assert highlight_model_listener.counter == 4
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'accept_callback_None': False,
        'default_stop_words': 'a an',
        'note_number': 3,
        'formats': all_highlight_formats,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [DefaultFields.cloze_text],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_cloze,
                          'selected_source_field': DefaultFields.cloze_back_extra,
                          'selected_stop_words': exp_default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': exp_default_stop_words},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [DefaultFields.cloze_text],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_back_extra,
                                                          'selected_stop_words': exp_default_stop_words}}}
    # Click Restore Defaults button
    adhoc_highlight_dialog_view_scaffold.click_restore_defaults_button()
    assert callback.counter == 1
    assert highlight_model_listener.counter == 5
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'accept_callback_None': False,
        'default_stop_words': 'a an',
        'note_number': 3,
        'formats': all_highlight_formats,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': exp_default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': exp_default_stop_words},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_text,
                                                          'selected_stop_words': exp_default_stop_words}}}


def test_bug_duplicate_formats_after_reopening(note_type_details_all: list[NoteTypeDetails],
                                               adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                               adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                               all_highlight_formats: HighlightFormats,
                                               bold_format: HighlightFormat):
    # Init model
    assert adhoc_highlight_dialog_model.get_formats() == []
    adhoc_highlight_dialog_model.fill(note_type_details_all, note_type_details_all, 3, all_highlight_formats, None,
                                      None)
    assert adhoc_highlight_dialog_model.get_formats() == all_highlight_formats
    assert_format_group_box(adhoc_highlight_dialog_view, None, [])

    # Fire model fills the format list in combo box
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert adhoc_highlight_dialog_model.get_formats() == all_highlight_formats
    assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)

    # Fire model again duplicates format list in combo box
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert adhoc_highlight_dialog_model.get_formats() == all_highlight_formats
    assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)


def test_remember_selected_source_when_changing_note_type(
        adhoc_highlight_dialog_view: AdhocHighlightDialogView, adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
        note_type_details_all: list[NoteTypeDetails], all_highlight_formats: HighlightFormats,
        bold_format: HighlightFormat, adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
        note_type_details_basic: NoteTypeDetails, note_type_details_cloze: NoteTypeDetails, visual_qtbot: VisualQtBot):
    # Fill model
    selected_note_types: list[NoteTypeDetails] = [note_type_details_basic, note_type_details_cloze]
    adhoc_highlight_dialog_model.fill(note_type_details_all, selected_note_types, 3, all_highlight_formats, None, None)
    # Show dialog
    adhoc_highlight_dialog_view.show_view()
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_front, DefaultFields.all_basic)
    # Choose "Back" field in "Basic" note type
    adhoc_highlight_dialog_view_scaffold.select_source_field(Qt.Key.Key_Down)
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_back, DefaultFields.all_basic)
    # Choose "Cloze" note type
    adhoc_highlight_dialog_view_scaffold.select_note_type(Qt.Key.Key_Down)
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.cloze_text, DefaultFields.all_cloze)
    # Choose "Back Extra" field in "Cloze" note type
    adhoc_highlight_dialog_view_scaffold.select_source_field(Qt.Key.Key_Down)
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.cloze_back_extra, DefaultFields.all_cloze)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'default_stop_words': None,
        'note_number': 3,
        'formats': all_highlight_formats,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_cloze,
                          'selected_source_field': DefaultFields.cloze_back_extra,
                          'selected_stop_words': None},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_back,
                                                          'selected_stop_words': None},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_back_extra,
                                                          'selected_stop_words': None}}}
    # Choose "Basic" note type again
    adhoc_highlight_dialog_view_scaffold.select_note_type(Qt.Key.Key_Up)
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_back, DefaultFields.all_basic)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': selected_note_types,
        'default_stop_words': None,
        'note_number': 3,
        'formats': all_highlight_formats,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_back,
                          'selected_stop_words': None},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_back,
                                                          'selected_stop_words': None},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_back_extra,
                                                          'selected_stop_words': None}}}


def test_repr(adhoc_highlight_dialog_view: AdhocHighlightDialogView):
    assert repr(adhoc_highlight_dialog_view) == "AdhocHighlightDialogView"
