from anki.notes import Note, NoteId

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode, \
    HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from tests.conftest import cloze_note_type_details, bold_format, all_highlight_formats, basic_note_type_details
from tests.data import Data, DefaultFields
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_asserts import assert_format_group_box, \
    FakeModelListener, FakeHighlightControllerCallback
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_scaffold import AdhocHighlightDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


def test_show_dialog(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                     adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                     adhoc_highlight_dialog_model: AdhocHighlightDialogModel, td: Data,
                     all_note_type_details: list[NoteTypeDetails], all_highlight_formats: HighlightFormats,
                     bold_format: HighlightFormat, basic_note_type_details: NoteTypeDetails):
    callback: FakeHighlightControllerCallback = FakeHighlightControllerCallback()
    listener: FakeModelListener = FakeModelListener()
    adhoc_highlight_dialog_model.add_listener(listener)

    note_1: Note = td.create_basic_note_1()
    note_ids: list[NoteId] = [note_1.id]
    params: DialogParams = DialogParams(all_note_type_details, note_ids)
    assert callback.history == []
    assert listener.history == []
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an to',
        'formats': all_highlight_formats,
        'note_ids': set(),
        'note_types': [],
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {},
        'current_state': None}

    adhoc_highlight_dialog_controller.show_dialog(params, FakeHighlightControllerCallback.call)
    assert callback.history == []
    assert len(listener.history) == 4
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an to',
        'formats': all_highlight_formats,
        'note_ids': note_ids,
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': 'a an to'}},
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'a an to'}}


def test_update_config(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                       adhoc_highlight_dialog_model: AdhocHighlightDialogModel, config_loader: ConfigLoader,
                       basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails,
                       all_note_type_details: list[NoteTypeDetails], bold_format: HighlightFormat,
                       all_highlight_formats: HighlightFormats, ):
    callback: FakeHighlightControllerCallback = FakeHighlightControllerCallback()
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': None,
                'Last Source Field Name': {},
                'Last Format': None,
                'Last Stop Words': None,
                'Last Destination Field Names': None,
                "Default Stop Words": "a an to"},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an to',
        'formats': all_highlight_formats,
        'note_ids': set(),
        'note_types': [],
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {},
        'current_state': None}

    # Update config from model
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, []), callback.call)
    adhoc_highlight_dialog_model.switch_state(basic_note_type_details)
    adhoc_highlight_dialog_model.current_state.selected_source_field = DefaultFields.basic_front
    adhoc_highlight_dialog_model.fire_model_changed(None)
    adhoc_highlight_dialog_model.accept_callback()
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': 'Basic',
                'Last Source Field Name': {basic_note_type_details.name: DefaultFields.basic_front},
                'Last Format': bold_format.code.name,
                'Last Stop Words': 'a an to',
                'Last Destination Field Names': [],
                "Default Stop Words": "a an to"},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an to',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': 'a an to'},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': 'Text',
                             'selected_stop_words': 'a an to'}},
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'a an to'}}

    # Update again
    adhoc_highlight_dialog_model.selected_note_type = cloze_note_type_details
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an to',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {'Basic': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': 'a an to'},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': 'Text',
                             'selected_stop_words': 'a an to'}},
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'a an to'}}


def test_fill_model_from_config_on_startup(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                           adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                           note_type_details_factory: NoteTypeDetailsFactory,
                                           config_loader: ConfigLoader,
                                           basic_note_type_details: NoteTypeDetails,
                                           cloze_note_type_details: NoteTypeDetails,
                                           formatter_facade: FormatterFacade,
                                           all_note_type_details: list[NoteTypeDetails],
                                           all_highlight_formats: HighlightFormats, bold_format: HighlightFormat):
    callback: FakeHighlightControllerCallback = FakeHighlightControllerCallback()
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': None,
                'Last Source Field Name': {},
                'Last Format': None,
                'Last Stop Words': None,
                'Last Destination Field Names': None,
                "Default Stop Words": "a an to"},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an to',
        'formats': all_highlight_formats,
        'note_ids': set(),
        'note_types': [],
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {},
        'current_state': None}

    # Update config from model
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, []), callback.call)
    adhoc_highlight_dialog_model.switch_state(basic_note_type_details)
    adhoc_highlight_dialog_model.current_state.selected_source_field = DefaultFields.basic_front
    adhoc_highlight_dialog_model.selected_format = formatter_facade.get_format_by_code(HighlightFormatCode.BOLD)
    adhoc_highlight_dialog_model.current_state.selected_stop_words = "to the"
    adhoc_highlight_dialog_model.current_state.selected_destination_fields = FieldNames([DefaultFields.basic_back])
    adhoc_highlight_dialog_model.fire_model_changed(None)
    adhoc_highlight_dialog_model.accept_callback()
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': 'Basic',
                'Last Source Field Name': {"Basic": "Front"},
                'Last Format': 'BOLD',
                'Last Stop Words': 'to the',
                'Last Destination Field Names': ['Back'],
                "Default Stop Words": "a an to"},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': 'a an to',
        'formats': all_highlight_formats,
        'note_ids': [],
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {'Basic': {'selected_destination_fields': [DefaultFields.basic_back],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': 'to the'},
                   'Cloze': {'selected_destination_fields': [],
                             'selected_format': bold_format,
                             'selected_note_type': cloze_note_type_details,
                             'selected_source_field': 'Text',
                             'selected_stop_words': 'a an to'}},
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'to the'}}

    # Initialize controller using saved config
    config: Config = config_loader.load_config()
    model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    view: AdhocHighlightDialogView = AdhocHighlightDialogView(model, note_type_details_factory)
    _: AdhocHighlightDialogController = AdhocHighlightDialogController(
        model, view, note_type_details_factory, formatter_facade, config, config_loader)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': 'Basic',
                'Last Source Field Name': {"Basic": "Front"},
                'Last Format': 'BOLD',
                'Last Stop Words': 'to the',
                'Last Destination Field Names': ['Back'],
                "Default Stop Words": "a an to"},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert model.as_dict() == {
        'default_stop_words': 'a an to',
        'formats': all_highlight_formats,
        'note_ids': set(),
        'note_types': [],
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {'Basic': {'selected_destination_fields': [DefaultFields.basic_back],
                             'selected_format': bold_format,
                             'selected_note_type': basic_note_type_details,
                             'selected_source_field': DefaultFields.basic_front,
                             'selected_stop_words': 'to the'}},
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'to the'}}


def test_remember_format(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                         adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                         adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                         all_note_type_details: list[NoteTypeDetails],
                         all_highlight_formats: HighlightFormats,
                         bold_format: HighlightFormat,
                         italic_format: HighlightFormat,
                         adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
                         visual_qtbot: VisualQtBot):
    callback: FakeHighlightControllerCallback = FakeHighlightControllerCallback()
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())
    # Fill model
    adhoc_highlight_dialog_model.note_types = all_note_type_details
    adhoc_highlight_dialog_model.formats = all_highlight_formats
    adhoc_highlight_dialog_model.accept_callback = callback.call
    # Show dialog
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, []), callback.call)
    visual_qtbot.waitExposed(adhoc_highlight_dialog_view)
    assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)
    # Choose "Italic" format
    adhoc_highlight_dialog_view_scaffold.select_2nd_format_combo_box()
    assert_format_group_box(adhoc_highlight_dialog_view, italic_format, all_highlight_formats)
    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    # Show dialog again
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, []), callback.call)
    assert_format_group_box(adhoc_highlight_dialog_view, italic_format, all_highlight_formats)
