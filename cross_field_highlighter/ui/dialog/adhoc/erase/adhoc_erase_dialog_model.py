import logging
from logging import Logger
from abc import abstractmethod
from typing import Callable, Optional

from .....highlighter.note_type_details import NoteTypeDetails
from .....highlighter.types import NoteTypeName, FieldNames
from .....ui.dialog.adhoc.erase.adhoc_erase_dialog_state import AdhocEraseDialogState

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogModelListener:
    @abstractmethod
    def model_changed(self, source: object):
        pass


class AdhocEraseDialogModel:
    __fields: str = "fields"

    def __init__(self):
        self.__note_types: list[NoteTypeDetails] = []
        self.__current_state: Optional[AdhocEraseDialogState] = None
        self.__accept_callback: Optional[Callable[[], None]] = None
        self.__reject_callback: Optional[Callable[[], None]] = None
        self.__states: dict[NoteTypeName, AdhocEraseDialogState] = {}
        self.__listeners: set[AdhocEraseDialogModelListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def fill(self, note_types: list[NoteTypeDetails], accept_callback: Optional[Callable[[], None]],
             reject_callback: Optional[Callable[[], None]]) -> None:
        self.__note_types = note_types
        self.__accept_callback = accept_callback
        self.__reject_callback = reject_callback

    def get_note_types(self) -> list[NoteTypeDetails]:
        return self.__note_types

    def get_current_state(self) -> AdhocEraseDialogState:
        if not self.__current_state:
            self.switch_to_first_state()
        return self.__current_state

    def get_states(self) -> list[AdhocEraseDialogState]:
        return list(self.__states.values())

    def switch_state(self, note_type_details: NoteTypeDetails):
        note_type_name: NoteTypeName = note_type_details.name
        if note_type_name not in self.__states:
            self.__states[note_type_name] = AdhocEraseDialogState(note_type_details)
        self.__current_state = self.__states[note_type_name]

    def switch_to_first_state(self) -> None:
        if len(self.__note_types) < 1:
            raise Exception("At least one note type should exist")
        note_type_details: NoteTypeDetails = self.__note_types[0]
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
            listener.model_changed(source)

    def reset_states(self) -> None:
        for state in self.__states.values():
            state.select_fields(FieldNames([]))
        self.switch_to_first_state()

    def as_dict(self) -> dict[str, any]:
        return {
            "note_types": self.__note_types,
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
