import logging
from logging import Logger
from typing import Any

from anki.models import NotetypeId

from .adhoc_erase_dialog_model import AdhocEraseDialogModel
from .....highlighter.types import FieldNames

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogModelSerDe:
    __note_type_id: str = "note_type_id"
    __fields: str = "fields"
    __current_state: str = "current_state"
    __states: str = "states"

    def __init__(self):
        log.debug(f"{self.__class__.__name__} was instantiated")

    def serialize_states(self, model: AdhocEraseDialogModel) -> dict[str, Any]:
        states: list[dict[str, Any]] = [{
            self.__note_type_id: state.get_selected_note_type().note_type_id,
            self.__fields: state.get_selected_fields()
        } for state in model.get_states()]
        result: dict[str, Any] = {
            self.__current_state: model.get_current_state().get_selected_note_type().note_type_id,
            self.__states: states}
        return result

    def deserialize_states(self, model: AdhocEraseDialogModel, json: dict[str, Any]) -> None:
        note_type_ids: list[NotetypeId] = [note_type_details.note_type_id for note_type_details in
                                           model.get_all_note_types()]
        if self.__states in json:
            for state_obj in json[self.__states]:
                note_type_id: NotetypeId = state_obj[self.__note_type_id]
                if note_type_id in note_type_ids:
                    selected_fields: FieldNames = FieldNames(
                        state_obj[self.__fields]) if self.__fields in state_obj else []
                    model.get_state(note_type_id).select_fields(selected_fields)
        if self.__current_state in json:
            current_note_type_id: NotetypeId = json[self.__current_state]
            if current_note_type_id in note_type_ids:
                model.switch_state(current_note_type_id)

    def __del__(self) -> None:
        log.debug(f"{self.__class__.__name__} was deleted")
