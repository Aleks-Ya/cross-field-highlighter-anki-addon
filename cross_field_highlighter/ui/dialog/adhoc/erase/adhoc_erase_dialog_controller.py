import logging
from logging import Logger
from typing import Callable

from aqt.qt import QWidget

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.types import NoteTypeDetails, FieldName, FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel, \
    AdhocEraseDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogController(AdhocEraseDialogModelListener):

    def __init__(self, model: AdhocEraseDialogModel, view: AdhocEraseDialogView, config: Config,
                 config_loader: ConfigLoader):
        self.__model: AdhocEraseDialogModel = model
        self.__model.add_listener(self)
        self.__view: AdhocEraseDialogView = view
        self.__config: Config = config
        self.__config_loader: ConfigLoader = config_loader
        self.__callback: Callable[[QWidget, FieldName], None]
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_dialog(self, params: DialogParams, run_on_callback: Callable[[QWidget, FieldNames], None]) -> None:
        log.debug(f"Show dialog: {params}")
        self.__model.show = True
        self.__model.note_types = params.note_types
        self.__model.run_op_callback = run_on_callback

        last_note_type: str = self.__config.get_dialog_adhoc_erase_last_note_type()
        log.debug(f"Last note type: {last_note_type}")
        note_type_names: dict[str, NoteTypeDetails] = {note_type.name: note_type for note_type in params.note_types}
        log.debug(f"Note type names: {note_type_names}")
        if last_note_type in note_type_names:
            log.debug(f"Set selected note type: {note_type_names[last_note_type]}")
            self.__model.selected_note_type = note_type_names[last_note_type]

        if self.__model.selected_note_type:
            last_field_names: FieldNames = self.__config.get_dialog_adhoc_erase_last_field_names()
            log.debug(f"Last field: {last_field_names}")
            for last_field in last_field_names:
                if last_field in self.__model.selected_note_type.fields:
                    log.debug(f"Set selected field: {last_field}")
                    self.__model.selected_source_field = last_field

        self.__model.fire_model_changed(self)

    def model_changed(self, source: object):
        if source != self:
            log.debug("Update config from model")
            self.__config.set_dialog_adhoc_erase_last_note_type(self.__model.selected_note_type.name)
            self.__config.set_dialog_adhoc_erase_last_field_names(self.__model.selected_fields)
            self.__config_loader.write_config(self.__config)

    def __repr__(self):
        return self.__class__.__name__