from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, \
    HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, Text
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from tests.data import DefaultFields
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_asserts import assert_format_group_box, \
    assert_source_combo_box, assert_model, assert_view, FakeModelListener, FakeCallback
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_scaffold import AdhocHighlightDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


def test_show_view(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                   adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                   all_note_type_details: list[NoteTypeDetails], cloze_note_type_details: NoteTypeDetails,
                   all_highlight_formats: HighlightFormats, bold_format: HighlightFormat,
                   adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold, visual_qtbot: VisualQtBot):
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())
    adhoc_highlight_dialog_model.default_stop_words = "a an"
    # Initial state
    assert_view(adhoc_highlight_dialog_view, current_note_type="", note_types=[], current_field="", source_fields=[],
                selected_format=None, formats=[], check_box_texts=[], selected_fields=[], disabled_field="")
    assert_model(adhoc_highlight_dialog_model, no_callback=True,
                 destination_fields=[], disabled_destination_fields=[],
                 note_types=[], formats=HighlightFormats([]),
                 selected_note_type=None, selected_format=None, selected_source_field={}, selected_stop_words=None,
                 selected_destination_fields=[], model_history_counter=0)
    # Fill model without firing
    adhoc_highlight_dialog_model.note_types = all_note_type_details
    adhoc_highlight_dialog_model.formats = all_highlight_formats
    adhoc_highlight_dialog_model.run_op_callback = FakeCallback.call
    assert_view(adhoc_highlight_dialog_view, current_note_type="", note_types=[], current_field="", source_fields=[],
                selected_format=None, formats=[], check_box_texts=[], selected_fields=[], disabled_field="")
    assert_model(adhoc_highlight_dialog_model, no_callback=False,
                 destination_fields=[], disabled_destination_fields=[],
                 note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                 selected_format=None, selected_source_field={}, selected_stop_words=None,
                 selected_destination_fields=[], model_history_counter=0)
    # Fire model changes
    adhoc_highlight_dialog_view.show_view()
    visual_qtbot.waitExposed(adhoc_highlight_dialog_view)
    assert_view(adhoc_highlight_dialog_view, current_note_type="Basic", note_types=['Basic', 'Cloze'],
                current_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=['Front', 'Back', 'Extra'], selected_fields=[],
                disabled_field=DefaultFields.basic_front)
    assert_model(adhoc_highlight_dialog_model, no_callback=False,
                 destination_fields=DefaultFields.all_basic, disabled_destination_fields=[DefaultFields.basic_front],
                 note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                 selected_format=bold_format, selected_source_field={}, selected_stop_words=None,
                 selected_destination_fields=[], model_history_counter=3)
    # Choose Note Type
    adhoc_highlight_dialog_view_scaffold.select_2nd_note_type()
    assert_view(adhoc_highlight_dialog_view, current_note_type="Cloze", note_types=['Basic', 'Cloze'],
                current_field=DefaultFields.cloze_text, source_fields=DefaultFields.all_cloze,
                selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=['Text', 'Back Extra'], selected_fields=[], disabled_field=DefaultFields.cloze_text)
    assert_model(adhoc_highlight_dialog_model, no_callback=False,
                 destination_fields=DefaultFields.all_cloze, disabled_destination_fields=[DefaultFields.cloze_text],
                 note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                 selected_format=bold_format, selected_source_field={}, selected_stop_words=None,
                 selected_destination_fields=[], model_history_counter=7)
    # Choose Field
    adhoc_highlight_dialog_view_scaffold.select_2nd_source_field_combo_box()
    assert_view(adhoc_highlight_dialog_view, current_note_type="Cloze", note_types=['Basic', 'Cloze'],
                current_field=DefaultFields.cloze_extra, source_fields=DefaultFields.all_cloze,
                selected_format=bold_format, formats=all_highlight_formats,
                check_box_texts=['Text', 'Back Extra'], selected_fields=[], disabled_field=DefaultFields.cloze_extra)
    assert_model(adhoc_highlight_dialog_model, no_callback=False,
                 destination_fields=DefaultFields.all_cloze, disabled_destination_fields=[DefaultFields.cloze_extra],
                 note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                 selected_format=bold_format, selected_source_field={}, selected_stop_words=None,
                 selected_destination_fields=[], model_history_counter=8)
    # Click Start button
    assert FakeCallback.history == []
    adhoc_highlight_dialog_view_scaffold.mark_destination_field()
    adhoc_highlight_dialog_view_scaffold.click_start_button()
    start_params: HighlightOpParams = HighlightOpParams(note_type_id=cloze_note_type_details.note_type_id,
                                                        note_ids=set(), parent=None,
                                                        source_field=DefaultFields.cloze_extra,
                                                        destination_fields=FieldNames([DefaultFields.cloze_text]),
                                                        stop_words=Text("a an to"),
                                                        highlight_format=bold_format)
    assert FakeCallback.history == [start_params]
    assert_model(adhoc_highlight_dialog_model, no_callback=False,
                 destination_fields=DefaultFields.all_cloze, disabled_destination_fields=[DefaultFields.cloze_extra],
                 note_types=all_note_type_details, formats=all_highlight_formats,
                 selected_note_type=cloze_note_type_details, selected_format=bold_format,
                 selected_source_field={cloze_note_type_details.name: DefaultFields.cloze_extra},
                 selected_stop_words='a an to', selected_destination_fields=[DefaultFields.cloze_text],
                 model_history_counter=9)
    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    assert FakeCallback.history == [start_params]
    assert_model(adhoc_highlight_dialog_model, no_callback=False,
                 destination_fields=DefaultFields.all_cloze, disabled_destination_fields=[DefaultFields.cloze_extra],
                 note_types=all_note_type_details, formats=all_highlight_formats,
                 selected_note_type=cloze_note_type_details, selected_format=bold_format,
                 selected_source_field={cloze_note_type_details.name: DefaultFields.cloze_extra},
                 selected_stop_words='a an to', selected_destination_fields=[DefaultFields.cloze_text],
                 model_history_counter=10)
    # Click Restore Defaults button
    adhoc_highlight_dialog_view_scaffold.click_restore_defaults_button()
    assert FakeCallback.history == [start_params]
    assert_model(adhoc_highlight_dialog_model, no_callback=False,
                 destination_fields=DefaultFields.all_basic, disabled_destination_fields=[DefaultFields.basic_front],
                 note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                 selected_format=bold_format, selected_source_field={}, selected_stop_words='a an',
                 selected_destination_fields=[], model_history_counter=19)


