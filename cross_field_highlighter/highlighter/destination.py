from .field_info import FieldInfo


class Destination:
    def __init__(self, fields: list[FieldInfo]):
        self.fields: list[FieldInfo] = fields
