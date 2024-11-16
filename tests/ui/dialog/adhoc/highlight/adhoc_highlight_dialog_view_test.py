from typing import Optional

from PyQtPath.path_chain_pyqt6 import path, PyQtPath
from aqt import QComboBox, Qt, QCheckBox, QDialogButtonBox, QPushButton

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, \
    HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldName, FieldNames, Text, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel, \
    AdhocHighlightDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.adhoc.highlight.format_group_box import FormatGroupBox
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout, TitledLineEditLayout
from tests.data import DefaultFields
from tests.qtget import get_items
from tests.visual_qtbot import VisualQtBot


class FakeCallback:
    history: list[HighlightOpParams] = []

    @staticmethod
    def call(params: HighlightOpParams):
        FakeCallback.history.append(params)


class FakeModelListener(AdhocHighlightDialogModelListener):
    history: list[object] = []

    def model_changed(self, source: object):
        FakeModelListener.history.append(source)


def test_show_view(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                   adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                   all_note_type_details: list[NoteTypeDetails], cloze_note_type_details: NoteTypeDetails,
                   all_highlight_formats: HighlightFormats, bold_format: HighlightFormat, visual_qtbot: VisualQtBot):
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())
    adhoc_highlight_dialog_model.default_stop_words = "a an"
    # Initial state
    __assert_view(adhoc_highlight_dialog_view, current_note_type="", note_types=[], current_field="", source_fields=[],
                  selected_format=None, formats=[], check_box_texts=[], selected_fields=[], disabled_field="")
    __assert_model(adhoc_highlight_dialog_model, no_callback=True,
                   destination_fields=[], disabled_destination_fields=[],
                   note_types=[], formats=HighlightFormats([]),
                   selected_note_type=None, selected_format=None, selected_source_field={}, selected_stop_words=None,
                   selected_destination_fields=[], model_history_counter=0)
    # Fill model without firing
    adhoc_highlight_dialog_model.note_types = all_note_type_details
    adhoc_highlight_dialog_model.formats = all_highlight_formats
    adhoc_highlight_dialog_model.run_op_callback = FakeCallback.call
    __assert_view(adhoc_highlight_dialog_view, current_note_type="", note_types=[], current_field="", source_fields=[],
                  selected_format=None, formats=[], check_box_texts=[], selected_fields=[], disabled_field="")
    __assert_model(adhoc_highlight_dialog_model, no_callback=False,
                   destination_fields=[], disabled_destination_fields=[],
                   note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                   selected_format=None, selected_source_field={}, selected_stop_words=None,
                   selected_destination_fields=[], model_history_counter=0)
    # Fire model changes
    adhoc_highlight_dialog_view.show_view()
    __assert_view(adhoc_highlight_dialog_view, current_note_type="Basic", note_types=['Basic', 'Cloze'],
                  current_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                  selected_format=bold_format, formats=all_highlight_formats,
                  check_box_texts=['Front', 'Back', 'Extra'], selected_fields=[],
                  disabled_field=DefaultFields.basic_front)
    __assert_model(adhoc_highlight_dialog_model, no_callback=False,
                   destination_fields=DefaultFields.all_basic, disabled_destination_fields=[DefaultFields.basic_front],
                   note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                   selected_format=bold_format, selected_source_field={}, selected_stop_words=None,
                   selected_destination_fields=[], model_history_counter=3)
    # Choose Note Type
    note_type_combo_box: QComboBox = path(adhoc_highlight_dialog_view).group(0).child(
        TitledComboBoxLayout, 0).combobox().get()
    visual_qtbot.mouseClick(note_type_combo_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(note_type_combo_box, Qt.Key.Key_Down)
    visual_qtbot.keyClick(note_type_combo_box.view(), Qt.Key.Key_Enter)
    __assert_view(adhoc_highlight_dialog_view, current_note_type="Cloze", note_types=['Basic', 'Cloze'],
                  current_field=DefaultFields.cloze_text, source_fields=DefaultFields.all_cloze,
                  selected_format=bold_format, formats=all_highlight_formats,
                  check_box_texts=['Text', 'Back Extra'], selected_fields=[], disabled_field=DefaultFields.cloze_text)
    __assert_model(adhoc_highlight_dialog_model, no_callback=False,
                   destination_fields=DefaultFields.all_cloze, disabled_destination_fields=[DefaultFields.cloze_text],
                   note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                   selected_format=bold_format, selected_source_field={}, selected_stop_words=None,
                   selected_destination_fields=[], model_history_counter=7)
    # Choose Field
    filed_combo_box: QComboBox = path(adhoc_highlight_dialog_view).group(0).child(
        TitledComboBoxLayout, 1).combobox().get()
    visual_qtbot.mouseClick(filed_combo_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(filed_combo_box, Qt.Key.Key_Down)
    visual_qtbot.keyClick(filed_combo_box.view(), Qt.Key.Key_Enter)
    __assert_view(adhoc_highlight_dialog_view, current_note_type="Cloze", note_types=['Basic', 'Cloze'],
                  current_field=DefaultFields.cloze_extra, source_fields=DefaultFields.all_cloze,
                  selected_format=bold_format, formats=all_highlight_formats,
                  check_box_texts=['Text', 'Back Extra'], selected_fields=[], disabled_field=DefaultFields.cloze_extra)
    __assert_model(adhoc_highlight_dialog_model, no_callback=False,
                   destination_fields=DefaultFields.all_cloze, disabled_destination_fields=[DefaultFields.cloze_extra],
                   note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                   selected_format=bold_format, selected_source_field={}, selected_stop_words=None,
                   selected_destination_fields=[], model_history_counter=8)
    # Click Start button
    assert FakeCallback.history == []
    check_box: QCheckBox = path(adhoc_highlight_dialog_view).child(FieldsLayout).checkbox().get()
    visual_qtbot.mouseClick(check_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(check_box, Qt.Key.Key_Space)  # Mouse click just focus on check_box, but doesn't select it
    button_box: QDialogButtonBox = path(adhoc_highlight_dialog_view).child(QDialogButtonBox).get()
    start_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
    visual_qtbot.mouseClick(start_button, Qt.MouseButton.LeftButton)
    start_params: HighlightOpParams = HighlightOpParams(note_type_id=cloze_note_type_details.note_type_id,
                                                        note_ids=set(), parent=None,
                                                        source_field=DefaultFields.cloze_extra,
                                                        destination_fields=FieldNames([DefaultFields.cloze_text]),
                                                        stop_words=Text("a an to"),
                                                        highlight_format=bold_format)
    assert FakeCallback.history == [start_params]
    __assert_model(adhoc_highlight_dialog_model, no_callback=False,
                   destination_fields=DefaultFields.all_cloze, disabled_destination_fields=[DefaultFields.cloze_extra],
                   note_types=all_note_type_details, formats=all_highlight_formats,
                   selected_note_type=cloze_note_type_details, selected_format=bold_format,
                   selected_source_field={cloze_note_type_details.name: DefaultFields.cloze_extra},
                   selected_stop_words='a an to', selected_destination_fields=[DefaultFields.cloze_text],
                   model_history_counter=9)
    # Click Cancel button
    cancel_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Cancel)
    visual_qtbot.mouseClick(cancel_button, Qt.MouseButton.LeftButton)
    assert FakeCallback.history == [start_params]
    __assert_model(adhoc_highlight_dialog_model, no_callback=False,
                   destination_fields=DefaultFields.all_cloze, disabled_destination_fields=[DefaultFields.cloze_extra],
                   note_types=all_note_type_details, formats=all_highlight_formats,
                   selected_note_type=cloze_note_type_details, selected_format=bold_format,
                   selected_source_field={cloze_note_type_details.name: DefaultFields.cloze_extra},
                   selected_stop_words='a an to', selected_destination_fields=[DefaultFields.cloze_text],
                   model_history_counter=10)
    # Click Restore Defaults button
    restore_defaults_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
    visual_qtbot.mouseClick(restore_defaults_button, Qt.MouseButton.LeftButton)
    assert FakeCallback.history == [start_params]
    __assert_model(adhoc_highlight_dialog_model, no_callback=False,
                   destination_fields=DefaultFields.all_basic, disabled_destination_fields=[DefaultFields.basic_front],
                   note_types=all_note_type_details, formats=all_highlight_formats, selected_note_type=None,
                   selected_format=bold_format, selected_source_field={}, selected_stop_words='a an',
                   selected_destination_fields=[], model_history_counter=19)


def test_bug_duplicate_formats_after_reopening(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                               adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                               all_highlight_formats: HighlightFormats,
                                               bold_format: HighlightFormat):
    assert adhoc_highlight_dialog_model.formats == []
    __assert_format_group_box(adhoc_highlight_dialog_view, None, [])

    adhoc_highlight_dialog_model.formats = all_highlight_formats
    assert adhoc_highlight_dialog_model.formats == all_highlight_formats
    __assert_format_group_box(adhoc_highlight_dialog_view, None, [])

    # Fire model fills the format list in combo box
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert adhoc_highlight_dialog_model.formats == all_highlight_formats
    __assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)

    # Fire model again duplicates format list in combo box
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert adhoc_highlight_dialog_model.formats == all_highlight_formats
    __assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)


