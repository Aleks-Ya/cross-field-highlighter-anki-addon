from anki.models import NotetypeId

from cross_field_highlighter.highlighter.types import FieldNames, NoteTypeName


class NoteTypeDetails:
    def __init__(self, note_type_id: NotetypeId, name: NoteTypeName, fields: FieldNames):
        self.note_type_id: NotetypeId = note_type_id
        self.name: NoteTypeName = name
        self.fields: FieldNames = fields

    def __str__(self):
        fields_str: str = ", ".join(self.fields)
        return f"NoteTypeDetails({self.note_type_id}, {self.name}, [{fields_str}])"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, NoteTypeDetails):
            return False
        return self.note_type_id == other.note_type_id and self.name == other.name and self.fields == other.fields
