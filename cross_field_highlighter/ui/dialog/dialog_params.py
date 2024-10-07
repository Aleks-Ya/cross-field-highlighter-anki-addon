from anki.models import NotetypeId

from ...highlighter.types import FieldName


class DialogParams:
    def __init__(self, field_type_to_field_name: dict[NotetypeId, list[FieldName]]):
        self.field_type_to_field_name: dict[NotetypeId, list[FieldName]] = field_type_to_field_name