def test_remember_selected_source_when_changing_note_type(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                                          adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                                          all_note_type_details: list[NoteTypeDetails],
                                                          all_highlight_formats: HighlightFormats,
                                                          visual_qtbot: VisualQtBot):
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())
    # Fill model
    adhoc_highlight_dialog_model.note_types = all_note_type_details
    adhoc_highlight_dialog_model.formats = all_highlight_formats
    adhoc_highlight_dialog_model.run_op_callback = FakeCallback.call
    adhoc_highlight_dialog_view.show_view()
    __assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_front, DefaultFields.all_basic)
    # Choose "Back" field in "Basic" note type
    filed_combo_box: QComboBox = path(adhoc_highlight_dialog_view).group(0).child(
        TitledComboBoxLayout, 1).combobox().get()
    visual_qtbot.mouseClick(filed_combo_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(filed_combo_box, Qt.Key.Key_Down)
    visual_qtbot.keyClick(filed_combo_box.view(), Qt.Key.Key_Enter)
    __assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_back, DefaultFields.all_basic)
    # Choose "Cloze" note type
    note_type_combo_box: QComboBox = path(adhoc_highlight_dialog_view).group(0).child(
        TitledComboBoxLayout, 0).combobox().get()
    visual_qtbot.mouseClick(note_type_combo_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(note_type_combo_box, Qt.Key.Key_Down)
    visual_qtbot.keyClick(note_type_combo_box.view(), Qt.Key.Key_Enter)
    __assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.cloze_text, DefaultFields.all_cloze)
    # Choose "Back Extra" field in "Cloze" note type
    filed_combo_box: QComboBox = path(adhoc_highlight_dialog_view).group(0).child(
        TitledComboBoxLayout, 1).combobox().get()
    visual_qtbot.mouseClick(filed_combo_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(filed_combo_box, Qt.Key.Key_Down)
    visual_qtbot.keyClick(filed_combo_box.view(), Qt.Key.Key_Enter)
    __assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.cloze_extra, DefaultFields.all_cloze)
    # Choose "Basic" note type again
    note_type_combo_box: QComboBox = path(adhoc_highlight_dialog_view).group(0).child(
        TitledComboBoxLayout, 0).combobox().get()
    visual_qtbot.mouseClick(note_type_combo_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(note_type_combo_box, Qt.Key.Key_Up)
    visual_qtbot.keyClick(note_type_combo_box.view(), Qt.Key.Key_Enter)
    __assert_source_combo_box(adhoc_highlight_dialog_view, DefaultFields.basic_front, DefaultFields.all_basic)


def test_remember_format(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                         adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                         all_note_type_details: list[NoteTypeDetails],
                         all_highlight_formats: HighlightFormats,
                         bold_format: HighlightFormat,
                         italic_format: HighlightFormat,
                         visual_qtbot: VisualQtBot):
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())
    # Fill model
    adhoc_highlight_dialog_model.note_types = all_note_type_details
    adhoc_highlight_dialog_model.formats = all_highlight_formats
    adhoc_highlight_dialog_model.run_op_callback = FakeCallback.call
    # Show dialog
    adhoc_highlight_dialog_view.show_view()
    __assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)
    # Choose "Italic" format
    format_combo_box: QComboBox = path(adhoc_highlight_dialog_view).child(FormatGroupBox).child(
        TitledComboBoxLayout).combobox().get()
    visual_qtbot.mouseClick(format_combo_box, Qt.MouseButton.LeftButton)
    visual_qtbot.keyClick(format_combo_box, Qt.Key.Key_Down)
    visual_qtbot.keyClick(format_combo_box.view(), Qt.Key.Key_Enter)
    __assert_format_group_box(adhoc_highlight_dialog_view, italic_format, all_highlight_formats)
    # Click Cancel button
    button_box: QDialogButtonBox = path(adhoc_highlight_dialog_view).child(QDialogButtonBox).get()
    cancel_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Cancel)
    visual_qtbot.mouseClick(cancel_button, Qt.MouseButton.LeftButton)
    # Show dialog again
    adhoc_highlight_dialog_view.show_view()
    __assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)  # TODO should be italic


