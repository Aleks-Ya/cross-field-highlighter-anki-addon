from anki.notes import Note, NoteId

from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModelListener, \
    AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from tests.data import Data


class FakeCallback:
    params_history: list[EraseOpParams] = []

    @staticmethod
    def call(params: EraseOpParams):
        FakeCallback.params_history.append(params)


class FakeModelListener(AdhocEraseDialogModelListener):
    model_changed_history: list[object] = []

    def model_changed(self, source: object):
        FakeModelListener.model_changed_history.append(source)


def test_show_dialog(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                     adhoc_erase_dialog_model: AdhocEraseDialogModel, td: Data,
                     basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails):
    adhoc_erase_dialog_model.add_listener(FakeModelListener())

    note_types: list[NoteTypeDetails] = [basic_note_type_details, cloze_note_type_details]
    note_1: Note = td.create_basic_note_1()
    note_ids: list[NoteId] = [note_1.id]
    params: DialogParams = DialogParams(note_types, note_ids)
    assert FakeCallback.params_history == []
    assert FakeModelListener.model_changed_history == []
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None}

    adhoc_erase_dialog_controller.show_dialog(params, FakeCallback.call)
    assert FakeCallback.params_history == []
    assert FakeModelListener.model_changed_history == [adhoc_erase_dialog_controller]
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [basic_note_type_details, cloze_note_type_details],
                                                  'run_op_callback_None': False,
                                                  'selected_fields': [],
                                                  'selected_note_type': None}


def test_update_config(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                       adhoc_erase_dialog_model: AdhocEraseDialogModel, config_loader: ConfigLoader,
                       basic_note_type_details: NoteTypeDetails):
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Destination Field Names': [],
                'Last Format': None,
                'Last Note Type': None,
                'Last Source Field Name': None},
            'Erase': {
                'Last Field Names': None,
                'Last Note Type': None}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': None}
    adhoc_erase_dialog_model.selected_note_type = basic_note_type_details
    adhoc_erase_dialog_model.fire_model_changed(None)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Destination Field Names': [],
                'Last Format': None,
                'Last Note Type': None,
                'Last Source Field Name': None},
            'Erase': {
                'Last Field Names': [],
                'Last Note Type': 'Basic'}}}}
    assert adhoc_erase_dialog_model.as_dict() == {'note_types': [],
                                                  'run_op_callback_None': True,
                                                  'selected_fields': [],
                                                  'selected_note_type': basic_note_type_details}