from anki.collection import Collection
from anki.decks import DeckId
from anki.models import NoteType
from anki.notes import Note
from aqt import gui_hooks

from cross_field_highlighter.highlighter.types import FieldContent, FieldName


class DefaultFields:
    word_field_name: FieldName = FieldName('Front')
    text_field_name: FieldName = FieldName('Back')


class Data:

    def __init__(self, col: Collection):
        self.col: Collection = col
        self.note_type: NoteType = self.col.models.by_name('Basic')
        self.deck_id: DeckId = self.col.decks.get_current_id()

    def create_note_with_fields(self,
                                word_field_content: str = "Word content",
                                text_field_content: str = "Text content",
                                new_note: bool = False) -> Note:
        word_field_content: FieldContent = FieldContent(word_field_content)
        text_field_content: FieldContent = FieldContent(text_field_content)
        note: Note = self.col.new_note(self.note_type)
        note[DefaultFields.word_field_name] = word_field_content
        note[DefaultFields.text_field_name] = text_field_content
        if not new_note:
            self.col.add_note(note, self.deck_id)
        gui_hooks.add_cards_did_add_note(note)
        return note

    def create_note(self, new_note: bool = False) -> Note:
        return self.create_note_with_fields('Front field content',
                                            'Back field content',
                                            new_note)