def test_repr(adhoc_highlight_dialog_view: AdhocHighlightDialogView):
    assert repr(adhoc_highlight_dialog_view) == "AdhocHighlightDialogView"


def __assert_view(view: AdhocHighlightDialogView, current_note_type: str, note_types: list[str],
                  current_field: str, source_fields: list[str], selected_format: Optional[HighlightFormat],
                  formats: list[HighlightFormat], check_box_texts: list[str], selected_fields: list[str],
                  disabled_field: str):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == "Highlight"
    __assert_buttons(view)
    __assert_source_group_box(view, current_note_type, note_types, current_field, source_fields, "a an to")
    __assert_format_group_box(view, selected_format, formats)
    __assert_destination_group_box(view, check_box_texts, selected_fields, disabled_field)


def __assert_source_group_box(view: AdhocHighlightDialogView, current_note_type: str, note_types: list[str],
                              current_source_field: str, source_fields: list[str], stop_words: str):
    group_box: PyQtPath = path(view).group(0)

    note_type: PyQtPath = group_box.child(TitledComboBoxLayout, 0)
    assert note_type.label().get().text() == "Note Type"
    note_type_combo_box: QComboBox = note_type.combobox().get()
    assert note_type_combo_box.currentText() == current_note_type
    assert get_items(note_type_combo_box) == note_types

    __assert_source_combo_box(view, current_source_field, source_fields)

    assert group_box.child(TitledLineEditLayout).get().get_text() == stop_words


