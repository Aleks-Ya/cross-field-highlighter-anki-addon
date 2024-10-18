from pathlib import Path
from typing import Any

from anki.collection import Collection
from anki.decks import DeckId
from anki.models import NoteType
from anki.notes import Note, NoteId
from aqt import gui_hooks

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.highlighter.types import FieldContent, FieldName, Text, Word


class DefaultFields:
    basic_front_field: FieldName = FieldName('Front')
    basic_back_field: FieldName = FieldName('Back')
    cloze_text_field: FieldName = FieldName('Text')
    cloze_extra_field: FieldName = FieldName('Back Extra')


class Case:
    def __init__(self, name: str, phrase: str, original_text: str, highlighted_text: str):
        self.name: str = name
        self.phrase: Text = Text(phrase)
        self.original_text: Text = Text(original_text)
        self.highlighted_text: Text = Text(highlighted_text)


class CaseNote:
    def __init__(self, note: Note, original_content: FieldContent, highlighted_content: FieldContent):
        self.note: Note = note
        self.original_content: FieldContent = original_content
        self.highlighted_content: FieldContent = highlighted_content


class Data:

    def __init__(self, col: Collection, module_dir: Path, basic_note_type: NoteType, cloze_note_type: NoteType):
        self.col: Collection = col
        self.basic_note_type: NoteType = basic_note_type
        self.cloze_note_type: NoteType = cloze_note_type
        self.deck_id: DeckId = self.col.decks.get_current_id()
        self.config_json: Path = module_dir.joinpath("config.json")

    def create_basic_note_1(self,
                            front_field_content: FieldContent = "Word content",
                            back_field_content: FieldContent = "Text content",
                            new_note: bool = False) -> Note:
        note: Note = self.col.new_note(self.basic_note_type)
        note[DefaultFields.basic_front_field] = front_field_content
        note[DefaultFields.basic_back_field] = back_field_content
        if not new_note:
            self.col.add_note(note, self.deck_id)
        gui_hooks.add_cards_did_add_note(note)
        return note

    def create_basic_note_2(self,
                            front_field_content: FieldContent = "Front content 2",
                            back_field_content: FieldContent = "Back content 2",
                            new_note: bool = False) -> Note:
        return self.create_basic_note_1(front_field_content=front_field_content,
                                        back_field_content=back_field_content,
                                        new_note=new_note)

    def create_cloze_note(self,
                          text_field_content: FieldContent = "Text content",
                          extra_field_content: FieldContent = "Extra content",
                          new_note: bool = False) -> Note:
        note: Note = self.col.new_note(self.cloze_note_type)
        note[DefaultFields.cloze_text_field] = text_field_content
        note[DefaultFields.cloze_extra_field] = extra_field_content
        if not new_note:
            self.col.add_note(note, self.deck_id)
        gui_hooks.add_cards_did_add_note(note)
        return note

    def create_note(self, new_note: bool = False) -> Note:
        return self.create_basic_note_1(FieldContent('Front field content'),
                                        FieldContent('Back field content'),
                                        new_note)

    @staticmethod
    def stop_words() -> set[Word]:
        return {Word("to"), Word("a"), Word("an")}

    @staticmethod
    def cases() -> list[Case]:
        return [
            Case("single word",
                 'beautiful',
                 'Hello, beautiful world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world!'),
            Case("several words",
                 'beautiful',
                 'Hello, beautiful world and beautiful day!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world and <b class="cross-field-highlighter">beautiful</b> day!'),
            Case("sub word",
                 'hip',
                 'Her children is at her hip.',
                 'Her children is at her <b class="cross-field-highlighter">hip</b>.'),
            Case("case insensitive",
                 'beautiful',
                 'Hello, Beautiful world!',
                 'Hello, <b class="cross-field-highlighter">Beautiful</b> world!'),
            Case("ing base", 'abstain',
                 'Abstaining from chocolate',
                 '<b class="cross-field-highlighter">Abstaining</b> from chocolate'),
            Case("ing banging",
                 'overtake',
                 'A driver was overtaking a slower vehicle.',
                 'A driver was <b class="cross-field-highlighter">overtaking</b> a slower vehicle.'),
            Case("ing changing short",
                 'lie',
                 'A cat was lying on the floor.',
                 'A cat was lying on the floor.'),
            Case("prefix to",
                 'to overtake',
                 'Driver was overtaking a slower vehicle.',
                 'Driver was <b class="cross-field-highlighter">overtaking</b> a slower vehicle.'),
            Case("prefix a",
                 'a driver',
                 'Driver was overtaking a slower vehicle.',
                 '<b class="cross-field-highlighter">Driver</b> was overtaking a slower vehicle.'),
            Case("prefix an",
                 'an automobile',
                 'Automobile was overtaking a slower vehicle.',
                 '<b class="cross-field-highlighter">Automobile</b> was overtaking a slower vehicle.'),
            Case("collocation",
                 'take forever',
                 'Downloading a movie takes forever.',
                 'Downloading a movie <b class="cross-field-highlighter">takes</b> <b class="cross-field-highlighter">forever</b>.'),
            Case("tag li",
                 'lid',
                 '<li>I opened the lid of the jar to get some jam.</li>',
                 '<li>I opened the <b class="cross-field-highlighter">lid</b> of the jar to get some jam.</li>'),
            Case("tag div",
                 'ivy',
                 '<li><div>There is ivy trailing all over the wall.</div></li>',
                 '<li><div>There is <b class="cross-field-highlighter">ivy</b> trailing all over the wall.</div></li>')
        ]

    def create_case_notes(self) -> list[CaseNote]:
        res: list[(NoteId, FieldContent, FieldContent)] = []
        for case in self.cases():
            phrase_content: FieldContent = FieldContent(case.phrase)
            original_content: FieldContent = FieldContent(case.original_text)
            highlighted_content: FieldContent = FieldContent(case.highlighted_text)
            note: Note = self.create_basic_note_1(FieldContent(phrase_content),
                                                  FieldContent(original_content))
            res.append(CaseNote(note, original_content, highlighted_content))
        return res

    def read_config(self) -> Config:
        return Config.from_path(self.config_json)

    def read_config_updated(self, overwrites: dict[str, Any]) -> Config:
        return Config.from_path_updated(self.config_json, overwrites)
