import logging
from logging import Logger
from typing import Callable

from aqt.qt import QWidget

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import NoteTypeDetails, FieldName
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogController:

    def __init__(self, model: AdhocHighlightDialogModel, view: AdhocHighlightDialogView, config: Config):
        self.__model: AdhocHighlightDialogModel = model
        self.__view: AdhocHighlightDialogView = view
        self.__config: Config = config

    def show_dialog(self, params: DialogParams, run_op_callback: Callable[
        [QWidget, FieldName, FieldName, set[str], HighlightFormat], None]) -> None:

        log.debug(f"Show dialog: {params}")
        self.__model.show = True
        self.__model.note_types = params.note_types
        self.__model.run_op_callback = run_op_callback

        last_note_type: str = self.__config.get_dialog_adhoc_last_note_type()
        note_type_names: dict[str, NoteTypeDetails] = {note_type.name: note_type for note_type in params.note_types}
        if last_note_type in note_type_names:
            self.__model.selected_note_type = note_type_names[last_note_type]

        if self.__model.selected_note_type:
            last_source_field: FieldName = self.__config.get_dialog_adhoc_last_source_field_name()
            if last_source_field in self.__model.selected_note_type.fields:
                self.__model.selected_source_field = last_source_field

            last_format: HighlightFormat = self.__config.get_dialog_adhoc_last_format()
            if last_format:
                self.__model.selected_format = last_format

            last_destination_field: FieldName = self.__config.get_dialog_adhoc_last_destination_field_name()
            if last_destination_field in self.__model.selected_note_type.fields:
                self.__model.selected_destination_field = last_destination_field

        self.__model.fire_model_changed()
