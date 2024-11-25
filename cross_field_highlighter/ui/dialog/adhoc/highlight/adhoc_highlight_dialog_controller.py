import logging
from logging import Logger
from typing import Callable, Optional

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldName, FieldNames, NoteTypeName, Text
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogController:

    def __init__(self, model: AdhocHighlightDialogModel, view: AdhocHighlightDialogView,
                 note_type_details_factory: NoteTypeDetailsFactory, formatter_facade: FormatterFacade, config: Config,
                 config_loader: ConfigLoader):
        self.__model: AdhocHighlightDialogModel = model
        self.__view: AdhocHighlightDialogView = view
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.__formatter_facade: FormatterFacade = formatter_facade
        self.__config: Config = config
        self.__config_loader: ConfigLoader = config_loader
        self.__fill_model_from_config()
        self.__run_op_callback: Optional[Callable[[HighlightOpParams], None]] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_dialog(self, params: DialogParams, run_op_callback: Callable[[HighlightOpParams], None]) -> None:
        log.debug(f"Show dialog: {params}")
        self.__run_op_callback = run_op_callback
        self.__model.note_types = params.note_types
        self.__model.note_ids = params.note_ids
        self.__fill_model_from_config()
        if not self.__model.current_state:
            if len(self.__model.note_types) > 0:
                note_type_details: NoteTypeDetails = self.__model.note_types[0]
                self.__model.switch_state(note_type_details)
        self.__view.show_view()

    def __save_model_to_config(self):
        log.debug("Update config from model")
        selected_note_type: NoteTypeDetails = self.__model.current_state.get_selected_note_type()
        self.__config.set_dialog_adhoc_highlight_last_note_type_name(selected_note_type.name)
        selected_source_field: FieldName = self.__model.current_state.selected_source_field
        self.__config.set_dialog_adhoc_highlight_last_source_field_name(selected_note_type.name, selected_source_field)
        self.__config.set_dialog_adhoc_highlight_last_format(
            self.__model.current_state.selected_format.code if self.__model.current_state.selected_format else None)
        self.__config.set_dialog_adhoc_highlight_last_stop_words(self.__model.current_state.selected_stop_words)
        self.__config.set_dialog_adhoc_highlight_last_destination_field_names(
            self.__model.current_state.selected_destination_fields)
        self.__config_loader.write_config(self.__config)

    def __fill_model_from_config(self):
        self.__model.accept_callback = self.__accept_callback
        self.__model.reject_callback = self.__reject_callback
        self.__model.formats = self.__formatter_facade.get_all_formats()
        last_note_type_name: Optional[NoteTypeName] = self.__config.get_dialog_adhoc_highlight_last_note_type_name()
        if last_note_type_name:
            selected_note_type: NoteTypeDetails = self.__note_type_details_factory.by_note_type_name(
                last_note_type_name)
            self.__model.switch_state(selected_note_type)
            last_source_field_name: Optional[
                FieldName] = self.__config.get_dialog_adhoc_highlight_last_source_field_name(last_note_type_name)
            if last_source_field_name:
                self.__model.current_state.selected_source_field = last_source_field_name
        highlight_format_code: Optional[HighlightFormatCode] = self.__config.get_dialog_adhoc_highlight_last_format()
        if highlight_format_code:
            last_format: HighlightFormat = self.__formatter_facade.get_format_by_code(highlight_format_code)
            self.__model.current_state.selected_format = last_format
        last_stop_words: Optional[FieldNames] = self.__config.get_dialog_adhoc_highlight_last_stop_words()
        if last_stop_words:
            self.__model.current_state.selected_stop_words = last_stop_words
        last_destination_field_names: Optional[
            FieldNames] = self.__config.get_dialog_adhoc_highlight_last_destination_field_names()
        if last_destination_field_names:
            self.__model.current_state.selected_destination_fields = last_destination_field_names
        default_stop_words: Optional[FieldNames] = self.__config.get_dialog_adhoc_highlight_default_stop_words()
        if default_stop_words:
            self.__model.default_stop_words = default_stop_words

    def __prepare_op_params(self):
        source_filed: FieldName = self.__model.current_state.selected_source_field
        stop_words: Text = Text(self.__model.current_state.selected_stop_words)
        note_type_details: NoteTypeDetails = self.__model.current_state.get_selected_note_type()
        highlight_op_params: HighlightOpParams = HighlightOpParams(
            note_type_details.note_type_id, self.__model.note_ids, None, source_filed,
            self.__model.current_state.selected_destination_fields, stop_words,
            self.__model.current_state.selected_format)
        return highlight_op_params

    def __accept_callback(self):
        log.debug("Accept callback")
        self.__save_model_to_config()
        erase_op_params: HighlightOpParams = self.__prepare_op_params()
        self.__run_op_callback(erase_op_params)

    def __reject_callback(self):
        log.debug("Reject callback")
        self.__save_model_to_config()

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
