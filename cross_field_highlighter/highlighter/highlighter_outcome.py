from .destination import Destination
from .field_content import FieldContent


class HighlighterOutcome:
    def __init__(self, fields: dict[Destination, FieldContent]):
        self.fields: dict[Destination, FieldContent] = fields
