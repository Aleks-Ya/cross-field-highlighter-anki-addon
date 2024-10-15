from anki.models import NotetypeId
from aqt import QWidget

from cross_field_highlighter.highlighter.types import FieldNames


class EraseOpParams:
    def __init__(self, note_type_id: NotetypeId, parent: QWidget, fields: FieldNames):
        self.note_type_id: NotetypeId = note_type_id
        self.parent: QWidget = parent
        self.fields: FieldNames = fields
