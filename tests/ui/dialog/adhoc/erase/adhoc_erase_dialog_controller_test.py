from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from tests.conftest import cloze_note_type_details, basic_note_type_details
from tests.data import Data, DefaultFields, DefaultStopWords
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_asserts import FakeModelListener, FakeEraseControllerCallback


def test_show_dialog(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                     adhoc_erase_dialog_view: AdhocEraseDialogView,
                     adhoc_erase_dialog_model: AdhocEraseDialogModel, td: Data,
                     basic_note_type_details: NoteTypeDetails,
                     all_note_type_details: list[NoteTypeDetails]):
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

    adhoc_erase_dialog_controller.show_dialog(params, FakeEraseControllerCallback.call)
    assert callback.history == []
    assert len(listener.history) == 1
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'note_number': 0,
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
                **DefaultStopWords.config,
                'States': {}},
            'Erase': {'States': {}}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'note_number': 0,
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}

    # Update config from model
    adhoc_erase_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    adhoc_erase_dialog_model.call_accept_callback()
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                **DefaultStopWords.config,
                'States': {}},
            'Erase': {'States': {'current_state': 'Basic',
                                 'states': [{'fields': [], 'note_type': 'Basic'}]}}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': all_note_type_details,
                                                  'note_number': 0,
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
                                                  'note_number': 0,
                                                  'accept_callback_None': False,
                                                  'reject_callback_None': False,
                                                  'current_state': {'selected_fields': [],
                                                                    'selected_note_type': cloze_note_type_details},
                                                  'states': {'Basic': {'selected_fields': [],
                                                                       'selected_note_type': basic_note_type_details},
                                                             'Cloze': {'selected_fields': [],
                                                                       'selected_note_type': cloze_note_type_details}}}


def test_fill_model_from_config_on_startup(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                                           adhoc_erase_dialog_model: AdhocEraseDialogModel, config_loader: ConfigLoader,
                                           basic_note_type_details: NoteTypeDetails,
                                           cloze_note_type_details: NoteTypeDetails,
                                           note_type_details_factory: NoteTypeDetailsFactory,
                                           all_note_type_details: list[NoteTypeDetails],
                                           adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe):
    callback: FakeEraseControllerCallback = FakeEraseControllerCallback()
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                **DefaultStopWords.config,
                'States': {}},
            'Erase': {'States': {}}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'note_number': 0,
                                                  'accept_callback_None': True,
                                                  'reject_callback_None': True,
                                                  'current_state': None,
                                                  'states': {}}

    # Show dialog
    adhoc_erase_dialog_controller.show_dialog(DialogParams(all_note_type_details, 0), callback.call)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                **DefaultStopWords.config,
                'States': {}},
            'Erase': {'States': {}}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'accept_callback_None': False,
                                                  'current_state': {'selected_fields': [],
                                                                    'selected_note_type': basic_note_type_details},
                                                  'note_types': all_note_type_details,
                                                  'note_number': 0,
                                                  'reject_callback_None': False,
                                                  'states': {'Basic': {'selected_fields': [],
                                                                       'selected_note_type': basic_note_type_details}}}

    # Update config from model
    adhoc_erase_dialog_model.switch_state(cloze_note_type_details)
    adhoc_erase_dialog_model.get_current_state().select_fields(FieldNames([DefaultFields.cloze_extra]))
    adhoc_erase_dialog_model.fire_model_changed(None)
    adhoc_erase_dialog_model.call_accept_callback()
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Erase': {'States': {'current_state': 'Cloze',
                                 'states': [{'fields': [], 'note_type': 'Basic'},
                                            {'fields': ['Back Extra'], 'note_type': 'Cloze'}]}},
            'Highlight': {**DefaultStopWords.config, 'States': {}}}}}
    assert adhoc_erase_dialog_model.as_dict() == {
        'accept_callback_None': False,
        'current_state': {'selected_fields': [DefaultFields.cloze_extra],
                          'selected_note_type': cloze_note_type_details},
        'note_types': all_note_type_details,
        'note_number': 0,
        'reject_callback_None': False,
        'states': {'Basic': {'selected_fields': [],
                             'selected_note_type': basic_note_type_details},
                   'Cloze': {'selected_fields': [DefaultFields.cloze_extra],
                             'selected_note_type': cloze_note_type_details}}}

    # Initialize controller using saved config
    config: Config = config_loader.load_config()
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    view: AdhocEraseDialogView = AdhocEraseDialogView(model)
    _: AdhocEraseDialogController = AdhocEraseDialogController(
        model, view, note_type_details_factory, adhoc_erase_dialog_model_serde, config, config_loader)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Erase': {'States': {'current_state': 'Cloze',
                                 'states': [{'fields': [], 'note_type': 'Basic'},
                                            {'fields': ['Back Extra'], 'note_type': 'Cloze'}]}},
            'Highlight': {**DefaultStopWords.config, 'States': {}}}}}
    assert model.as_dict() == {'note_types': [],
                               'note_number': 0,
                               'accept_callback_None': True,
                               'reject_callback_None': True,
                               'current_state': None,
                               'states': {}}
