import logging
from logging import Logger
from typing import Callable, Optional

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldName, FieldNames, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel, \
    AdhocHighlightDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogController(AdhocHighlightDialogModelListener):

    def __init__(self, model: AdhocHighlightDialogModel, view: AdhocHighlightDialogView,
                 note_type_details_factory: NoteTypeDetailsFactory, formatter_facade: FormatterFacade, config: Config,
                 config_loader: ConfigLoader):
        self.__model: AdhocHighlightDialogModel = model
        self.__model.add_listener(self)
        self.__view: AdhocHighlightDialogView = view
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.__formatter_facade: FormatterFacade = formatter_facade
        self.__config: Config = config
        self.__config_loader: ConfigLoader = config_loader
        self.__fill_model_from_config()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_dialog(self, params: DialogParams, run_op_callback: Callable[[HighlightOpParams], None]) -> None:
        log.debug(f"Show dialog: {params}")
        self.__model.note_types = params.note_types
        self.__model.note_ids = params.note_ids
        self.__model.formats = self.__formatter_facade.get_all_formats()
        self.__model.accept_callback = run_op_callback

        note_type_names: dict[NoteTypeName, NoteTypeDetails] = {note_type.name: note_type for note_type in
                                                                params.note_types}
        last_note_type_name: NoteTypeName = self.__config.get_dialog_adhoc_highlight_last_note_type_name()
        if last_note_type_name in note_type_names:
            self.__model.selected_note_type = note_type_names[last_note_type_name]

        if self.__model.selected_note_type:
            last_source_field: FieldName = self.__config.get_dialog_adhoc_highlight_last_source_field_name(
                last_note_type_name)
            if last_source_field in self.__model.selected_note_type.fields:
                self.__model.selected_source_field[last_note_type_name] = last_source_field

            last_destination_fields: FieldNames = self.__config.get_dialog_adhoc_highlight_last_destination_field_names()
            if last_destination_fields in self.__model.selected_note_type.fields:
                self.__model.selected_destination_fields = last_destination_fields

        highlight_last_format: Optional[HighlightFormatCode] = self.__config.get_dialog_adhoc_highlight_last_format()
        if highlight_last_format:
            last_format: HighlightFormat = self.__formatter_facade.get_format_by_code(highlight_last_format)
            self.__model.selected_format = last_format

        self.__view.show_view()

    def model_changed(self, source: object):
        if source != self:
            log.debug("Update config from model")
            selected_note_type: Optional[NoteTypeDetails] = self.__model.selected_note_type
            self.__config.set_dialog_adhoc_highlight_last_note_type_name(
                selected_note_type.name if selected_note_type else None)
            if selected_note_type:
                if selected_note_type.name in self.__model.selected_source_field:
                    selected_source_field: FieldName = self.__model.selected_source_field[selected_note_type.name]
                    self.__config.set_dialog_adhoc_highlight_last_source_field_name(selected_note_type.name,
                                                                                    selected_source_field)
            self.__config.set_dialog_adhoc_highlight_last_format(
                self.__model.selected_format.code if self.__model.selected_format else None)
            self.__config.set_dialog_adhoc_highlight_last_stop_words(self.__model.selected_stop_words)
            self.__config.set_dialog_adhoc_highlight_last_destination_field_names(
                self.__model.selected_destination_fields)
            self.__config_loader.write_config(self.__config)

    def __fill_model_from_config(self):
        last_note_type_name: Optional[NoteTypeName] = self.__config.get_dialog_adhoc_highlight_last_note_type_name()
        if last_note_type_name:
            self.__model.selected_note_type = self.__note_type_details_factory.by_note_type_name(last_note_type_name)
            last_source_field_name: Optional[
                FieldName] = self.__config.get_dialog_adhoc_highlight_last_source_field_name(last_note_type_name)
            if last_source_field_name:
                self.__model.selected_source_field[last_note_type_name] = last_source_field_name
        highlight_format_code: Optional[HighlightFormatCode] = self.__config.get_dialog_adhoc_highlight_last_format()
        if highlight_format_code:
            last_format: HighlightFormat = self.__formatter_facade.get_format_by_code(highlight_format_code)
            self.__model.selected_format = last_format
        last_stop_words: Optional[FieldNames] = self.__config.get_dialog_adhoc_highlight_last_stop_words()
        if last_stop_words:
            self.__model.selected_stop_words = last_stop_words
        last_destination_field_names: Optional[
            FieldNames] = self.__config.get_dialog_adhoc_highlight_last_destination_field_names()
        if last_destination_field_names:
            self.__model.selected_destination_fields = last_destination_field_names
        default_stop_words: Optional[FieldNames] = self.__config.get_dialog_adhoc_highlight_default_stop_words()
        if default_stop_words:
            self.__model.default_stop_words = default_stop_words

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
