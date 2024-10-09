from typing import NewType

from anki.models import NotetypeId

FieldName = NewType("FieldName", str)


class NoteTypeDetails:
    note_type_id: NotetypeId
    name: str
    fields: list[FieldName]

    def __str__(self):
        fields_str: str = ", ".join(self.fields)
        return f"NoteTypeDetails(note_type_id={self.note_type_id}, name='{self.name}', fields=[{fields_str}])"
