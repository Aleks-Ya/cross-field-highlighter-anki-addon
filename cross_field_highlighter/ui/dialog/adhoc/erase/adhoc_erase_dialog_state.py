import logging
from logging import Logger

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogState:
    def __init__(self, note_type_details: NoteTypeDetails):
        self.__selected_note_type: NoteTypeDetails = note_type_details
        self.__selected_fields: FieldNames = FieldNames([])
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_selected_note_type(self) -> NoteTypeDetails:
        return self.__selected_note_type

    def get_selected_fields(self) -> FieldNames:
        return self.__selected_fields

    def select_fields(self, field_names: FieldNames) -> None:
        existing_field_names: FieldNames = FieldNames(
            [field_name for field_name in field_names
             if self.__selected_note_type and field_name in self.__selected_note_type.fields])
        self.__selected_fields = existing_field_names

    def as_dict(self) -> dict[str, any]:
        return {
            "selected_note_type": self.__selected_note_type,
            "selected_fields": self.__selected_fields
        }

    def __repr__(self):
        return str(self.as_dict())

    def __eq__(self, other):
        if not isinstance(other, AdhocEraseDialogState):
            return False
        return self.as_dict() == other.as_dict()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
