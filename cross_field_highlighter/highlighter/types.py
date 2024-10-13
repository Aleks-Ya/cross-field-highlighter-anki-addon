from typing import NewType

from anki.models import NotetypeId

FieldName = NewType("FieldName", str)
FieldNames = NewType("FieldNames", list[FieldName])
FieldContent = NewType("FieldContent", str)
Word = NewType("Word", str)
Text = NewType("Text", str)


class NoteTypeDetails:
    note_type_id: NotetypeId
    name: str
    fields: FieldNames

    def __str__(self):
        fields_str: str = ", ".join(self.fields)
        return f"NoteTypeDetails(note_type_id={self.note_type_id}, name='{self.name}', fields=[{fields_str}])"

    def __repr__(self):
        return self.__str__()
