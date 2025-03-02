from aqt import Qt

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.config.settings import Settings
from cross_field_highlighter.config.user_files_storage import UserFilesStorage
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
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from tests.conftest import note_type_details_cloze, bold_format, all_highlight_formats, note_type_details_basic
from tests.data import Data, DefaultFields, DefaultConfig, DefaultModel
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_asserts import HighlightFakeModelListener, \
    FakeHighlightControllerCallback, assert_view
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_scaffold import AdhocHighlightDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


def test_show_dialog(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                     adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                     adhoc_highlight_dialog_model: AdhocHighlightDialogModel, td: Data,
                     note_type_details_all: list[NoteTypeDetails], all_highlight_formats: HighlightFormats,
                     bold_format: HighlightFormat, note_type_details_basic: NoteTypeDetails,
                     user_files_storage: UserFilesStorage, highlight_model_listener: HighlightFakeModelListener,
                     highlight_controller_callback: FakeHighlightControllerCallback):
    # Default data
    td.create_basic_note_1()
    params: DialogParams = DialogParams(note_type_details_all, 1)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 0
    assert adhoc_highlight_dialog_model.as_dict() == DefaultModel.default_highlight
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)

    adhoc_highlight_dialog_controller.show_dialog(params, highlight_controller_callback.call)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 1
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}},
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words, }}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)


def test_save_to_storage(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                         adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                         adhoc_highlight_dialog_model: AdhocHighlightDialogModel, config_loader: ConfigLoader,
                         note_type_details_basic: NoteTypeDetails, note_type_details_cloze: NoteTypeDetails,
                         note_type_details_all: list[NoteTypeDetails], bold_format: HighlightFormat,
                         all_highlight_formats: HighlightFormats, user_files_storage: UserFilesStorage,
                         highlight_controller_callback: FakeHighlightControllerCallback):
    # Assert default config and model
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == DefaultModel.default_highlight
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)

    # Update config from model
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(note_type_details_all, 0),
                                                  highlight_controller_callback.call)
    adhoc_highlight_dialog_model.call_accept_callback()  # Click "Start" button
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 0,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}},
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words, }}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': 'a an to'}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 0 notes",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)

    # Update again
    adhoc_highlight_dialog_model.switch_state(note_type_details_cloze)
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 0,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_cloze,
                          'selected_source_field': DefaultFields.cloze_text,
                          'selected_stop_words': DefaultConfig.default_stop_words, },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_text,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': 'a an to'}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 0 notes",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)


def test_fill_model_from_config_on_startup(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                           adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                           adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                           adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe,
                                           note_type_details_factory: NoteTypeDetailsFactory,
                                           config_loader: ConfigLoader, user_files_storage: UserFilesStorage,
                                           note_type_details_basic: NoteTypeDetails,
                                           note_type_details_cloze: NoteTypeDetails,
                                           formatter_facade: FormatterFacade,
                                           note_type_details_all: list[NoteTypeDetails],
                                           all_highlight_formats: HighlightFormats, bold_format: HighlightFormat,
                                           settings: Settings,
                                           highlight_controller_callback: FakeHighlightControllerCallback):
    # Assert default config and model
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == DefaultModel.default_highlight
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)

    # Update config from model
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(note_type_details_all, 0),
                                                  highlight_controller_callback.call)
    adhoc_highlight_dialog_model.switch_state(note_type_details_basic)
    adhoc_highlight_dialog_model.get_current_state().select_source_field(DefaultFields.basic_front)
    adhoc_highlight_dialog_model.get_current_state().select_format(formatter_facade.get_format_by_code(
        HighlightFormatCode.BOLD))
    adhoc_highlight_dialog_model.get_current_state().set_stop_words(Text("to the"))
    adhoc_highlight_dialog_model.get_current_state().select_destination_fields(FieldNames(
        [DefaultFields.basic_back]))
    adhoc_highlight_dialog_model.fire_model_changed(None)
    adhoc_highlight_dialog_model.call_accept_callback()  # Click "Start" button
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 0,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'to the', },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [DefaultFields.basic_back],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': 'to the'}}}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [DefaultFields.basic_back],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': 'to the'}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 0 notes",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[DefaultFields.basic_back], disabled_fields=[DefaultFields.basic_front],
                stop_words='to the')

    # Initialize controller using saved config
    config: Config = Config(config_loader)
    model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    view: AdhocHighlightDialogView = AdhocHighlightDialogView(model, settings)
    controller: AdhocHighlightDialogController = AdhocHighlightDialogController(
        model, view, note_type_details_factory, formatter_facade, adhoc_highlight_dialog_model_serde, config,
        user_files_storage)
    controller.show_dialog(DialogParams(note_type_details_all, 0), highlight_controller_callback.call)
    assert config_loader.load_config() == DefaultConfig.loader
    assert model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 0,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': 'to the', },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [DefaultFields.basic_back],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': 'to the'}}}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [DefaultFields.basic_back],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': 'to the'}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 0 notes",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[DefaultFields.basic_back], disabled_fields=[DefaultFields.basic_front],
                stop_words='to the')


