import logging
from logging import Logger
from abc import abstractmethod
from typing import Callable, Optional

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogModelListener:
    @abstractmethod
    def model_changed(self, source: object):
        pass


class AdhocEraseDialogModel:
    def __init__(self):
        self.note_types: list[NoteTypeDetails] = []
        self.selected_note_type: Optional[NoteTypeDetails] = None
        self.selected_fields: FieldNames = FieldNames([])
        self.run_op_callback: Optional[Callable[[EraseOpParams], None]] = None
        self.__listeners: set[AdhocEraseDialogModelListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def add_listener(self, listener: AdhocEraseDialogModelListener):
        self.__listeners.add(listener)

    def fire_model_changed(self, source: object):
        log.debug(f"Fire model changed: {source}")
        for listener in self.__listeners:
            listener.model_changed(source)

    def as_dict(self) -> dict[str, any]:
        return {
            "note_types": self.note_types,
            "selected_note_type": self.selected_note_type,
            "selected_fields": self.selected_fields,
            "run_op_callback_None": not self.run_op_callback
        }

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
