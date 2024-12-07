import logging
from logging import Logger

from anki.models import NotetypeId

from .op_params import OpParams
from ...highlighter.types import FieldNames

log: Logger = logging.getLogger(__name__)


class EraseOpParams(OpParams):
    def __init__(self, note_type_id: NotetypeId, fields: FieldNames):
        super().__init__(note_type_id)
        self.fields: FieldNames = fields
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        fields: str = ", ".join([str(field) for field in self.fields])
        return f"EraseOpParams(note_type_id={self.note_type_id}, fields={fields})"

    def __eq__(self, other):
        if not isinstance(other, EraseOpParams):
            return False
        return self.note_type_id == other.note_type_id and self.fields == other.fields

    def __hash__(self):
        return hash((self.note_type_id, tuple(self.fields)))
