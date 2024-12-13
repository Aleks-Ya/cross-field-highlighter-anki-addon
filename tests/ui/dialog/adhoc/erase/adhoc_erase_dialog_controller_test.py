from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.config.user_folder_storage import UserFolderStorage
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from tests.conftest import cloze_note_type_details, basic_note_type_details
from tests.data import Data, DefaultFields, DefaultStopWords, DefaultTags
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_asserts import FakeModelListener, FakeEraseControllerCallback


def test_show_dialog(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                     adhoc_erase_dialog_view: AdhocEraseDialogView,
                     adhoc_erase_dialog_model: AdhocEraseDialogModel, td: Data,
                     basic_note_type_details: NoteTypeDetails,
                     all_note_type_details: list[NoteTypeDetails], user_folder_storage: UserFolderStorage):
    listener: FakeModelListener = FakeModelListener()
    adhoc_erase_dialog_model.add_listener(listener)

    params: DialogParams = DialogParams(all_note_type_details, 0)
    callback: FakeEraseControllerCallback = FakeEraseControllerCallback()
    assert callback.history == []
    assert listener.history == []
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'note_number': 0,
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}
    assert user_folder_storage.read_all() == {}

    adhoc_erase_dialog_controller.show_dialog(params, FakeEraseControllerCallback.call)
    assert callback.history == []
    assert len(listener.history) == 1
    assert adhoc_erase_dialog_model.as_dict() == {
        'note_types': all_note_type_details,
        'note_number': 0,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': basic_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details}}}
    assert user_folder_storage.read_all() == {}


def test_update_config(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                       adhoc_erase_dialog_model: AdhocEraseDialogModel, config_loader: ConfigLoader,
                       basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails,
                       all_note_type_details: list[NoteTypeDetails], user_folder_storage: UserFolderStorage):
    callback: FakeEraseControllerCallback = FakeEraseControllerCallback()
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultStopWords.config}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'note_number': 0,
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}
    assert user_folder_storage.read_all() == {}

    # Update config from model
    adhoc_erase_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    adhoc_erase_dialog_model.call_accept_callback()
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultStopWords.config}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_erase_dialog_model.as_dict() == {
        'note_types': all_note_type_details,
        'note_number': 0,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': basic_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details}}}
    assert user_folder_storage.read_all() == {'erase_dialog_states': {
        'current_state': basic_note_type_details.name,
        'states': [{'note_type': basic_note_type_details.name, 'fields': []}]}}

    # Update again
    adhoc_erase_dialog_model.switch_state(cloze_note_type_details)
    adhoc_erase_dialog_model.fire_model_changed(None)
    assert adhoc_erase_dialog_model.as_dict() == {
        'note_types': all_note_type_details,
        'note_number': 0,
        'accept_callback_None': False,
        'reject_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': cloze_note_type_details},
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details},
                   cloze_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': cloze_note_type_details}}}
    assert user_folder_storage.read_all() == {'erase_dialog_states': {
        'current_state': basic_note_type_details.name,
        'states': [{'note_type': basic_note_type_details.name, 'fields': []}]}}


def test_fill_model_from_storage_on_startup(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                                            adhoc_erase_dialog_model: AdhocEraseDialogModel,
                                            config_loader: ConfigLoader,
                                            basic_note_type_details: NoteTypeDetails,
                                            cloze_note_type_details: NoteTypeDetails,
                                            note_type_details_factory: NoteTypeDetailsFactory,
                                            all_note_type_details: list[NoteTypeDetails],
                                            adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe,
                                            user_folder_storage: UserFolderStorage):
    callback: FakeEraseControllerCallback = FakeEraseControllerCallback()
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultStopWords.config}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'note_number': 0,
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}
    assert user_folder_storage.read_all() == {}

    # Show dialog
    adhoc_erase_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultStopWords.config}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_erase_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_fields': [],
                          'selected_note_type': basic_note_type_details},
        'note_types': all_note_type_details,
        'note_number': 0,
        'reject_callback_None': False,
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details}}}
    assert user_folder_storage.read_all() == {}

    # Update config from model
    adhoc_erase_dialog_model.switch_state(cloze_note_type_details)
    adhoc_erase_dialog_model.get_current_state().select_fields(FieldNames([DefaultFields.cloze_back_extra]))
    adhoc_erase_dialog_model.fire_model_changed(None)
    adhoc_erase_dialog_model.call_accept_callback()
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultStopWords.config}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert adhoc_erase_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_fields': [DefaultFields.cloze_back_extra],
                          'selected_note_type': cloze_note_type_details},
        'note_types': all_note_type_details,
        'note_number': 0,
        'reject_callback_None': False,
        'states': {basic_note_type_details.name: {'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details},
                   cloze_note_type_details.name: {'selected_fields': [DefaultFields.cloze_back_extra],
                                                  'selected_note_type': cloze_note_type_details}}}
    assert user_folder_storage.read_all() == {'erase_dialog_states': {
        'current_state': cloze_note_type_details.name,
        'states': [{'note_type': basic_note_type_details.name, 'fields': []},
                   {'note_type': cloze_note_type_details.name, 'fields': [DefaultFields.cloze_back_extra]}]}}

    # Initialize controller using saved config
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    view: AdhocEraseDialogView = AdhocEraseDialogView(model)
    _: AdhocEraseDialogController = AdhocEraseDialogController(
        model, view, note_type_details_factory, adhoc_erase_dialog_model_serde, user_folder_storage)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {'Highlight': {**DefaultStopWords.config}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert model.as_dict() == {'note_types': [],
                               'note_number': 0,
                               'accept_callback_None': True,
                               'reject_callback_None': True,
                               'current_state': None,
                               'states': {}}
    assert user_folder_storage.read_all() == {'erase_dialog_states': {
        'current_state': cloze_note_type_details.name,
        'states': [{'note_type': basic_note_type_details.name, 'fields': []},
                   {'note_type': cloze_note_type_details.name, 'fields': [DefaultFields.cloze_back_extra]}]}}