def test_remember_state_on_cancel_click(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                        adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                        adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                        note_type_details_all: list[NoteTypeDetails],
                                        all_highlight_formats: HighlightFormats,
                                        bold_format: HighlightFormat, italic_format: HighlightFormat,
                                        adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
                                        user_files_storage: UserFilesStorage, config_loader: ConfigLoader,
                                        note_type_details_basic: NoteTypeDetails,
                                        highlight_controller_callback: FakeHighlightControllerCallback,
                                        visual_qtbot: VisualQtBot):
    # Default state
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == DefaultModel.default_highlight
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)

    # Show dialog
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(note_type_details_all, 0),
                                                  highlight_controller_callback.call)
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 0,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 0 notes",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)

    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 0,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': DefaultConfig.default_stop_words}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 0 notes",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)


def test_remember_state_on_cancel_esc_shortcut(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                               adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                               adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                               note_type_details_all: list[NoteTypeDetails],
                                               all_highlight_formats: HighlightFormats,
                                               bold_format: HighlightFormat, italic_format: HighlightFormat,
                                               adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
                                               user_files_storage: UserFilesStorage, config_loader: ConfigLoader,
                                               note_type_details_basic: NoteTypeDetails,
                                               highlight_controller_callback: FakeHighlightControllerCallback,
                                               visual_qtbot: VisualQtBot):
    # Default state
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == DefaultModel.default_highlight
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)

    # Show dialog
    adhoc_highlight_dialog_controller.show_dialog(DialogParams(note_type_details_all, 0),
                                                  highlight_controller_callback.call)
    visual_qtbot.wait_exposed(adhoc_highlight_dialog_view)
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 0,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 0 notes",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)

    # Click Cancel button
    adhoc_highlight_dialog_view_scaffold.press_esc()
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 0,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words},
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': DefaultConfig.default_stop_words}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 0 notes",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)


def test_exclude_source_field_from_destination_fields(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                                      adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                                      adhoc_highlight_dialog_model: AdhocHighlightDialogModel, td: Data,
                                                      adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
                                                      note_type_details_all: list[NoteTypeDetails],
                                                      all_highlight_formats: HighlightFormats,
                                                      bold_format: HighlightFormat,
                                                      note_type_details_basic: NoteTypeDetails,
                                                      user_files_storage: UserFilesStorage,
                                                      highlight_model_listener: HighlightFakeModelListener,
                                                      highlight_controller_callback: FakeHighlightControllerCallback):
    # Initial state
    td.create_basic_note_1()
    params: DialogParams = DialogParams(note_type_details_all, 1)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 0
    assert adhoc_highlight_dialog_model.as_dict() == DefaultModel.default_highlight
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)

    # Show dialog
    adhoc_highlight_dialog_controller.show_dialog(params, highlight_controller_callback.call)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 1
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words, },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)

    # Mark destination field
    adhoc_highlight_dialog_view_scaffold.mark_destination_field(DefaultFields.basic_back)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 2
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words, },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [DefaultFields.basic_back],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[DefaultFields.basic_back], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)

    # Select marked destination field as source field (should be excluded from HighlightOpParams)
    adhoc_highlight_dialog_view_scaffold.select_source_field(Qt.Key.Key_Down)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 3
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_back,
                          'selected_stop_words': DefaultConfig.default_stop_words, },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [DefaultFields.basic_back],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_back,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_back, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[DefaultFields.basic_back], disabled_fields=[DefaultFields.basic_back],
                stop_words=DefaultConfig.default_stop_words)

    # Mark another destination field
    adhoc_highlight_dialog_view_scaffold.mark_destination_field(DefaultFields.basic_extra)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 4
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back, DefaultFields.basic_extra],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_back,
                          'selected_stop_words': DefaultConfig.default_stop_words, },
        'states': {note_type_details_basic.note_type_id: {
            'selected_destination_fields': [DefaultFields.basic_back, DefaultFields.basic_extra],
            'selected_format': bold_format,
            'selected_note_type': note_type_details_basic,
            'selected_source_field': DefaultFields.basic_back,
            'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_back, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[DefaultFields.basic_back, DefaultFields.basic_extra],
                disabled_fields=[DefaultFields.basic_back], stop_words=DefaultConfig.default_stop_words, )

    # Click Start
    adhoc_highlight_dialog_view_scaffold.click_start_button()
    assert highlight_controller_callback.history == [HighlightOpParams(
        note_type_details_basic.note_type_id, DefaultFields.basic_back, FieldNames([DefaultFields.basic_extra]),
        Text(DefaultConfig.default_stop_words), bold_format)]
    assert highlight_model_listener.counter == 4
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [DefaultFields.basic_back, DefaultFields.basic_extra],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_back,
                          'selected_stop_words': DefaultConfig.default_stop_words},
        'states': {note_type_details_basic.note_type_id: {
            'selected_destination_fields': [DefaultFields.basic_back, DefaultFields.basic_extra],
            'selected_format': bold_format,
            'selected_note_type': note_type_details_basic,
            'selected_source_field': DefaultFields.basic_back,
            'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [DefaultFields.basic_back, DefaultFields.basic_extra],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_back,
                         'stop_words': DefaultConfig.default_stop_words}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_basic, note_types=note_type_details_all,
                selected_source_field=DefaultFields.basic_back, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[DefaultFields.basic_back, DefaultFields.basic_extra],
                disabled_fields=[DefaultFields.basic_back], stop_words=DefaultConfig.default_stop_words)


