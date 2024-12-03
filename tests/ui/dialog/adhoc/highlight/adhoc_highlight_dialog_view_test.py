from aqt import Qt

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, \
    HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from tests.conftest import basic_note_type_details, cloze_note_type_details
from tests.data import DefaultFields, DefaultStopWords
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_asserts import assert_format_group_box, \
    assert_source_combo_box, assert_view, FakeModelListener, FakeCallback, assert_space_delimited_language
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_scaffold import AdhocHighlightDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


def test_show_view(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                   adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                   all_note_type_details: list[NoteTypeDetails], cloze_note_type_details: NoteTypeDetails,
                   basic_note_type_details: NoteTypeDetails,
                   all_highlight_formats: HighlightFormats, bold_format: HighlightFormat,
                   adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold, visual_qtbot: VisualQtBot):
    callback: FakeCallback = FakeCallback()
    listener: FakeModelListener = FakeModelListener()
    adhoc_highlight_dialog_model.add_listener(listener)
    exp_default_stop_words: str = "a an"
    adhoc_highlight_dialog_model.fill(all_note_type_details, [], all_highlight_formats, callback.call, None)
    adhoc_highlight_dialog_model.set_default_stop_words(exp_default_stop_words)
    adhoc_highlight_dialog_model.switch_state(basic_note_type_details)
    # Initial state
    assert len(listener.history) == 0
    assert_view(adhoc_highlight_dialog_view, current_note_type="", note_types=[], current_field="", source_fields=[],
                selected_format=None, formats=[], check_box_texts=[], selected_fields=[], disabled_fields=[],
                stop_words=DefaultStopWords.in_config, space_delimited_language=False)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'a an',
                          'space_delimited_language': True},
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': 'a an',
                             'space_delimited_language': True}}}
    # Fill model without firing
    adhoc_highlight_dialog_model.set_default_stop_words(exp_default_stop_words)
    assert len(listener.history) == 0
    assert_view(adhoc_highlight_dialog_view, current_note_type="", note_types=[], current_field="", source_fields=[],
                selected_format=None, formats=[], check_box_texts=[], selected_fields=[], disabled_fields=[],
                stop_words=DefaultStopWords.in_config, space_delimited_language=False)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'a an',
                          'space_delimited_language': True},
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': 'a an',
                             'space_delimited_language': True}}}
    # Fire model changes
    adhoc_highlight_dialog_view.show_view()
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert len(listener.history) == 2
    assert_view(adhoc_highlight_dialog_view, current_note_type="Basic", note_types=['Basic', 'Cloze'],
                current_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=['Front', 'Back', 'Extra'], selected_fields=[],
                disabled_fields=[DefaultFields.basic_front], stop_words=exp_default_stop_words,
                space_delimited_language=True)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': exp_default_stop_words,
                          'space_delimited_language': True},
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True}}}
    # Choose Note Type
    adhoc_highlight_dialog_view_scaffold.select_note_type(Qt.Key.Key_Down)
    assert len(listener.history) == 3
    assert_view(adhoc_highlight_dialog_view, current_note_type="Cloze", note_types=['Basic', 'Cloze'],
                current_field=DefaultFields.cloze_text, source_fields=DefaultFields.all_cloze,
                selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=['Text', 'Back Extra'], selected_fields=[], disabled_fields=[DefaultFields.cloze_text],
                stop_words=exp_default_stop_words, space_delimited_language=True)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': cloze_note_type_details,
                          'selected_source_field': DefaultFields.cloze_text,
                          'selected_stop_words': exp_default_stop_words,
                          'space_delimited_language': True},
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_text,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True}}}
    # Choose Field
    adhoc_highlight_dialog_view_scaffold.select_source_field(Qt.Key.Key_Down)
    assert len(listener.history) == 4
    assert_view(adhoc_highlight_dialog_view, current_note_type="Cloze", note_types=['Basic', 'Cloze'],
                current_field=DefaultFields.cloze_extra, source_fields=DefaultFields.all_cloze,
                selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=['Text', 'Back Extra'], selected_fields=[], disabled_fields=[DefaultFields.cloze_extra],
                stop_words=exp_default_stop_words, space_delimited_language=True)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': cloze_note_type_details,
                          'selected_source_field': DefaultFields.cloze_extra,
                          'selected_stop_words': exp_default_stop_words,
                          'space_delimited_language': True},
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_extra,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True}}}
    # Click Start button
    assert callback.counter == 0
    adhoc_highlight_dialog_view_scaffold.mark_destination_field(DefaultFields.cloze_text)
    adhoc_highlight_dialog_view_scaffold.click_start_button()
    assert callback.counter == 1
    assert len(listener.history) == 4
    assert adhoc_highlight_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_destination_fields': [DefaultFields.cloze_text],
                          'selected_format': bold_format,
                          'selected_note_type': cloze_note_type_details,
                          'selected_source_field': DefaultFields.cloze_extra,
                          'selected_stop_words': exp_default_stop_words,
                          'space_delimited_language': True},
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True},
                   'Cloze': {'selected_destination_fields': [DefaultFields.cloze_text],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_extra,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True}}}
    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    assert callback.counter == 1
    assert len(listener.history) == 4
    assert adhoc_highlight_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_destination_fields': [DefaultFields.cloze_text],
                          'selected_format': bold_format,
                          'selected_note_type': cloze_note_type_details,
                          'selected_source_field': DefaultFields.cloze_extra,
                          'selected_stop_words': exp_default_stop_words,
                          'space_delimited_language': True},
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True},
                   'Cloze': {'selected_destination_fields': [DefaultFields.cloze_text],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_extra,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True}}}
    # Click Restore Defaults button
    adhoc_highlight_dialog_view_scaffold.click_restore_defaults_button()
    assert callback.counter == 1
    assert len(listener.history) == 5
    assert adhoc_highlight_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': exp_default_stop_words,
                          'space_delimited_language': True},
        'default_stop_words': 'a an',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_text,
                             'selected_stop_words': exp_default_stop_words,
                             'space_delimited_language': True}}}


