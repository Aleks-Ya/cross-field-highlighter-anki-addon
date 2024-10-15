import logging
from logging import Logger
from abc import abstractmethod
from typing import Callable, Optional

from cross_field_highlighter.highlighter.types import NoteTypeDetails, FieldNames
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogModelListener:
    @abstractmethod
    def model_changed(self, source: object):
        pass


class AdhocEraseDialogModel:
    def __init__(self):
        self.show: bool = False
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
