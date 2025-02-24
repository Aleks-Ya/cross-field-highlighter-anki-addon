from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.config.settings import Settings
from cross_field_highlighter.config.user_files_storage import UserFilesStorage
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from tests.conftest import note_type_details_cloze, note_type_details_basic
from tests.data import Data, DefaultFields, DefaultConfig, DefaultModel
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_asserts import EraseFakeModelListener, \
    FakeEraseControllerCallback, assert_view
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_scaffold import AdhocEraseDialogViewScaffold


def test_show_dialog(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                     adhoc_erase_dialog_view: AdhocEraseDialogView,
                     adhoc_erase_dialog_model: AdhocEraseDialogModel, td: Data,
                     note_type_details_basic: NoteTypeDetails,
                     note_type_details_all: list[NoteTypeDetails], user_files_storage: UserFilesStorage,
                     erase_model_listener: EraseFakeModelListener,
                     erase_controller_callback: FakeEraseControllerCallback):
    # Default state
    params: DialogParams = DialogParams(note_type_details_all, 0)
    assert erase_controller_callback.history == []
    assert erase_model_listener.history == []
    assert adhoc_erase_dialog_model.as_dict() == DefaultModel.default_erase
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_erase_dialog_view, window_title="", selected_note_type=None, all_fields=[], selected_fields=[])

    adhoc_erase_dialog_controller.show_dialog(params, erase_controller_callback.call)
    assert erase_controller_callback.history == []
    assert len(erase_model_listener.history) == 1
    assert adhoc_erase_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 0,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': note_type_details_basic},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_erase_dialog_view, window_title="Erase 0 notes", selected_note_type=note_type_details_basic,
                all_fields=DefaultFields.all_basic, selected_fields=[])


def test_update_config(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                       adhoc_erase_dialog_view: AdhocEraseDialogView,
                       adhoc_erase_dialog_model: AdhocEraseDialogModel, config_loader: ConfigLoader,
                       note_type_details_basic: NoteTypeDetails, note_type_details_cloze: NoteTypeDetails,
                       note_type_details_all: list[NoteTypeDetails], user_files_storage: UserFilesStorage,
                       erase_controller_callback: FakeEraseControllerCallback):
    # Default config and model
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == DefaultModel.default_erase
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_erase_dialog_view, window_title="", selected_note_type=None,
                all_fields=[], selected_fields=[])

    # Update config from model
    adhoc_erase_dialog_controller.show_dialog(DialogParams(note_type_details_all, 0), erase_controller_callback.call)
    adhoc_erase_dialog_model.call_accept_callback()
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 0,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': note_type_details_basic},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic}}}
    assert user_files_storage.read_all() == {'erase_dialog_states': {
        'current_state': note_type_details_basic.note_type_id,
        'states': [{'note_type_id': note_type_details_basic.note_type_id, 'fields': []}]}}
    assert_view(adhoc_erase_dialog_view, window_title="Erase 0 notes", selected_note_type=note_type_details_basic,
                all_fields=DefaultFields.all_basic, selected_fields=[])

    # Update again
    adhoc_erase_dialog_model.switch_state(note_type_details_cloze)
    adhoc_erase_dialog_model.fire_model_changed(None)
    assert adhoc_erase_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 0,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': note_type_details_cloze},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic},
                   note_type_details_cloze.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_cloze}}}
    assert user_files_storage.read_all() == {'erase_dialog_states': {
        'current_state': note_type_details_basic.note_type_id,
        'states': [{'note_type_id': note_type_details_basic.note_type_id, 'fields': []}]}}
    assert_view(adhoc_erase_dialog_view, window_title="Erase 0 notes", selected_note_type=note_type_details_cloze,
                all_fields=DefaultFields.all_cloze, selected_fields=[])


