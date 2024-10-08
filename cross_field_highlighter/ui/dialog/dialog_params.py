from anki.models import NoteType, NotetypeId


class DialogParams:
    def __init__(self, note_types: dict[NotetypeId, NoteType]):
        self.note_types: dict[NotetypeId, NoteType] = note_types
