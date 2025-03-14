from typing import NewType

from anki.notes import Note

FieldName = NewType("FieldName", str)
FieldNames = NewType("FieldNames", list[FieldName])
FieldContent = NewType("FieldContent", str)
Word = NewType("Word", str)
Words = NewType("Words", list[Word])
Text = NewType("Text", str)
Notes = NewType("Notes", list[Note])
NoteTypeName = NewType("NoteTypeName", str)
Profile = NewType("Profile", str)