def test_fill_model_from_storage_on_startup(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                                            adhoc_erase_dialog_view: AdhocEraseDialogView,
                                            adhoc_erase_dialog_model: AdhocEraseDialogModel,
                                            config_loader: ConfigLoader,
                                            note_type_details_basic: NoteTypeDetails,
                                            note_type_details_cloze: NoteTypeDetails,
                                            note_type_details_factory: NoteTypeDetailsFactory,
                                            note_type_details_all: list[NoteTypeDetails],
                                            adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe,
                                            user_files_storage: UserFilesStorage,
                                            settings: Settings,
                                            erase_controller_callback: FakeEraseControllerCallback):
    # Default config and model
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == DefaultModel.default_erase
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_erase_dialog_view, window_title="", selected_note_type=None,
                all_fields=[], selected_fields=[])

    # Show dialog
    adhoc_erase_dialog_controller.show_dialog(DialogParams(note_type_details_all, 5), erase_controller_callback.call)
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'accept_callback_None': False,
        'selected_note_types': note_type_details_all,
        'note_number': 5,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': note_type_details_basic},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_erase_dialog_view, window_title="Erase 5 notes", selected_note_type=note_type_details_basic,
                all_fields=DefaultFields.all_basic, selected_fields=[])

    # Update config from model
    adhoc_erase_dialog_model.switch_state(note_type_details_cloze)
    adhoc_erase_dialog_model.get_current_state().select_fields(FieldNames([DefaultFields.cloze_back_extra]))
    adhoc_erase_dialog_model.fire_model_changed(None)
    adhoc_erase_dialog_model.call_accept_callback()
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'accept_callback_None': False,
        'selected_note_types': note_type_details_all,
        'note_number': 5,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [DefaultFields.cloze_back_extra],
                          'selected_note_type': note_type_details_cloze},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic},
                   note_type_details_cloze.note_type_id: {'selected_fields': [DefaultFields.cloze_back_extra],
                                                          'selected_note_type': note_type_details_cloze}}}
    assert user_files_storage.read_all() == {'erase_dialog_states': {
        'current_state': note_type_details_cloze.note_type_id,
        'states': [{'note_type_id': note_type_details_basic.note_type_id, 'fields': []},
                   {'note_type_id': note_type_details_cloze.note_type_id, 'fields': [DefaultFields.cloze_back_extra]}]}}
    assert_view(adhoc_erase_dialog_view, window_title="Erase 5 notes", selected_note_type=note_type_details_cloze,
                all_fields=DefaultFields.all_cloze, selected_fields=[DefaultFields.cloze_back_extra])

    # Initialize controller using saved config
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    view: AdhocEraseDialogView = AdhocEraseDialogView(model, settings)
    controller: AdhocEraseDialogController = AdhocEraseDialogController(
        model, view, note_type_details_factory, adhoc_erase_dialog_model_serde, user_files_storage)
    assert config_loader.load_config() == DefaultConfig.loader
    assert model.as_dict() == DefaultModel.default_erase
    assert user_files_storage.read_all() == {'erase_dialog_states': {
        'current_state': note_type_details_cloze.note_type_id,
        'states': [{'note_type_id': note_type_details_basic.note_type_id, 'fields': []},
                   {'note_type_id': note_type_details_cloze.note_type_id, 'fields': [DefaultFields.cloze_back_extra]}]}}
    assert_view(view, window_title="", selected_note_type=None, all_fields=[], selected_fields=[])

    # Show dialog (will read state from storage)
    params: DialogParams = DialogParams(note_type_details_all, 6)
    controller.show_dialog(params, erase_controller_callback.call)
    assert model.as_dict() == {
        'all_note_types': note_type_details_all,
        'selected_note_types': note_type_details_all,
        'note_number': 6,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [DefaultFields.cloze_back_extra],
                          'selected_note_type': note_type_details_cloze},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic},
                   note_type_details_cloze.note_type_id: {'selected_fields': [DefaultFields.cloze_back_extra],
                                                          'selected_note_type': note_type_details_cloze}}}
    assert user_files_storage.read_all() == {'erase_dialog_states': {
        'current_state': note_type_details_cloze.note_type_id,
        'states': [{'note_type_id': note_type_details_basic.note_type_id, 'fields': []},
                   {'note_type_id': note_type_details_cloze.note_type_id, 'fields': [DefaultFields.cloze_back_extra]}]}}
    assert_view(view, window_title="Erase 6 notes", selected_note_type=note_type_details_cloze,
                all_fields=DefaultFields.all_cloze, selected_fields=[DefaultFields.cloze_back_extra])


