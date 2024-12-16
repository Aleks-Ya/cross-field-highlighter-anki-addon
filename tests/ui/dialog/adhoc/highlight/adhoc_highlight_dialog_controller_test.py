from aqt import Qt

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.config.user_folder_storage import UserFolderStorage
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode, \
    HighlightFormats
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames, Text
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model_serde import \
    AdhocHighlightDialogModelSerDe
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from tests.conftest import cloze_note_type_details, bold_format, all_highlight_formats, basic_note_type_details
from tests.data import Data, DefaultFields, DefaultConfig, DefaultTags
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_asserts import assert_format_group_box, \
    FakeModelListener, FakeHighlightControllerCallback, assert_stop_words, assert_space_delimited_language
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_scaffold import AdhocHighlightDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


def test_show_dialog(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                     adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                     adhoc_highlight_dialog_model: AdhocHighlightDialogModel, td: Data,
                     all_note_type_details: list[NoteTypeDetails], all_highlight_formats: HighlightFormats,
                     bold_format: HighlightFormat, basic_note_type_details: NoteTypeDetails,
                     user_folder_storage: UserFolderStorage):
    callback: FakeHighlightControllerCallback = FakeHighlightControllerCallback()
    listener: FakeModelListener = FakeModelListener()
    adhoc_highlight_dialog_model.add_listener(listener)

    td.create_basic_note_1()
    params: DialogParams = DialogParams(all_note_type_details, 1)
    assert callback.history == []
    assert listener.counter == 0
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': DefaultConfig.in_config,
        'note_number': 0,
        'formats': [],
        'note_types': [],
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {},
        'current_state': None}
    assert user_folder_storage.read_all() == {}

    adhoc_highlight_dialog_controller.show_dialog(params, FakeHighlightControllerCallback.call)
    assert callback.history == []
    assert listener.counter == 2
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': DefaultConfig.in_config,
        'note_number': 1,
        'formats': all_highlight_formats,
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {basic_note_type_details.name: {'selected_destination_fields': [],
                                                  'selected_format': bold_format,
                                                  'selected_note_type': basic_note_type_details,
                                                  'selected_source_field': DefaultFields.basic_front,
                                                  'selected_stop_words': DefaultConfig.in_config,
                                                  'space_delimited_language': True}},
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.in_config,
                          'space_delimited_language': True}}
    assert user_folder_storage.read_all() == {}


def test_save_to_storage(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                         adhoc_highlight_dialog_model: AdhocHighlightDialogModel, config_loader: ConfigLoader,
                         basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails,
                         all_note_type_details: list[NoteTypeDetails], bold_format: HighlightFormat,
                         all_highlight_formats: HighlightFormats, user_folder_storage: UserFolderStorage):
    callback: FakeHighlightControllerCallback = FakeHighlightControllerCallback()
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultConfig.highlight}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': DefaultConfig.in_config,
        'note_number': 0,
        'formats': [],
        'note_types': [],
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {},
        'current_state': None}
    assert user_folder_storage.read_all() == {}

    # Update config from model
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    adhoc_highlight_dialog_model.switch_state(basic_note_type_details)
    adhoc_highlight_dialog_model.get_current_state().select_source_field(DefaultFields.basic_front)
    adhoc_highlight_dialog_model.fire_model_changed(None)
    adhoc_highlight_dialog_model.call_accept_callback()
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultConfig.highlight}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': DefaultConfig.in_config,
        'note_number': 0,
        'formats': all_highlight_formats,
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {basic_note_type_details.name: {'selected_destination_fields': [],
                                                  'selected_format': bold_format,
                                                  'selected_note_type': basic_note_type_details,
                                                  'selected_source_field': DefaultFields.basic_front,
                                                  'selected_stop_words': DefaultConfig.in_config,
                                                  'space_delimited_language': True}},
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.in_config,
                          'space_delimited_language': True}}
    assert user_folder_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': basic_note_type_details.name,
             'states': [{'note_type': basic_note_type_details.name,
                         'destination_fields': [],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': 'a an to',
                         'space_delimited_language': True}]}}

    # Update again
    adhoc_highlight_dialog_model.switch_state(cloze_note_type_details)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultConfig.highlight}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': DefaultConfig.in_config,
        'note_number': 0,
        'formats': all_highlight_formats,
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {basic_note_type_details.name: {'selected_destination_fields': [],
                                                  'selected_format': bold_format,
                                                  'selected_note_type': basic_note_type_details,
                                                  'selected_source_field': DefaultFields.basic_front,
                                                  'selected_stop_words': DefaultConfig.in_config,
                                                  'space_delimited_language': True},
                   cloze_note_type_details.name: {'selected_destination_fields': [],
                                                  'selected_format': bold_format,
                                                  'selected_note_type': cloze_note_type_details,
                                                  'selected_source_field': DefaultFields.cloze_text,
                                                  'selected_stop_words': DefaultConfig.in_config,
                                                  'space_delimited_language': True}},
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': cloze_note_type_details,
                          'selected_source_field': DefaultFields.cloze_text,
                          'selected_stop_words': DefaultConfig.in_config,
                          'space_delimited_language': True}}
    assert user_folder_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': basic_note_type_details.name,
             'states': [{'note_type': basic_note_type_details.name,
                         'destination_fields': [],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': 'a an to',
                         'space_delimited_language': True}]}}


