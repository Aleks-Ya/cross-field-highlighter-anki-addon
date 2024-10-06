from anki.notes import NoteId

from .field_info import FieldInfo


class Source:
    def __init__(self, note_id: NoteId, field_info: FieldInfo):
        self.note_id: NoteId = note_id
        self.field_info: FieldInfo = field_info