def test_empty_note_type(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                         adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                         adhoc_highlight_dialog_model: AdhocHighlightDialogModel, td: Data,
                         adhoc_highlight_dialog_view_scaffold: AdhocHighlightDialogViewScaffold,
                         note_type_details_all: list[NoteTypeDetails], all_highlight_formats: HighlightFormats,
                         bold_format: HighlightFormat, note_type_details_basic: NoteTypeDetails,
                         note_type_details_cloze: NoteTypeDetails, user_files_storage: UserFilesStorage,
                         highlight_model_listener: HighlightFakeModelListener,
                         highlight_controller_callback: FakeHighlightControllerCallback):
    td.create_basic_note_1()
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 0
    assert adhoc_highlight_dialog_model.as_dict() == DefaultModel.default_highlight
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)

    # Show dialog for Basic note type
    adhoc_highlight_dialog_controller.show_dialog(DialogParams([note_type_details_basic], 1),
                                                  highlight_controller_callback.call)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 1
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': [note_type_details_basic],
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words, },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_basic, note_types=[note_type_details_basic],
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)

    # Click Cancel
    adhoc_highlight_dialog_view_scaffold.click_cancel_button()
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 1
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': [note_type_details_basic],
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_basic,
                          'selected_source_field': DefaultFields.basic_front,
                          'selected_stop_words': DefaultConfig.default_stop_words, },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': DefaultConfig.default_stop_words}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_basic, note_types=[note_type_details_basic],
                selected_source_field=DefaultFields.basic_front, source_fields=DefaultFields.all_basic,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_basic,
                selected_destination_fields=[], disabled_fields=[DefaultFields.basic_front],
                stop_words=DefaultConfig.default_stop_words)

    # Show dialog for Cloze note type
    adhoc_highlight_dialog_controller.show_dialog(DialogParams([note_type_details_cloze], 1),
                                                  highlight_controller_callback.call)
    assert highlight_controller_callback.history == []
    assert highlight_model_listener.counter == 2
    assert adhoc_highlight_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': [note_type_details_cloze],
        'default_stop_words': DefaultConfig.default_stop_words,
        'note_number': 1,
        'formats': all_highlight_formats,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_destination_fields': [],
                          'selected_format': bold_format,
                          'selected_note_type': note_type_details_cloze,
                          'selected_source_field': DefaultFields.cloze_text,
                          'selected_stop_words': DefaultConfig.default_stop_words, },
        'states': {note_type_details_basic.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_basic,
                                                          'selected_source_field': DefaultFields.basic_front,
                                                          'selected_stop_words': DefaultConfig.default_stop_words},
                   note_type_details_cloze.note_type_id: {'selected_destination_fields': [],
                                                          'selected_format': bold_format,
                                                          'selected_note_type': note_type_details_cloze,
                                                          'selected_source_field': DefaultFields.cloze_text,
                                                          'selected_stop_words': DefaultConfig.default_stop_words}}}
    assert user_files_storage.read_all() == {
        'highlight_dialog_states':
            {'current_state': note_type_details_basic.note_type_id,
             'states': [{'note_type_id': note_type_details_basic.note_type_id,
                         'destination_fields': [],
                         'format': bold_format.code.name,
                         'source_field': DefaultFields.basic_front,
                         'stop_words': DefaultConfig.default_stop_words}]}}
    assert_view(adhoc_highlight_dialog_view, window_title="Highlight 1 note",
                selected_note_type=note_type_details_cloze, note_types=[note_type_details_cloze],
                selected_source_field=DefaultFields.cloze_text, source_fields=DefaultFields.all_cloze,
                selected_format=bold_format, formats=all_highlight_formats, check_box_texts=DefaultFields.all_cloze,
                selected_destination_fields=[], disabled_fields=[DefaultFields.cloze_text],
                stop_words=DefaultConfig.default_stop_words)


def test_no_notes_selected(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                           adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                           all_highlight_formats: HighlightFormats,
                           bold_format: HighlightFormat, note_type_details_basic: NoteTypeDetails,
                           user_files_storage: UserFilesStorage,
                           highlight_controller_callback: FakeHighlightControllerCallback):
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)

    params: DialogParams = DialogParams([], 1)
    adhoc_highlight_dialog_controller.show_dialog(params, highlight_controller_callback.call)
    assert_view(adhoc_highlight_dialog_view, window_title="", selected_note_type=None, note_types=[],
                selected_source_field="", source_fields=[], selected_format=None, formats=[], check_box_texts=[],
                selected_destination_fields=[], disabled_fields=[], stop_words=DefaultConfig.default_stop_words)
