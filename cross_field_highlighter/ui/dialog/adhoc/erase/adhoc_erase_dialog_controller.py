import logging
from logging import Logger
from typing import Callable

from aqt.qt import QWidget

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.highlighter.types import NoteTypeDetails, FieldName
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogController:

    def __init__(self, model: AdhocEraseDialogModel, view: AdhocEraseDialogView, config: Config):
        self.__model: AdhocEraseDialogModel = model
        self.__view: AdhocEraseDialogView = view
        self.__config: Config = config
        self.__callback: Callable[[QWidget, FieldName], None]

    def show_dialog(self, params: DialogParams, run_on_callback: Callable[[QWidget, FieldName], None]) -> None:
        log.debug(f"Show dialog: {params}")
        self.__model.show = True
        self.__model.note_types = params.note_types
        self.__model.run_op_callback = run_on_callback

        last_note_type: str = self.__config.get_dialog_adhoc_highlight_last_note_type()
        note_type_names: dict[str, NoteTypeDetails] = {note_type.name: note_type for note_type in params.note_types}
        if last_note_type in note_type_names:
            self.__model.selected_note_type = note_type_names[last_note_type]

        if self.__model.selected_note_type:
            last_field: FieldName = self.__config.get_dialog_adhoc_erase_last_field_name()
            if last_field in self.__model.selected_note_type.fields:
                self.__model.selected_source_field = last_field

        self.__model.fire_model_changed()
