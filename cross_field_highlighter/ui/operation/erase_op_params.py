from typing import Optional

from anki.models import NotetypeId
from aqt import QWidget

from cross_field_highlighter.highlighter.types import FieldNames


class EraseOpParams:
    def __init__(self, note_type_id: NotetypeId, parent: Optional[QWidget], fields: FieldNames):
        self.note_type_id: NotetypeId = note_type_id
        self.parent: Optional[QWidget] = parent
        self.fields: FieldNames = fields

    def __str__(self):
        fields: str = ", ".join([str(field) for field in self.fields])
        return (f"EraseOpParams(note_type_id={self.note_type_id}, fields={fields})")

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, EraseOpParams):
            return False
        return (self.note_type_id == other.note_type_id and
                self.parent == other.parent and
                self.fields == other.fields)

    def __hash__(self):
        return hash((self.note_type_id, tuple(self.fields)))
