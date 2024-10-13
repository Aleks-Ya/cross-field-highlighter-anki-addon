from abc import abstractmethod
from typing import Optional, Callable

from aqt import QWidget

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import NoteTypeDetails, FieldName


class AdhocHighlightDialogModelListener:
    @abstractmethod
    def model_changed(self):
        pass


class AdhocHighlightDialogModel:
    def __init__(self):
        self.show: bool = False
        self.note_types: list[NoteTypeDetails] = []
        self.selected_note_type: Optional[NoteTypeDetails] = None
        self.selected_source_field: Optional[FieldName] = None
        self.selected_format: Optional[HighlightFormat] = None
        self.selected_destination_field: Optional[FieldName] = None
        self.run_op_callback: Optional[
            Callable[[QWidget, FieldName, FieldName, set[str], HighlightFormat], None]] = None
        self.__listeners: set[AdhocHighlightDialogModelListener] = set()

    def add_listener(self, listener: AdhocHighlightDialogModelListener):
        self.__listeners.add(listener)

    def fire_model_changed(self):
        for listener in self.__listeners:
            listener.model_changed()
