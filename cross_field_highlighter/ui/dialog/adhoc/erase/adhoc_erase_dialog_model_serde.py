import logging
from logging import Logger

from .adhoc_erase_dialog_model import AdhocEraseDialogModel
from .....highlighter.note_type_details import NoteTypeDetails
from .....highlighter.types import NoteTypeName, FieldNames

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogModelSerDe:
    __fields: str = "fields"

    def __init__(self):
        log.debug(f"{self.__class__.__name__} was instantiated")

    def serialize_states(self, model: AdhocEraseDialogModel) -> dict[str, any]:
        states: list[dict[str, any]] = [{
            "note_type": state.get_selected_note_type().name,
            self.__fields: state.get_selected_fields()
        } for state in model.get_states()]
        result: dict[str, any] = {
            "current_state": model.get_current_state().get_selected_note_type().name,
            "states": states}
        return result

    def deserialize_states(self, model: AdhocEraseDialogModel, json: dict[str, any]) -> None:
        note_type_dict: [NoteTypeName, NoteTypeDetails] = {note_type.name: note_type for note_type in
                                                           model.get_selected_note_types()}
        if "states" in json:
            for state_obj in json["states"]:
                saved_note_type_name: NoteTypeName = state_obj["note_type"]
                if saved_note_type_name in note_type_dict:
                    saved_note_type_details: NoteTypeDetails = note_type_dict[saved_note_type_name]
                    model.switch_state(saved_note_type_details)
                    if self.__fields in state_obj:
                        saved_fields: FieldNames = FieldNames(state_obj[self.__fields])
                        model.get_current_state().select_fields(saved_fields)
        if "current_state" in json:
            current_state_name: NoteTypeName = json["current_state"]
            if current_state_name in note_type_dict:
                current_note_type_details: NoteTypeDetails = note_type_dict[current_state_name]
                model.switch_state(current_note_type_details)

    def __del__(self) -> None:
        log.debug(f"{self.__class__.__name__} was deleted")