def test_fill_model_from_config_on_startup(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                           adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                           adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe,
                                           note_type_details_factory: NoteTypeDetailsFactory,
                                           config_loader: ConfigLoader, user_folder_storage: UserFolderStorage,
                                           basic_note_type_details: NoteTypeDetails,
                                           cloze_note_type_details: NoteTypeDetails,
                                           formatter_facade: FormatterFacade,
                                           all_note_type_details: list[NoteTypeDetails],
                                           all_highlight_formats: HighlightFormats, bold_format: HighlightFormat):
    callback: FakeHighlightControllerCallback = FakeHighlightControllerCallback()
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultConfig.highlight}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': DefaultConfig.in_config,
        'note_number': 0,
        'formats': [],
        'note_types': [],
        'accept_callback_None': True,
        'reject_callback_None': True,
        'states': {},
        'current_state': None}
    assert user_folder_storage.read_all() == {}

    # Update config from model
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    adhoc_highlight_dialog_model.switch_state(basic_note_type_details)
    adhoc_highlight_dialog_model.get_current_state().select_source_field(DefaultFields.basic_front)
    adhoc_highlight_dialog_model.get_current_state().select_format(formatter_facade.get_format_by_code(
        HighlightFormatCode.BOLD))
    adhoc_highlight_dialog_model.get_current_state().set_stop_words(Text("to the"))
    adhoc_highlight_dialog_model.get_current_state().select_destination_fields(FieldNames(
        [DefaultFields.basic_back]))
    adhoc_highlight_dialog_model.fire_model_changed(None)
    adhoc_highlight_dialog_model.call_accept_callback()
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultConfig.highlight}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_highlight_dialog_model.as_dict() == {
        'default_stop_words': DefaultConfig.in_config,
        'note_number': 0,
        'formats': all_highlight_formats,
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {basic_note_type_details.name: {'selected_destination_fields': [DefaultFields.basic_back],
                                                  'selected_format': bold_format,
                                                  'selected_note_type': basic_note_type_details,
                                                  'selected_source_field': DefaultFields.basic_front,
                                                  'selected_stop_words': 'to the',
                                                  'space_delimited_language': True}},
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'to the',
                          'space_delimited_language': True}}
    assert user_folder_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': basic_note_type_details.name,
             'states': [{'note_type': basic_note_type_details.name,
                         'destination_fields': [DefaultFields.basic_back],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': 'to the',
                         'space_delimited_language': True}]}}

    # Initialize controller using saved config
    config: Config = config_loader.load_config()
    model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    view: AdhocHighlightDialogView = AdhocHighlightDialogView(model)
    controller: AdhocHighlightDialogController = AdhocHighlightDialogController(
        model, view, note_type_details_factory, formatter_facade, adhoc_highlight_dialog_model_serde, config,
        user_folder_storage)
    controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultConfig.highlight}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert model.as_dict() == {
        'default_stop_words': DefaultConfig.in_config,
        'note_number': 0,
        'formats': all_highlight_formats,
        'note_types': all_note_type_details,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {basic_note_type_details.name: {'selected_destination_fields': [DefaultFields.basic_back],
                                                  'selected_format': bold_format,
                                                  'selected_note_type': basic_note_type_details,
                                                  'selected_source_field': DefaultFields.basic_front,
                                                  'selected_stop_words': 'to the',
                                                  'space_delimited_language': True}},
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back],
                          'selected_format': bold_format,
                          'selected_note_type': basic_note_type_details,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'to the',
                          'space_delimited_language': True}}
    assert user_folder_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': basic_note_type_details.name,
             'states': [{'note_type': basic_note_type_details.name,
                         'destination_fields': [DefaultFields.basic_back],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': 'to the',
                         'space_delimited_language': True}]}}


def test_remember_format_on_cancel(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
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
    # Show dialog
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert_format_group_box(adhoc_highlight_dialog_view, bold_format, all_highlight_formats)
    # Choose "Italic" format
    adhoc_highlight_dialog_view_scaffold.select_format(Qt.Key.Key_Down)
    assert_format_group_box(adhoc_highlight_dialog_view, italic_format, all_highlight_formats)
    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    # Show dialog again
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    assert_format_group_box(adhoc_highlight_dialog_view, italic_format, all_highlight_formats)


def test_remember_stop_words_on_cancel(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
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
    # Show dialog
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert_stop_words(adhoc_highlight_dialog_view, DefaultConfig.in_config)
    # Modify stop words
    appended_stop_words: str = " the"
    exp_stop_words: str = DefaultConfig.in_config + appended_stop_words
    adhoc_highlight_dialog_view_scaffold.print_to_stop_words(appended_stop_words)
    assert_stop_words(adhoc_highlight_dialog_view, exp_stop_words)
    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    # Show dialog again
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    assert_stop_words(adhoc_highlight_dialog_view, exp_stop_words)


def test_remember_space_delimited_language_on_cancel(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                                     adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                                     adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                                     all_note_type_details: list[NoteTypeDetails],
                                                     adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
                                                     visual_qtbot: VisualQtBot):
    callback: FakeHighlightControllerCallback = FakeHighlightControllerCallback()
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())
    # Show dialog
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert_space_delimited_language(adhoc_highlight_dialog_view, True)
    # Uncheck space-delimited language combobox
    adhoc_highlight_dialog_view_scaffold.click_space_delimited_language()
    assert_space_delimited_language(adhoc_highlight_dialog_view, False)
    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    # Show dialog again
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    assert_space_delimited_language(adhoc_highlight_dialog_view, False)
