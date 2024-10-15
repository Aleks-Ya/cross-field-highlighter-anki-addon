from typing import NewType

from anki.models import NotetypeId
from anki.notes import Note

FieldName = NewType("FieldName", str)
FieldNames = NewType("FieldNames", list[FieldName])
FieldContent = NewType("FieldContent", str)
Word = NewType("Word", str)
Text = NewType("Text", str)
Notes = NewType("Notes", list[Note])


class NoteTypeDetails:
    def __init__(self, note_type_id: NotetypeId, name: str, fields: FieldNames):
        self.note_type_id: NotetypeId = note_type_id
        self.name: str = name
        self.fields: FieldNames = fields

    def __str__(self):
        fields_str: str = ", ".join(self.fields)
        return f"NoteTypeDetails(note_type_id={self.note_type_id}, name='{self.name}', fields=[{fields_str}])"

    def __repr__(self):
        return self.__str__()
