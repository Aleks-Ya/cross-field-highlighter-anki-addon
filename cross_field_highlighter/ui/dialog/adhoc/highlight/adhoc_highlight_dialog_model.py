import logging
from logging import Logger
from abc import abstractmethod
from typing import Optional, Callable

from anki.notes import NoteId

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldName, FieldNames
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogModelListener:
    @abstractmethod
    def model_changed(self, source: object):
        pass


class AdhocHighlightDialogModel:
    def __init__(self):
        self.show: bool = False
        self.note_types: list[NoteTypeDetails] = []
        self.note_ids: set[NoteId] = set()
        self.formats: list[HighlightFormat] = []
        self.selected_note_type: Optional[NoteTypeDetails] = None
        self.selected_source_field: Optional[FieldName] = None
        self.selected_format: Optional[HighlightFormat] = None
        self.selected_destination_fields: FieldNames = FieldNames([])
        self.run_op_callback: Optional[Callable[[HighlightOpParams], None]] = None
        self.__listeners: set[AdhocHighlightDialogModelListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def add_listener(self, listener: AdhocHighlightDialogModelListener):
        self.__listeners.add(listener)

    def fire_model_changed(self, source: object):
        for listener in self.__listeners:
            listener.model_changed(source)