def test_bug_duplicate_formats_after_reopening(all_note_type_details: list[NoteTypeDetails],
                                               adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                               adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                               all_highlight_formats: HighlightFormats,
                                               bold_format: HighlightFormat):
    # Init model
    assert adhoc_highlight_dialog_model.get_formats() == []
    adhoc_highlight_dialog_model.fill(all_note_type_details, [], all_highlight_formats,
                                      None, None)
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
        all_note_type_details: list[NoteTypeDetails], all_highlight_formats: HighlightFormats,
        bold_format: HighlightFormat, adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
        basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails, visual_qtbot: VisualQtBot):
    listener: FakeModelListener = FakeModelListener()
    adhoc_highlight_dialog_model.add_listener(listener)
    # Fill model
    adhoc_highlight_dialog_model.fill(all_note_type_details, [], all_highlight_formats, None, None)
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
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.cloze_extra, DefaultFields.all_cloze)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': cloze_note_type_details,
                          'selected_source_field': DefaultFields.cloze_extra,
                          'selected_stop_words': None,
                          'space_delimited_language': True},
        'default_stop_words': None,
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_back,
                             'selected_stop_words': None,
                             'space_delimited_language': True},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_extra,
                             'selected_stop_words': None,
                             'space_delimited_language': True}}}
    # Choose "Basic" note type again
    adhoc_highlight_dialog_view_scaffold.select_note_type(Qt.Key.Key_Up)
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_back, DefaultFields.all_basic)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_back,
                          'selected_stop_words': None,
                          'space_delimited_language': True},
        'default_stop_words': None,
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_back,
                             'selected_stop_words': None,
                             'space_delimited_language': True},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_extra,
                             'selected_stop_words': None,
                             'space_delimited_language': True}}}


def test_remember_space_delimited_language_when_changing_note_type(
        adhoc_highlight_dialog_view: AdhocHighlightDialogView, adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
        all_note_type_details: list[NoteTypeDetails], all_highlight_formats: HighlightFormats,
        bold_format: HighlightFormat, adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
        basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails, visual_qtbot: VisualQtBot):
    listener: FakeModelListener = FakeModelListener()
    adhoc_highlight_dialog_model.add_listener(listener)
    # Fill model
    adhoc_highlight_dialog_model.fill(all_note_type_details, [], all_highlight_formats, None, None)
    # Show dialog
    adhoc_highlight_dialog_view.show_view()
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert_space_delimited_language(adhoc_highlight_dialog_view, True)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': None,
                          'space_delimited_language': True},
        'default_stop_words': None,
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': None,
                             'space_delimited_language': True}}}
    # Uncheck space-delimited language checkbox
    adhoc_highlight_dialog_view_scaffold.click_space_delimited_language()
    assert_space_delimited_language(adhoc_highlight_dialog_view, False)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': None,
                          'space_delimited_language': False},
        'default_stop_words': None,
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': None,
                             'space_delimited_language': False}}}
    # Choose "Cloze" note type
    adhoc_highlight_dialog_view_scaffold.select_note_type(Qt.Key.Key_Down)
    assert_space_delimited_language(adhoc_highlight_dialog_view, True)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': cloze_note_type_details,
                          'selected_source_field': DefaultFields.cloze_text,
                          'selected_stop_words': None,
                          'space_delimited_language': True},
        'default_stop_words': None,
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': None,
                             'space_delimited_language': False},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_text,
                             'selected_stop_words': None,
                             'space_delimited_language': True}}}
    # Choose "Basic" note type again
    adhoc_highlight_dialog_view_scaffold.select_note_type(Qt.Key.Key_Up)
    assert_space_delimited_language(adhoc_highlight_dialog_view, False)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': None,
                          'space_delimited_language': False},
        'default_stop_words': None,
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': None,
                             'space_delimited_language': False},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': DefaultFields.cloze_text,
                             'selected_stop_words': None,
                             'space_delimited_language': True}}}


def test_repr(adhoc_highlight_dialog_view: AdhocHighlightDialogView):
    assert repr(adhoc_highlight_dialog_view) == "AdhocHighlightDialogView"
