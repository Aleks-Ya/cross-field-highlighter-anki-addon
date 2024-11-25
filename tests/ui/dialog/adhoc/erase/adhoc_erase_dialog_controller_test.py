from anki.notes import Note, NoteId

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from tests.conftest import cloze_note_type_details, basic_note_type_details
from tests.data import Data, DefaultFields
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_asserts import FakeModelListener, FakeEraseControllerCallback


def test_show_dialog(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                     adhoc_erase_dialog_view: AdhocEraseDialogView,
                     adhoc_erase_dialog_model: AdhocEraseDialogModel, td: Data,
                     basic_note_type_details: NoteTypeDetails,
                     all_note_type_details: list[NoteTypeDetails]):
    listener: FakeModelListener = FakeModelListener()
    adhoc_erase_dialog_model.add_listener(listener)

    note_1: Note = td.create_basic_note_1()
    note_ids: list[NoteId] = [note_1.id]
    params: DialogParams = DialogParams(all_note_type_details, note_ids)
    callback: FakeEraseControllerCallback = FakeEraseControllerCallback()
    assert callback.history == []
    assert listener.history == []
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}

    adhoc_erase_dialog_controller.show_dialog(params, FakeEraseControllerCallback.call)
    assert callback.history == []
    assert len(listener.history) == 2
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': False,
                                                  'current_state': {'selected_fields': [],
                                                                    'selected_note_type': basic_note_type_details},
                                                  'states': {'Basic': {'selected_fields': [],
                                                                       'selected_note_type': basic_note_type_details}}}


def test_update_config(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                       adhoc_erase_dialog_model: AdhocEraseDialogModel, config_loader: ConfigLoader,
                       basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails,
                       all_note_type_details: list[NoteTypeDetails]):
    callback: FakeEraseControllerCallback = FakeEraseControllerCallback()
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
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}

    # Update config from model
    adhoc_erase_dialog_model.switch_state(basic_note_type_details)
    adhoc_erase_dialog_model.fire_model_changed(None)
    adhoc_erase_dialog_controller.show_dialog(DialogParams(all_note_type_details, []), callback.call)
    adhoc_erase_dialog_model.accept_callback()
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
                'Last Note Type': 'Basic',
                'Last Field Names': []}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': False,
                                                  'current_state': {'selected_fields': [],
                                                                    'selected_note_type': basic_note_type_details},
                                                  'states': {'Basic': {'selected_fields': [],
                                                                       'selected_note_type': basic_note_type_details}}}

    # Update again
    adhoc_erase_dialog_model.switch_state(cloze_note_type_details)
    adhoc_erase_dialog_model.fire_model_changed(None)
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': False,
                                                  'current_state': {'selected_fields': [],
                                                                    'selected_note_type': basic_note_type_details},
                                                  'states': {'Basic': {'selected_fields': [],
                                                                       'selected_note_type': basic_note_type_details},
                                                             'Cloze': {'selected_fields': [],
                                                                       'selected_note_type': cloze_note_type_details}}}


def test_fill_model_from_config_on_startup(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                                           adhoc_erase_dialog_model: AdhocEraseDialogModel, config_loader: ConfigLoader,
                                           basic_note_type_details: NoteTypeDetails,
                                           cloze_note_type_details: NoteTypeDetails,
                                           note_type_details_factory: NoteTypeDetailsFactory,
                                           all_note_type_details: list[NoteTypeDetails]):
    callback: FakeEraseControllerCallback = FakeEraseControllerCallback()
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
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}
    adhoc_erase_dialog_controller.show_dialog(DialogParams(all_note_type_details, []), callback.call)

    # Update config from model
    adhoc_erase_dialog_model.switch_state(basic_note_type_details)
    adhoc_erase_dialog_model.current_state.select_fields(FieldNames([DefaultFields.basic_back]))
    adhoc_erase_dialog_model.fire_model_changed(None)
    adhoc_erase_dialog_model.accept_callback()
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
                'Last Note Type': 'Basic',
                'Last Field Names': ['Back']}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': False,
                                                  'current_state': {'selected_fields': ['Back'],
                                                                    'selected_note_type': basic_note_type_details},
                                                  'states': {'Basic': {'selected_fields': ['Back'],
                                                                       'selected_note_type': basic_note_type_details},
                                                             'Cloze': {'selected_fields': [],
                                                                       'selected_note_type': cloze_note_type_details}}}

    # Initialize controller using saved config
    config: Config = config_loader.load_config()
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    view: AdhocEraseDialogView = AdhocEraseDialogView(model, note_type_details_factory)
    _: AdhocEraseDialogController = AdhocEraseDialogController(
        model, view, note_type_details_factory, config, config_loader)
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
                'Last Note Type': 'Basic',
                'Last Field Names': ['Back']}}}}
    assert model.as_dict() == {'note_types': [],
                               'accept_callback_None': True,
                               'reject_callback_None': True,
                               'current_state': None,
                               'states': {}}
