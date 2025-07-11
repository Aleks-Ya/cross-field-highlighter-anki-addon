import logging
from logging import Logger
from typing import Callable, Optional, Any

from aqt.utils import show_info

from .adhoc_highlight_dialog_model_serde import AdhocHighlightDialogModelSerDe
from .adhoc_highlight_dialog_state import AdhocHighlightDialogState
from .....config.config import Config
from .....config.user_files_storage import UserFilesStorage
from .....highlighter.formatter.formatter_facade import FormatterFacade
from .....highlighter.note_type_details import NoteTypeDetails
from .....highlighter.note_type_details_factory import NoteTypeDetailsFactory
from .....highlighter.types import FieldName, Text, FieldNames
from .....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from .....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from .....ui.dialog.dialog_params import DialogParams
from .....ui.operation.highlight_op_params import HighlightOpParams

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogController:
    __state_key: str = "highlight_dialog_states"

    def __init__(self, model: AdhocHighlightDialogModel, view: AdhocHighlightDialogView,
                 note_type_details_factory: NoteTypeDetailsFactory, formatter_facade: FormatterFacade,
                 model_serde: AdhocHighlightDialogModelSerDe, config: Config, user_files_storage: UserFilesStorage):
        self.__model: AdhocHighlightDialogModel = model
        self.__view: AdhocHighlightDialogView = view
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.__formatter_facade: FormatterFacade = formatter_facade
        self.__model_serde: AdhocHighlightDialogModelSerDe = model_serde
        self.__config: Config = config
        self.__user_files_storage: UserFilesStorage = user_files_storage
        self.__fill_model_from_storage()
        self.__run_op_callback: Optional[Callable[[HighlightOpParams], None]] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_dialog(self, params: DialogParams, run_op_callback: Callable[[HighlightOpParams], None]) -> None:
        log.debug(f"Show dialog: {params}")
        if len(params.selected_note_types) == 0:
            log.debug("No notes are selected")
            show_info("No notes are selected", title="Cross-Field Highlighter")
            return
        self.__run_op_callback = run_op_callback
        default_stop_words: Optional[str] = self.__config.get_dialog_adhoc_highlight_default_stop_words()
        self.__model.fill(self.__note_type_details_factory.get_all(), params.selected_note_types, params.note_number,
                          self.__formatter_facade.get_all_formats(), default_stop_words, self.__accept_callback,
                          self.__reject_callback)
        self.__fill_model_from_storage()
        self.__model.get_current_state()  # choose 1st if not selected
        self.__view.show_view()

    def __save_model_to_storage(self) -> None:
        log.debug("Save model to storage")
        serialized_state: dict[str, Any] = self.__model_serde.serialize_states(self.__model)
        self.__user_files_storage.write(self.__state_key, serialized_state)

    def __fill_model_from_storage(self) -> None:
        log.debug("Fill model from storage")
        log.debug(f"Model before deserialization: {self.__model.as_dict()}")
        data: dict[str, Any] = self.__user_files_storage.read(self.__state_key)
        log.debug(f"Data from storage: {data}")
        self.__model_serde.deserialize_states(self.__model, data)
        log.debug(f"Model after deserialization: {self.__model.as_dict()}")

    def __prepare_op_params(self) -> HighlightOpParams:
        state: AdhocHighlightDialogState = self.__model.get_current_state()
        source_field: FieldName = state.get_selected_source_field()
        stop_words: Text = Text(state.get_selected_stop_words())
        note_type: NoteTypeDetails = state.get_selected_note_type()
        enabled_destination_fields: FieldNames = state.get_selected_enabled_destination_fields()
        highlight_op_params: HighlightOpParams = HighlightOpParams(
            note_type.note_type_id, source_field, enabled_destination_fields, stop_words, state.get_selected_format())
        return highlight_op_params

    def __accept_callback(self) -> None:
        log.debug("Accept callback")
        self.__save_model_to_storage()
        highlight_op_params: HighlightOpParams = self.__prepare_op_params()
        self.__run_op_callback(highlight_op_params)

    def __reject_callback(self) -> None:
        log.debug("Reject callback")
        self.__save_model_to_storage()

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
