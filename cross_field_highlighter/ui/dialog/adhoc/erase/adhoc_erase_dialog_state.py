import logging
from logging import Logger
from typing import Optional

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogState:
    def __init__(self):
        self.selected_note_type: Optional[NoteTypeDetails] = None
        self.selected_fields: FieldNames = FieldNames([])
        log.debug(f"{self.__class__.__name__} was instantiated")

    def as_dict(self) -> dict[str, any]:
        return {
            "selected_note_type": self.selected_note_type,
            "selected_fields": self.selected_fields
        }

    def __repr__(self):
        return str(self.as_dict())

    def __eq__(self, other):
        if not isinstance(other, AdhocEraseDialogState):
            return False
        return self.as_dict() == other.as_dict()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
