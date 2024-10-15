from aqt import QWidget

from cross_field_highlighter.highlighter.types import FieldNames


class EraseOpParams:
    def __init__(self, parent: QWidget, fields: FieldNames):
        self.parent: QWidget = parent
        self.fields: FieldNames = fields
