import logging
from logging import Logger

from ...highlighter.note_type_details import NoteTypeDetails

log: Logger = logging.getLogger(__name__)


class DialogParams:
    def __init__(self, note_types: list[NoteTypeDetails], note_number: int):
        self.note_types: list[NoteTypeDetails] = note_types
        self.note_number: int = note_number
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        note_types_str: str = ', '.join(str(note_type) for note_type in self.note_types)
        return f"DialogParams(note_types=[{note_types_str}], note_number={self.note_number})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.note_types == other.note_types and self.note_number == other.note_number

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
