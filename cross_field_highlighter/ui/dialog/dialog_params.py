from cross_field_highlighter.highlighter.types import NoteTypeDetails


class DialogParams:
    def __init__(self, note_types: list[NoteTypeDetails]):
        self.note_types: list[NoteTypeDetails] = note_types

    def __str__(self):
        note_types_str: str = ', '.join(str(note_type) for note_type in self.note_types)
        return f"DialogParams(note_types=[{note_types_str}])"
