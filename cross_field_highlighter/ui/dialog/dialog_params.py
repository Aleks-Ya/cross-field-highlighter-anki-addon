from typing import Sequence

from anki.notes import NoteId

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails


class DialogParams:
    def __init__(self, note_types: list[NoteTypeDetails], note_ids: Sequence[NoteId]):
        self.note_types: list[NoteTypeDetails] = note_types
        self.note_ids: Sequence[NoteId] = note_ids

    def __str__(self):
        note_types_str: str = ', '.join(str(note_type) for note_type in self.note_types)
        return f"DialogParams(note_types=[{note_types_str}])"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.note_types == other.note_types
