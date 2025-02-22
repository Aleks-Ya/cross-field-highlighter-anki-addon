import logging
from logging import Logger
from typing import Callable, Optional

from aqt.utils import show_info

from .adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from .....config.user_folder_storage import UserFolderStorage
from .....highlighter.note_type_details_factory import NoteTypeDetailsFactory
from .....ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from .....ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from .....ui.dialog.dialog_params import DialogParams
from .....ui.operation.erase_op_params import EraseOpParams

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogController:
    __state_key: str = "erase_dialog_states"

    def __init__(self, model: AdhocEraseDialogModel, view: AdhocEraseDialogView,
                 note_type_details_factory: NoteTypeDetailsFactory, model_serde: AdhocEraseDialogModelSerDe,
                 user_folder_storage: UserFolderStorage):
        self.__model: AdhocEraseDialogModel = model
        self.__view: AdhocEraseDialogView = view
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.__model_serde: AdhocEraseDialogModelSerDe = model_serde
        self.__user_folder_storage: UserFolderStorage = user_folder_storage
        self.__start_callback: Optional[Callable[[EraseOpParams], None]] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_dialog(self, params: DialogParams, start_callback: Callable[[EraseOpParams], None]) -> None:
        log.debug(f"Show dialog: {params}")
        if len(params.selected_note_types) == 0:
            log.debug("No notes are selected")
            show_info("No notes are selected", title="Cross-Field Highlighter")
            return
        self.__start_callback = start_callback
        self.__model.fill(self.__note_type_details_factory.get_all(), params.selected_note_types, params.note_number,
                          self.__accept_callback, self.__reject_callback)
        self.__fill_model_from_config()
        self.__model.get_current_state()  # choose 1st if not selected
        self.__view.show_view()

    def __fill_model_from_config(self):
        data: dict[str, any] = self.__user_folder_storage.read(self.__state_key)
        self.__model_serde.deserialize_states(self.__model, data)

    def __save_model_to_config(self):
        log.debug("Save model to storage")
        serialized_state: dict[str, any] = self.__model_serde.serialize_states(self.__model)
        self.__user_folder_storage.write(self.__state_key, serialized_state)

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
