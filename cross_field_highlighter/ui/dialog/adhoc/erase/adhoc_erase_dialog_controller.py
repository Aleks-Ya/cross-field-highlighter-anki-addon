import logging
from logging import Logger
from typing import Callable, Optional

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogController:

    def __init__(self, model: AdhocEraseDialogModel, view: AdhocEraseDialogView,
                 note_type_details_factory: NoteTypeDetailsFactory, config: Config, config_loader: ConfigLoader):
        self.__model: AdhocEraseDialogModel = model
        self.__view: AdhocEraseDialogView = view
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.__config: Config = config
        self.__config_loader: ConfigLoader = config_loader
        self.__run_op_callback: Optional[Callable[[EraseOpParams], None]] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_dialog(self, params: DialogParams, run_op_callback: Callable[[EraseOpParams], None]) -> None:
        log.debug(f"Show dialog: {params}")
        self.__run_op_callback = run_op_callback
        self.__model.note_types = params.note_types
        self.__model.accept_callback = self.__accept_callback
        self.__model.reject_callback = self.__reject_callback
        self.__fill_model_from_config()
        self.__view.show_view()

    def __fill_model_from_config(self):
        last_note_type_name: Optional[NoteTypeName] = self.__config.get_dialog_adhoc_erase_last_note_type_name()
        if last_note_type_name:
            last_note_type_details: NoteTypeDetails = self.__note_type_details_factory.by_note_type_name(
                last_note_type_name)
            self.__model.switch_state(last_note_type_details)
        last_field_names: Optional[FieldNames] = self.__config.get_dialog_adhoc_erase_last_field_names()
        if last_field_names:
            self.__model.get_current_state().select_fields(last_field_names)

    def __save_model_to_config(self):
        log.debug("Save model to config")
        note_type_name: NoteTypeName = self.__model.get_current_state().get_selected_note_type().name
        self.__config.set_dialog_adhoc_erase_last_note_type_name(note_type_name)
        self.__config.set_dialog_adhoc_erase_last_field_names(self.__model.get_current_state().get_selected_fields())
        self.__config_loader.write_config(self.__config)

    def __accept_callback(self):
        log.debug("Accept callback")
        self.__save_model_to_config()
        erase_op_params: EraseOpParams = EraseOpParams(
            self.__model.get_current_state().get_selected_note_type().note_type_id,
            None, self.__model.get_current_state().get_selected_fields())
        self.__run_op_callback(erase_op_params)

    def __reject_callback(self):
        log.debug("Reject callback")
        self.__save_model_to_config()

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
