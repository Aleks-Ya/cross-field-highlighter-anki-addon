from pathlib import Path

import yaml
from anki.collection import Collection
from anki.decks import DeckId
from anki.models import NoteType, FieldDict
from anki.notes import Note
from aqt import gui_hooks

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.types import FieldContent, FieldName, Text


class DefaultFields:
    basic_front: FieldName = FieldName('Front')
    basic_back: FieldName = FieldName('Back')
    basic_extra: FieldName = FieldName('Extra')
    cloze_text: FieldName = FieldName('Text')
    cloze_back_extra: FieldName = FieldName('Back Extra')
    all_basic: list[FieldName] = [basic_front, basic_back, basic_extra]
    all_cloze: list[FieldName] = [cloze_text, cloze_back_extra]


class DefaultTags:
    latest_modified: str = "cross-field-highlighter::modified-by-latest-run"


class DefaultConfig:
    default_stop_words: str = "a an to"
    highlight_shortcut: str = "Ctrl+Shift+H"
    erase_shortcut: str = ""
    highlight: dict[str, str] = {"Default Stop Words": default_stop_words, "Editor Shortcut": highlight_shortcut}
    erase: dict[str, str] = {"Editor Shortcut": erase_shortcut}
    loader: dict = {
        'Dialog': {'Adhoc': {
            "Highlight": {**highlight},
            "Erase": {**erase}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}


class DefaultModel:
    default_highlight: dict = {'all_note_types': [],
                               'selected_note_types': [],
                               'default_stop_words': None,
                               'note_number': 0,
                               'formats': [],
                               'accept_callback_None': True,
                               'reject_callback_None': True,
                               'current_state': None,
                               'states': {}}
    default_erase: dict = {'all_note_types': [],
                           'selected_note_types': [],
                           'note_number': 0,
                           'accept_callback_None': True,
                           'reject_callback_None': True,
                           'current_state': None,
                           'states': {}}


class Case:
    def __init__(self, name: str, collocation: str, original_text: str, highlighted_text: str):
        self.name: str = name
        self.collocation: Text = Text(collocation)
        self.original_text: Text = Text(original_text)
        self.highlighted_text: Text = Text(highlighted_text)


class CaseNote:
    def __init__(self, note: Note, original_content: FieldContent, highlighted_content: FieldContent):
        self.note: Note = note
        self.original_content: FieldContent = original_content
        self.highlighted_content: FieldContent = highlighted_content


class Data:

    def __init__(self, col: Collection, module_dir: Path, note_type_basic: NoteType, note_type_cloze: NoteType,
                 config_loader: ConfigLoader):
        self.col: Collection = col
        self.note_type_basic: NoteType = note_type_basic
        self.note_type_cloze: NoteType = note_type_cloze
        self.config_loader: ConfigLoader = config_loader
        self.deck_id: DeckId = self.col.decks.get_current_id()
        self.config_json: Path = module_dir.joinpath("config.json")

    def create_basic_note_1(self,
                            front_field_content: FieldContent = "Word content",
                            back_field_content: FieldContent = "Text content",
                            extra_field_content: FieldContent = "Extra content",
                            new_note: bool = False) -> Note:
        note: Note = self.col.new_note(self.note_type_basic)
        note[DefaultFields.basic_front] = front_field_content
        note[DefaultFields.basic_back] = back_field_content
        note[DefaultFields.basic_extra] = extra_field_content
        if not new_note:
            self.col.add_note(note, self.deck_id)
        gui_hooks.add_cards_did_add_note(note)
        return note

    def create_basic_note_2(self,
                            front_field_content: FieldContent = "Front content 2",
                            back_field_content: FieldContent = "Back content 2",
                            extra_field_content: FieldContent = "Extra content 2",
                            new_note: bool = False) -> Note:
        return self.create_basic_note_1(front_field_content=front_field_content,
                                        back_field_content=back_field_content,
                                        extra_field_content=extra_field_content,
                                        new_note=new_note)

    def create_cloze_note(self,
                          text_field_content: FieldContent = "Text content",
                          extra_field_content: FieldContent = "Extra content",
                          new_note: bool = False) -> Note:
        note: Note = self.col.new_note(self.note_type_cloze)
        note[DefaultFields.cloze_text] = text_field_content
        note[DefaultFields.cloze_back_extra] = extra_field_content
        if not new_note:
            self.col.add_note(note, self.deck_id)
        gui_hooks.add_cards_did_add_note(note)
        return note

    def add_fields_to_note_type(self, note_type: NoteType, field_number: int, min_field_name_length: int) -> None:
        for i in range(field_number):
            new_field_name: str = f"Field {i + 1}"
            if len(new_field_name) < min_field_name_length:
                new_field_name += " " + "x" * (min_field_name_length - len(new_field_name) - 2) + "S"
            new_field_dict: FieldDict = self.col.models.new_field(new_field_name)
            self.col.models.add_field(note_type, new_field_dict)

    @staticmethod
    def stop_words() -> Text:
        return Text("to a an")

    @staticmethod
    def cases() -> list[Case]:
        yaml_file: Path = Path(__file__).parent / "cases.yaml"
        with open(yaml_file, encoding="utf-8") as f:
            data: list[dict] = yaml.safe_load(f)
        return [Case(c["name"], c["collocation"], c["original_text"], c["highlighted_text"]) for c in data]

    def create_case_notes(self) -> list[CaseNote]:
        res: list[CaseNote] = []
        for case in self.cases():
            collocation_content: FieldContent = FieldContent(case.collocation)
            original_content: FieldContent = FieldContent(case.original_text)
            highlighted_content: FieldContent = FieldContent(case.highlighted_text)
            note: Note = self.create_basic_note_1(FieldContent(collocation_content),
                                                  FieldContent(original_content))
            res.append(CaseNote(note, original_content, highlighted_content))
        return res

    def read_config(self) -> Config:
        return Config(self.config_loader)

    def assert_original_case_notes(self, case_notes: list[CaseNote]):
        for case_note in case_notes:
            act_note: Note = self.col.get_note(case_note.note.id)
            assert act_note[DefaultFields.basic_back] == case_note.original_content

    def assert_highlighted_case_notes(self, case_notes: list[CaseNote]):
        for case_note in case_notes:
            act_note: Note = self.col.get_note(case_note.note.id)
            act_content: str = act_note[DefaultFields.basic_back]
            exp_content: FieldContent = case_note.highlighted_content
            assert act_content == exp_content, f"Field content: '{act_content}' != '{exp_content}'"
            act_tags: list[str] = act_note.tags
            was_modified: bool = act_content != case_note.original_content
            exp_tags: list[str] = [DefaultTags.latest_modified] if was_modified else []
            assert act_tags == exp_tags, f"Tags: '{act_tags}' != '{exp_tags}'"
