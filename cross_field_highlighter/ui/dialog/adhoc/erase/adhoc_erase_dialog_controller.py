import logging
from logging import Logger
from typing import Callable, Optional

from .adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from .....config.config import Config
from .....config.config_loader import ConfigLoader
from .....highlighter.note_type_details_factory import NoteTypeDetailsFactory
from .....ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from .....ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from .....ui.dialog.dialog_params import DialogParams
from .....ui.operation.erase_op_params import EraseOpParams

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogController:

    def __init__(self, model: AdhocEraseDialogModel, view: AdhocEraseDialogView,
                 note_type_details_factory: NoteTypeDetailsFactory, model_serde: AdhocEraseDialogModelSerDe,
                 config: Config, config_loader: ConfigLoader):
        self.__model: AdhocEraseDialogModel = model
        self.__view: AdhocEraseDialogView = view
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.__model_serde: AdhocEraseDialogModelSerDe = model_serde
        self.__config: Config = config
        self.__config_loader: ConfigLoader = config_loader
        self.__start_callback: Optional[Callable[[EraseOpParams], None]] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_dialog(self, params: DialogParams, start_callback: Callable[[EraseOpParams], None]) -> None:
        log.debug(f"Show dialog: {params}")
        self.__start_callback = start_callback
        self.__model.fill(params.note_types, params.note_number, self.__accept_callback, self.__reject_callback)
        self.__model.reset_states()
        self.__fill_model_from_config()
        self.__view.show_view()

    def __fill_model_from_config(self):
        data: dict[str, any] = self.__config.get_dialog_adhoc_erase_states()
        self.__model_serde.deserialize_states(self.__model, data)

    def __save_model_to_config(self):
        log.debug("Save model to config")
        data: dict[str, any] = self.__model_serde.serialize_states(self.__model)
        self.__config.set_dialog_adhoc_erase_states(data)
        self.__config_loader.write_config(self.__config)

    def __accept_callback(self):
        log.debug("Accept callback")
        self.__save_model_to_config()
        erase_op_params: EraseOpParams = EraseOpParams(
            self.__model.get_current_state().get_selected_note_type().note_type_id,
            self.__model.get_current_state().get_selected_fields())
        self.__start_callback(erase_op_params)

    def __reject_callback(self):
        log.debug("Reject callback")
        self.__save_model_to_config()

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
