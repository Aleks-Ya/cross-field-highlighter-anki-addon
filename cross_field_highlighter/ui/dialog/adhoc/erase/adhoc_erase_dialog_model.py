import logging
from abc import abstractmethod
from logging import Logger
from typing import Callable, Optional

from anki.models import NotetypeId

from .....highlighter.note_type_details import NoteTypeDetails
from .....highlighter.types import FieldNames
from .....ui.dialog.adhoc.erase.adhoc_erase_dialog_state import AdhocEraseDialogState

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogModelListener:
    @abstractmethod
    def erase_model_changed(self, source: object, model: 'AdhocEraseDialogModel'):
        pass


class AdhocEraseDialogModel:
    def __init__(self):
        self.__all_note_types: list[NoteTypeDetails] = []
        self.__selected_note_types: list[NoteTypeDetails] = []
        self.__note_number: int = 0
        self.__current_state: Optional[AdhocEraseDialogState] = None
        self.__accept_callback: Optional[Callable[[], None]] = None
        self.__reject_callback: Optional[Callable[[], None]] = None
        self.__states: dict[NotetypeId, AdhocEraseDialogState] = {}
        self.__listeners: set[AdhocEraseDialogModelListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def fill(self, all_note_types: list[NoteTypeDetails], selected_note_types: list[NoteTypeDetails], note_number: int,
             accept_callback: Optional[Callable[[], None]], reject_callback: Optional[Callable[[], None]]) -> None:
        self.__all_note_types = all_note_types
        self.__selected_note_types = selected_note_types
        self.__note_number = note_number
        self.__accept_callback = accept_callback
        self.__reject_callback = reject_callback

    def get_all_note_types(self) -> list[NoteTypeDetails]:
        return self.__all_note_types

    def get_selected_note_types(self) -> list[NoteTypeDetails]:
        return self.__selected_note_types

    def get_note_number(self) -> int:
        return self.__note_number

    def get_current_state(self) -> AdhocEraseDialogState:
        if not self.__current_state or self.__current_state.get_selected_note_type() not in self.__selected_note_types:
            self.switch_to_first_state()
        return self.__current_state

    def get_states(self) -> list[AdhocEraseDialogState]:
        return list(self.__states.values())

    def switch_state(self, note_type_details: NoteTypeDetails):
        note_type_id: NotetypeId = note_type_details.note_type_id
        if note_type_id not in self.__states:
            self.__states[note_type_id] = AdhocEraseDialogState(note_type_details)
        self.__current_state = self.__states[note_type_id]

    def switch_to_first_state(self) -> None:
        if len(self.__selected_note_types) < 1:
            raise ValueError("At least one note type should exist")
        note_type_details: NoteTypeDetails = self.__selected_note_types[0]
        self.switch_state(note_type_details)

    def add_listener(self, listener: AdhocEraseDialogModelListener) -> None:
        self.__listeners.add(listener)

    def call_accept_callback(self) -> None:
        if self.__accept_callback:
            self.__accept_callback()

    def call_reject_callback(self) -> None:
        if self.__reject_callback:
            self.__reject_callback()

    def fire_model_changed(self, source: object) -> None:
        log.debug(f"Fire model changed: {source}")
        for listener in self.__listeners:
            listener.erase_model_changed(source, self)

    def reset_states(self) -> None:
        log.debug("Reset states")
        for state in self.__states.values():
            state.select_fields(FieldNames([]))
        self.switch_to_first_state()

    def as_dict(self) -> dict[str, any]:
        return {
            "all_note_types": self.__all_note_types,
            "selected_note_types": self.__selected_note_types,
            "note_number": self.__note_number,
            "accept_callback_None": not self.__accept_callback,
            "reject_callback_None": not self.__reject_callback,
            "states": {k: v.as_dict() for k, v in self.__states.items()},
            "current_state": self.__current_state.as_dict() if self.__current_state else None
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.as_dict()})"

    def __eq__(self, other):
        if not isinstance(other, AdhocEraseDialogModel):
            return False
        return self.as_dict() == other.as_dict()

    def __del__(self) -> None:
        log.debug(f"{self.__class__.__name__} was deleted")