def test_bug_duplicate_formats_after_reopening(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                               adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                               all_highlight_formats: HighlightFormats,
                                               bold_format: HighlightFormat):
    assert adhoc_highlight_dialog_model.formats == []
    assert_format_group_box(adhoc_highlight_dialog_view, None, [])

    adhoc_highlight_dialog_model.formats = all_highlight_formats
    assert adhoc_highlight_dialog_model.formats == all_highlight_formats
    assert_format_group_box(adhoc_highlight_dialog_view, None, [])

    # Fire model fills the format list in combo box
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert adhoc_highlight_dialog_model.formats == all_highlight_formats
    assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)

    # Fire model again duplicates format list in combo box
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert adhoc_highlight_dialog_model.formats == all_highlight_formats
    assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)


def test_remember_selected_source_when_changing_note_type(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                                          adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                                          all_note_type_details: list[NoteTypeDetails],
                                                          all_highlight_formats: HighlightFormats,
                                                          adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
                                                          visual_qtbot: VisualQtBot):
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())
    # Fill model
    adhoc_highlight_dialog_model.note_types = all_note_type_details
    adhoc_highlight_dialog_model.formats = all_highlight_formats
    adhoc_highlight_dialog_model.run_op_callback = FakeCallback.call
    # Show dialog
    adhoc_highlight_dialog_view.show_view()
    visual_qtbot.waitExposed(adhoc_highlight_dialog_view)
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_front, DefaultFields.all_basic)
    # Choose "Back" field in "Basic" note type
    adhoc_highlight_dialog_view_scaffold.select_2nd_source_field_combo_box()
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_back, DefaultFields.all_basic)
    # Choose "Cloze" note type
    adhoc_highlight_dialog_view_scaffold.select_2nd_note_type()
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.cloze_text, DefaultFields.all_cloze)
    # Choose "Back Extra" field in "Cloze" note type
    adhoc_highlight_dialog_view_scaffold.select_2nd_source_field_combo_box()
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.cloze_extra, DefaultFields.all_cloze)
    # Choose "Basic" note type again
    adhoc_highlight_dialog_view_scaffold.select_1st_note_type()
    assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_front, DefaultFields.all_basic)


def test_remember_format(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                         adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                         all_note_type_details: list[NoteTypeDetails],
                         all_highlight_formats: HighlightFormats,
                         bold_format: HighlightFormat,
                         italic_format: HighlightFormat,
                         adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
                         visual_qtbot: VisualQtBot):
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())
    # Fill model
    adhoc_highlight_dialog_model.note_types = all_note_type_details
    adhoc_highlight_dialog_model.formats = all_highlight_formats
    adhoc_highlight_dialog_model.run_op_callback = FakeCallback.call
    # Show dialog
    adhoc_highlight_dialog_view.show_view()
    visual_qtbot.waitExposed(adhoc_highlight_dialog_view)
    assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)
    # Choose "Italic" format
    adhoc_highlight_dialog_view_scaffold.select_2nd_format_combo_box()
    assert_format_group_box(adhoc_highlight_dialog_view, italic_format, all_highlight_formats)
    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    # Show dialog again
    adhoc_highlight_dialog_view.show_view()
    assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)  # TODO should be italic


def test_repr(adhoc_highlight_dialog_view: AdhocHighlightDialogView):
    assert repr(adhoc_highlight_dialog_view) == "AdhocHighlightDialogView"
