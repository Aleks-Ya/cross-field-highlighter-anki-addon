import logging
from logging import Logger
from typing import Callable

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldName, FieldNames
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel, \
    AdhocHighlightDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogController(AdhocHighlightDialogModelListener):

    def __init__(self, model: AdhocHighlightDialogModel, view: AdhocHighlightDialogView,
                 formatter_facade: FormatterFacade, config: Config, config_loader: ConfigLoader):
        self.__model: AdhocHighlightDialogModel = model
        self.__view: AdhocHighlightDialogView = view
        self.__formatter_facade: FormatterFacade = formatter_facade
        self.__config: Config = config
        self.__config_loader: ConfigLoader = config_loader
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_dialog(self, params: DialogParams, run_op_callback: Callable[[HighlightOpParams], None]) -> None:
        log.debug(f"Show dialog: {params}")
        self.__model.show = True
        self.__model.note_types = params.note_types
        self.__model.note_ids = params.note_ids
        self.__model.formats = self.__formatter_facade.get_all_formats()
        self.__model.run_op_callback = run_op_callback

        last_note_type: str = self.__config.get_dialog_adhoc_highlight_last_note_type()
        note_type_names: dict[str, NoteTypeDetails] = {note_type.name: note_type for note_type in params.note_types}
        if last_note_type in note_type_names:
            self.__model.selected_note_type = note_type_names[last_note_type]

        if self.__model.selected_note_type:
            last_source_field: FieldName = self.__config.get_dialog_adhoc_highlight_last_source_field_name()
            if last_source_field in self.__model.selected_note_type.fields:
                self.__model.selected_source_field = last_source_field

            last_format: HighlightFormat = self.__formatter_facade.get_format_by_code(
                self.__config.get_dialog_adhoc_highlight_last_format())
            if last_format:
                self.__model.selected_format = last_format

            last_destination_fields: FieldNames = self.__config.get_dialog_adhoc_highlight_last_destination_field_names()
            if last_destination_fields in self.__model.selected_note_type.fields:
                self.__model.selected_destination_fields = last_destination_fields

        self.__model.fire_model_changed(self)

    def model_changed(self, source: object):
        if source != self:
            log.debug("Update config from model")
            self.__config.set_dialog_adhoc_highlight_last_note_type(self.__model.selected_note_type.name)
            self.__config.set_dialog_adhoc_highlight_last_source_field_name(self.__model.selected_source_field)
            self.__config.set_dialog_adhoc_highlight_last_format(self.__model.selected_format.code)
            self.__config.set_dialog_adhoc_highlight_last_destination_field_names(
                self.__model.selected_destination_fields)
            self.__config_loader.write_config(self.__config)

    def __repr__(self):
        return self.__class__.__name__
