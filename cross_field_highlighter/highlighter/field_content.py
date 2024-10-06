from .field_info import FieldInfo


class FieldContent:
    def __init__(self, field_info: FieldInfo, content: str):
        self.field_info: FieldInfo = field_info
        self.content: str = content
