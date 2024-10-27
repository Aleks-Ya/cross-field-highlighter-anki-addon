from anki.notes import Note, NoteId

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModelListener, \
    AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from tests.conftest import cloze_note_type_details
from tests.data import Data, DefaultFields


class FakeCallback:
    history: list[EraseOpParams] = []

    @staticmethod
    def call(params: EraseOpParams):
        FakeCallback.history.append(params)


class FakeModelListener(AdhocEraseDialogModelListener):
    history: list[object] = []

    def model_changed(self, source: object):
        FakeModelListener.history.append(source)


def test_show_dialog(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                     adhoc_erase_dialog_model: AdhocEraseDialogModel, td: Data,
                     basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails):
    adhoc_erase_dialog_model.add_listener(FakeModelListener())

    note_types: list[NoteTypeDetails] = [basic_note_type_details, cloze_note_type_details]
    note_1: Note = td.create_basic_note_1()
    note_ids: list[NoteId] = [note_1.id]
    params: DialogParams = DialogParams(note_types, note_ids)
    assert FakeCallback.history == []
    assert FakeModelListener.history == []
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None}

    adhoc_erase_dialog_controller.show_dialog(params, FakeCallback.call)
    assert FakeCallback.history == []
    assert FakeModelListener.history == [adhoc_erase_dialog_controller]
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [basic_note_type_details, cloze_note_type_details],
                                                  'run_op_callback_None': False,
                                                  'selected_fields': [],
                                                  'selected_note_type': None}


def test_update_config(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                       adhoc_erase_dialog_model: AdhocEraseDialogModel, config_loader: ConfigLoader,
                       basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails):
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': None,
                'Last Source Field Name': None,
                'Last Format': None,
                'Last Destination Field Names': None},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None}

    # Update config from model
    adhoc_erase_dialog_model.selected_note_type = basic_note_type_details
    adhoc_erase_dialog_model.fire_model_changed(None)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': None,
                'Last Source Field Name': None,
                'Last Format': None,
                'Last Destination Field Names': None},
            'Erase': {
                'Last Note Type': 'Basic',
                'Last Field Names': []}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details}

    # Update again
    adhoc_erase_dialog_model.selected_note_type = cloze_note_type_details
    adhoc_erase_dialog_model.fire_model_changed(None)
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': cloze_note_type_details}


def test_fill_model_from_config_on_startup(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                                           adhoc_erase_dialog_model: AdhocEraseDialogModel, config_loader: ConfigLoader,
                                           basic_note_type_details: NoteTypeDetails,
                                           cloze_note_type_details: NoteTypeDetails,
                                           note_type_details_factory: NoteTypeDetailsFactory):
    # Default config and model
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': None,
                'Last Source Field Name': None,
                'Last Format': None,
                'Last Destination Field Names': None},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None}

    # Update config from model
    adhoc_erase_dialog_model.selected_note_type = basic_note_type_details
    adhoc_erase_dialog_model.selected_fields = FieldNames([DefaultFields.basic_back_field])
    adhoc_erase_dialog_model.fire_model_changed(None)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': None,
                'Last Source Field Name': None,
                'Last Format': None,
                'Last Destination Field Names': None},
            'Erase': {
                'Last Note Type': 'Basic',
                'Last Field Names': ['Back']}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': ['Back'],
                                                  'selected_note_type': basic_note_type_details}

    # Initialize controller using saved config
    config: Config = config_loader.load_config()
    model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    _: AdhocEraseDialogController = AdhocEraseDialogController(
        model, note_type_details_factory, config, config_loader)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': None,
                'Last Source Field Name': None,
                'Last Format': None,
                'Last Destination Field Names': None},
            'Erase': {
                'Last Note Type': 'Basic',
                'Last Field Names': ['Back']}}}}
    assert model.as_dict() == {'note_types': [],
                               'run_op_callback_None': True,
                               'selected_fields': ['Back'],
                               'selected_note_type': basic_note_type_details}