# Select NoteType which yet doesn't have a state
def test_empty_note_type(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                         adhoc_erase_dialog_model: AdhocEraseDialogModel,
                         adhoc_erase_dialog_view: AdhocEraseDialogView, config_loader: ConfigLoader,
                         note_type_details_basic: NoteTypeDetails, note_type_details_cloze: NoteTypeDetails,
                         note_type_details_factory: NoteTypeDetailsFactory,
                         note_type_details_all: list[NoteTypeDetails],
                         adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe,
                         user_files_storage: UserFilesStorage,
                         adhoc_erase_dialog_view_scaffold: AdhocEraseDialogViewScaffold,
                         erase_controller_callback: FakeEraseControllerCallback):
    # Default config and model
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == DefaultModel.default_erase
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_erase_dialog_view, window_title="", selected_note_type=None, all_fields=[], selected_fields=[])

    # Show dialog with Basic note type
    adhoc_erase_dialog_controller.show_dialog(DialogParams([note_type_details_basic], 1),
                                              erase_controller_callback.call)
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'accept_callback_None': False,
        'selected_note_types': [note_type_details_basic],
        'note_number': 1,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': note_type_details_basic},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic}}}
    assert user_files_storage.read_all() == {}
    assert_view(adhoc_erase_dialog_view, window_title="Erase 1 note", selected_note_type=note_type_details_basic,
                all_fields=DefaultFields.all_basic, selected_fields=[])

    # Close Dialog (click Cancel)
    adhoc_erase_dialog_view_scaffold.click_cancel_button()
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'accept_callback_None': False,
        'selected_note_types': [note_type_details_basic],
        'note_number': 1,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': note_type_details_basic},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic}}}
    assert user_files_storage.read_all() == {'erase_dialog_states': {
        'current_state': note_type_details_basic.note_type_id,
        'states': [{'note_type_id': note_type_details_basic.note_type_id, 'fields': []}]}}
    assert_view(adhoc_erase_dialog_view, window_title="Erase 1 note", selected_note_type=note_type_details_basic,
                all_fields=DefaultFields.all_basic, selected_fields=[])

    # Show Dialog with Cloze note type (it does not have a state yet)
    adhoc_erase_dialog_controller.show_dialog(DialogParams([note_type_details_cloze], 1),
                                              erase_controller_callback.call)
    assert config_loader.load_config() == DefaultConfig.loader
    assert adhoc_erase_dialog_model.as_dict() == {
        'all_note_types': note_type_details_all,
        'accept_callback_None': False,
        'selected_note_types': [note_type_details_cloze],
        'note_number': 1,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': note_type_details_cloze},
        'states': {note_type_details_basic.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_basic},
                   note_type_details_cloze.note_type_id: {'selected_fields': [],
                                                          'selected_note_type': note_type_details_cloze}}}
    assert user_files_storage.read_all() == {'erase_dialog_states': {
        'current_state': note_type_details_basic.note_type_id,
        'states': [{'note_type_id': note_type_details_basic.note_type_id, 'fields': []}]}}
    assert_view(adhoc_erase_dialog_view, window_title="Erase 1 note", selected_note_type=note_type_details_cloze,
                all_fields=DefaultFields.all_cloze, selected_fields=[])


def test_no_notes_selected(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                           adhoc_erase_dialog_view: AdhocEraseDialogView,
                           erase_controller_callback: FakeEraseControllerCallback):
    assert_view(adhoc_erase_dialog_view, window_title="", selected_note_type=None, all_fields=[], selected_fields=[])
    params: DialogParams = DialogParams([], 1)
    adhoc_erase_dialog_controller.show_dialog(params, erase_controller_callback.call)
    assert_view(adhoc_erase_dialog_view, window_title="", selected_note_type=None, all_fields=[], selected_fields=[])