def __assert_source_combo_box(view: AdhocHighlightDialogView, current_source_field: str, source_fields: list[str]):
    group_box: PyQtPath = path(view).group(0)
    field_path: PyQtPath = group_box.child(TitledComboBoxLayout, 1)
    assert field_path.label().get().text() == "Field"
    field_combo_box: QComboBox = field_path.combobox().get()
    assert field_combo_box.currentText() == current_source_field
    assert get_items(field_combo_box) == source_fields


def __assert_format_group_box(view: AdhocHighlightDialogView, current_format: Optional[HighlightFormat],
                              formats: list[HighlightFormat]):
    combo_box: PyQtPath = path(view).group(1).child(TitledComboBoxLayout)
    assert combo_box.label().get().text() == "Format"
    format_combo_box: QComboBox = combo_box.combobox().get()
    assert format_combo_box.currentText() == (current_format.name if current_format else "")
    format_names: list[str] = [highlight_format.name for highlight_format in formats]
    assert get_items(format_combo_box) == format_names


def __assert_destination_group_box(view: AdhocHighlightDialogView, check_box_texts: list[str],
                                   selected_fields: list[str], disabled_field: str):
    group_box: PyQtPath = path(view).group(2)
    assert group_box.label().get().text() == "Fields:"
    fields_layout: FieldsLayout = group_box.child(FieldsLayout).get()
    assert fields_layout.get_selected_field_names() == selected_fields
    check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    texts: list[str] = [check_box.text() for check_box in check_boxes]
    assert texts == check_box_texts
    for check_box in check_boxes:
        should_be_enabled: bool = check_box.text() != disabled_field
        assert check_box.isEnabled() == should_be_enabled


def __assert_buttons(view: AdhocHighlightDialogView):
    start_button: QPushButton = path(view).child(QDialogButtonBox).button(0).get()
    assert start_button.text() == "Start"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    assert cancel_button.text() == "&Cancel"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"


def __assert_model(adhoc_highlight_dialog_model: AdhocHighlightDialogModel, no_callback: bool,
                   note_types: list[NoteTypeDetails], formats: HighlightFormats,
                   destination_fields: list[str], disabled_destination_fields: list[str],
                   selected_note_type: Optional[NoteTypeDetails], selected_format: Optional[HighlightFormat],
                   selected_source_field: dict[NoteTypeName, FieldName], selected_stop_words: Optional[str],
                   selected_destination_fields: list[str], model_history_counter: int):
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an',
        'destination_fields': destination_fields,
        'disabled_destination_fields': disabled_destination_fields,
        'formats': formats,
        'note_ids': set(),
        'note_types': note_types,
        'run_op_callback_None': no_callback,
        'selected_destination_fields': selected_destination_fields,
        'selected_format': selected_format,
        'selected_note_type': selected_note_type,
        'selected_source_field': selected_source_field,
        'selected_stop_words': selected_stop_words}
    assert len(FakeModelListener.history) == model_history_counter
