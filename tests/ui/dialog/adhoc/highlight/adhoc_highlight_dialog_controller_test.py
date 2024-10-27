from anki.notes import Note, NoteId

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel, \
    AdhocHighlightDialogModelListener
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from tests.conftest import cloze_note_type_details
from tests.data import Data, DefaultFields


class FakeCallback:
    history: list[HighlightOpParams] = []

    @staticmethod
    def call(params: HighlightOpParams):
        FakeCallback.history.append(params)


class FakeModelListener(AdhocHighlightDialogModelListener):
    history: list[object] = []

    def model_changed(self, source: object):
        FakeModelListener.history.append(source)


def test_show_dialog(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                     adhoc_highlight_dialog_model: AdhocHighlightDialogModel, td: Data,
                     basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails,
                     bold_format: HighlightFormat, italic_format: HighlightFormat, underline_format: HighlightFormat,
                     mark_format: HighlightFormat):
    adhoc_highlight_dialog_model.add_listener(FakeModelListener())

    note_types: list[NoteTypeDetails] = [basic_note_type_details, cloze_note_type_details]
    note_1: Note = td.create_basic_note_1()
    note_ids: list[NoteId] = [note_1.id]
    params: DialogParams = DialogParams(note_types, note_ids)
    assert FakeCallback.history == []
    assert FakeModelListener.history == []
    assert adhoc_highlight_dialog_model.as_dict() == {'formats': [],
                                                      'note_ids': set(),
                                                      'note_types': [],
                                                      'run_op_callback_None': True,
                                                      'selected_destination_fields': [],
                                                      'selected_format': None,
                                                      'selected_note_type': None,
                                                      'selected_source_field': None}

    adhoc_highlight_dialog_controller.show_dialog(params, FakeCallback.call)
    assert FakeCallback.history == []
    assert FakeModelListener.history == [adhoc_highlight_dialog_controller]
    assert adhoc_highlight_dialog_model.as_dict() == {
        'formats': [bold_format, italic_format, underline_format, mark_format],
        'note_ids': note_ids,
        'note_types': [basic_note_type_details, cloze_note_type_details],
        'run_op_callback_None': False,
        'selected_destination_fields': [],
        'selected_format': None,
        'selected_note_type': None,
        'selected_source_field': None}


def test_update_config(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                       adhoc_highlight_dialog_model: AdhocHighlightDialogModel, config_loader: ConfigLoader,
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
    assert adhoc_highlight_dialog_model.as_dict() == {'formats': [],
                                                      'note_ids': set(),
                                                      'note_types': [],
                                                      'run_op_callback_None': True,
                                                      'selected_destination_fields': [],
                                                      'selected_format': None,
                                                      'selected_note_type': None,
                                                      'selected_source_field': None}

    # Update config from model
    adhoc_highlight_dialog_model.selected_note_type = basic_note_type_details
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': 'Basic',
                'Last Source Field Name': None,
                'Last Format': None,
                'Last Destination Field Names': []},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert adhoc_highlight_dialog_model.as_dict() == {'formats': [],
                                                      'note_ids': set(),
                                                      'note_types': [],
                                                      'run_op_callback_None': True,
                                                      'selected_destination_fields': [],
                                                      'selected_format': None,
                                                      'selected_note_type': basic_note_type_details,
                                                      'selected_source_field': None}

    # Update again
    adhoc_highlight_dialog_model.selected_note_type = cloze_note_type_details
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert adhoc_highlight_dialog_model.as_dict() == {'formats': [],
                                                      'note_ids': set(),
                                                      'note_types': [],
                                                      'run_op_callback_None': True,
                                                      'selected_destination_fields': [],
                                                      'selected_format': None,
                                                      'selected_note_type': cloze_note_type_details,
                                                      'selected_source_field': None}


def test_fill_model_from_config_on_startup(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                           adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                           note_type_details_factory: NoteTypeDetailsFactory,
                                           config_loader: ConfigLoader,
                                           basic_note_type_details: NoteTypeDetails,
                                           cloze_note_type_details: NoteTypeDetails,
                                           formatter_facade: FormatterFacade):
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
    assert adhoc_highlight_dialog_model.as_dict() == {'formats': [],
                                                      'note_ids': set(),
                                                      'note_types': [],
                                                      'run_op_callback_None': True,
                                                      'selected_destination_fields': [],
                                                      'selected_format': None,
                                                      'selected_note_type': None,
                                                      'selected_source_field': None}

    # Update config from model
    adhoc_highlight_dialog_model.selected_note_type = basic_note_type_details
    adhoc_highlight_dialog_model.selected_source_field = DefaultFields.basic_front_field
    adhoc_highlight_dialog_model.selected_format = formatter_facade.get_format_by_code(HighlightFormatCode.BOLD)
    adhoc_highlight_dialog_model.selected_destination_fields = FieldNames([DefaultFields.basic_back_field])
    adhoc_highlight_dialog_model.fire_model_changed(None)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': 'Basic',
                'Last Source Field Name': 'Front',
                'Last Format': 'BOLD',
                'Last Destination Field Names': ['Back']},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert (adhoc_highlight_dialog_model.as_dict() ==
            {'formats': [],
             'note_ids': set(),
             'note_types': [],
             'run_op_callback_None': True,
             'selected_destination_fields': ['Back'],
             'selected_format': formatter_facade.get_format_by_code(HighlightFormatCode.BOLD),
             'selected_note_type': basic_note_type_details,
             'selected_source_field': 'Front'})

    # Initialize controller using saved config
    config: Config = config_loader.load_config()
    model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    _: AdhocHighlightDialogController = AdhocHighlightDialogController(model, note_type_details_factory,
                                                                       formatter_facade, config, config_loader)
    assert config_loader.load_config().get_as_dict() == {
        'Dialog': {'Adhoc': {
            'Highlight': {
                'Last Note Type': 'Basic',
                'Last Source Field Name': 'Front',
                'Last Format': 'BOLD',
                'Last Destination Field Names': ['Back']},
            'Erase': {
                'Last Note Type': None,
                'Last Field Names': None}}}}
    assert model.as_dict() == {'formats': [],
                               'note_ids': set(),
                               'note_types': [],
                               'run_op_callback_None': True,
                               'selected_destination_fields': ['Back'],
                               'selected_format': formatter_facade.get_format_by_code(HighlightFormatCode.BOLD),
                               'selected_note_type': basic_note_type_details,
                               'selected_source_field': 'Front'}
