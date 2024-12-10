from pathlib import Path
from typing import Any

from anki.collection import Collection
from anki.decks import DeckId
from anki.models import NoteType, FieldDict
from anki.notes import Note, NoteId
from aqt import gui_hooks

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.highlighter.types import FieldContent, FieldName, Text


class DefaultFields:
    basic_front: FieldName = FieldName('Front')
    basic_back: FieldName = FieldName('Back')
    basic_extra: FieldName = FieldName('Extra')
    cloze_text: FieldName = FieldName('Text')
    cloze_extra: FieldName = FieldName('Back Extra')
    all_basic: list[FieldName] = [basic_front, basic_back, basic_extra]
    all_cloze: list[FieldName] = [cloze_text, cloze_extra]


class DefaultStopWords:
    in_config: str = "a an to"
    config: dict[str, str] = {"Default Stop Words": in_config}


class Case:
    def __init__(self, name: str, collocation: str, original_text: str, highlighted_text_space_delimited: str,
                 highlighted_text_non_space_delimited: str):
        self.name: str = name
        self.collocation: Text = Text(collocation)
        self.original_text: Text = Text(original_text)
        self.highlighted_text_space_delimited: Text = Text(highlighted_text_space_delimited)
        self.highlighted_text_non_space_delimited: Text = Text(highlighted_text_non_space_delimited)


class CaseNote:
    def __init__(self, note: Note, original_content: FieldContent, highlighted_content_space_delimited: FieldContent,
                 highlighted_content_non_space_delimited: FieldContent):
        self.note: Note = note
        self.original_content: FieldContent = original_content
        self.highlighted_content_space_delimited: FieldContent = highlighted_content_space_delimited
        self.highlighted_content_non_space_delimited: FieldContent = highlighted_content_non_space_delimited


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
                            extra_field_content: FieldContent = "Extra content",
                            new_note: bool = False) -> Note:
        note: Note = self.col.new_note(self.basic_note_type)
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
        note: Note = self.col.new_note(self.cloze_note_type)
        note[DefaultFields.cloze_text] = text_field_content
        note[DefaultFields.cloze_extra] = extra_field_content
        if not new_note:
            self.col.add_note(note, self.deck_id)
        gui_hooks.add_cards_did_add_note(note)
        return note

    def add_fields_to_note_type(self, note_type: NoteType, field_number: int, min_field_name_length: int) -> None:
        for i in range(field_number):
            new_field_name: str = f"Field {i + 1}"
            if len(new_field_name) < min_field_name_length:
                new_field_name += " " + "x" * (min_field_name_length - len(new_field_name) - 1)
            new_field_dict: FieldDict = self.col.models.new_field(new_field_name)
            self.col.models.add_field(note_type, new_field_dict)

    @staticmethod
    def stop_words() -> Text:
        return Text("to a an")

    @staticmethod
    def cases() -> list[Case]:
        return [
            Case("single word one time",
                 'beautiful',
                 'Hello, beautiful world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world!'),
            Case("single word several times",
                 'beautiful',
                 'Hello, beautiful world and beautiful day!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world and <b class="cross-field-highlighter">beautiful</b> day!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world and <b class="cross-field-highlighter">beautiful</b> day!'),
            Case("sub word",
                 'hip',
                 'Her children is at her hip.',
                 'Her children is at her <b class="cross-field-highlighter">hip</b>.',
                 'Her children is at her <b class="cross-field-highlighter">hip</b>.'),
            Case("case insensitive",
                 'beautiful',
                 'Hello, Beautiful world!',
                 'Hello, <b class="cross-field-highlighter">Beautiful</b> world!',
                 'Hello, <b class="cross-field-highlighter">Beautiful</b> world!'),
            Case("ing base", 'abstain',
                 'Abstaining from chocolate',
                 '<b class="cross-field-highlighter">Abstaining</b> from chocolate',
                 '<b class="cross-field-highlighter">Abstain</b>ing from chocolate'),
            Case("ing banging",
                 'overtake',
                 'A driver was overtaking a slower vehicle.',
                 'A driver was <b class="cross-field-highlighter">overtaking</b> a slower vehicle.',
                 'A driver was overtaking a slower vehicle.'),
            Case("ing changing short",
                 'lie',
                 'A cat was lying on the floor.',
                 'A cat was lying on the floor.',
                 'A cat was lying on the floor.'),
            Case("prefix to",
                 'to overtake',
                 'Driver was overtaking a slower vehicle.',
                 'Driver was <b class="cross-field-highlighter">overtaking</b> a slower vehicle.',
                 'Driver was overtaking a slower vehicle.'),
            Case("prefix a",
                 'a driver',
                 'Driver was overtaking a slower vehicle.',
                 '<b class="cross-field-highlighter">Driver</b> was overtaking a slower vehicle.',
                 '<b class="cross-field-highlighter">Driver</b> was overtaking a slower vehicle.'),
            Case("prefix an",
                 'an automobile',
                 'Automobile was overtaking a slower vehicle.',
                 '<b class="cross-field-highlighter">Automobile</b> was overtaking a slower vehicle.',
                 '<b class="cross-field-highlighter">Automobile</b> was overtaking a slower vehicle.'),
            Case("collocation",
                 'take forever',
                 'Downloading a movie takes forever.',
                 'Downloading a movie <b class="cross-field-highlighter">takes</b> <b class="cross-field-highlighter">forever</b>.',
                 'Downloading a movie <b class="cross-field-highlighter">take</b>s <b class="cross-field-highlighter">forever</b>.'),
            Case("tag li",
                 'lid',
                 '<li>I opened the lid of the jar to get some jam.</li>',
                 '<li>I opened the <b class="cross-field-highlighter">lid</b> of the jar to get some jam.</li>',
                 '<li>I opened the <b class="cross-field-highlighter">lid</b> of the jar to get some jam.</li>'),
            Case("tag div",
                 'ivy',
                 '<li><div>There is ivy trailing all over the wall.</div></li>',
                 '<li><div>There is <b class="cross-field-highlighter">ivy</b> trailing all over the wall.</div></li>',
                 '<li><div>There is <b class="cross-field-highlighter">ivy</b> trailing all over the wall.</div></li>'),
            Case("the beginning of a sentence",
                 'hello',
                 'Hello beautiful world!',
                 '<b class="cross-field-highlighter">Hello</b> beautiful world!',
                 '<b class="cross-field-highlighter">Hello</b> beautiful world!'),
            Case("collocation touches tag",
                 'hello',
                 '<li>Hello, beautiful world!</li>',
                 '<li><b class="cross-field-highlighter">Hello</b>, beautiful world!</li>',
                 '<li><b class="cross-field-highlighter">Hello</b>, beautiful world!</li>'),
            Case("tag contains spaces",
                 'hello',
                 '<p class="big">Hello, beautiful world!</p>',
                 '<p class="big"><b class="cross-field-highlighter">Hello</b>, beautiful world!</p>',
                 '<p class="big"><b class="cross-field-highlighter">Hello</b>, beautiful world!</p>'),
            Case("collocation within a tag",
                 'hello',
                 '<p class="hello">Hello, beautiful world!</p>',
                 '<p class="hello"><b class="cross-field-highlighter">Hello</b>, beautiful world!</p>',
                 '<p class="hello"><b class="cross-field-highlighter">Hello</b>, beautiful world!</p>'),
            Case("non-breakable space",
                 'beautiful',
                 'Hello,&nbsp;beautiful&nbsp;world!',
                 'Hello,&nbsp;<b class="cross-field-highlighter">beautiful</b>&nbsp;world!',
                 'Hello,&nbsp;<b class="cross-field-highlighter">beautiful</b>&nbsp;world!'),
            Case("cloze note (entire)",
                 'study',
                 'I {{c1:study}} every day.',
                 'I {{c1:<b class="cross-field-highlighter">study</b>}} every day.',
                 'I {{c1:<b class="cross-field-highlighter">study</b>}} every day.'),
            Case("cloze note (sub-word)",
                 'study',
                 'He {{c2:also studies hard}} every day.',
                 'He {{c2:also <b class="cross-field-highlighter">studies</b> hard}} every day.',
                 'He {{c2:also studies hard}} every day.'),
            Case("empty collocation",
                 '',
                 'Hello, beautiful world!',
                 'Hello, beautiful world!',
                 'Hello, beautiful world!'),
            Case("HTML tags in collocation",
                 '<i>beautiful</i>',
                 'Hello, beautiful world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world!'),
            Case("HTML tags in collocation",
                 '<i>beautiful</i> <b>world</b>',
                 'Hello, <i>beautiful</i> world!',
                 'Hello, <i><b class="cross-field-highlighter">beautiful</b></i> <b class="cross-field-highlighter">world</b>!',
                 'Hello, <i><b class="cross-field-highlighter">beautiful</b></i> <b class="cross-field-highlighter">world</b>!'),
            Case("furigana (ruby collocation, ruby text)",
                 '<ruby>東京<rt>とうきょう</rt></ruby>',
                 '<p><ruby>東京<rt>とうきょう</rt></ruby>は首都です。</p>',
                 '<p><ruby><b class="cross-field-highlighter">東京</b><rt><b class="cross-field-highlighter">とうきょう</b></rt></ruby>は首都です。</p>',
                 '<p><ruby><b class="cross-field-highlighter">東京</b><rt><b class="cross-field-highlighter">とうきょう</b></rt></ruby>は首都です。</p>'),
            Case("furigana (ruby collocation, brackets text)",
                 '<ruby>東京<rt>とうきょう</rt></ruby>',
                 '<p>東京[とうきょう]は首都です。</p>',
                 '<p><b class="cross-field-highlighter">東京</b>[<b class="cross-field-highlighter">とうきょう</b>]は首都です。</p>',
                 '<p><b class="cross-field-highlighter">東京</b>[<b class="cross-field-highlighter">とうきょう</b>]は首都です。</p>'),
            Case("furigana (brackets collocation, ruby text)",
                 '東京[とうきょう]',
                 '<p><ruby>東京<rt>とうきょう</rt></ruby>は首都です。</p>',
                 '<p><ruby><b class="cross-field-highlighter">東京</b><rt><b class="cross-field-highlighter">とうきょう</b></rt></ruby>は首都です。</p>',
                 '<p><ruby><b class="cross-field-highlighter">東京</b><rt><b class="cross-field-highlighter">とうきょう</b></rt></ruby>は首都です。</p>'),
            Case("forward slash in collocation",
                 'beautiful/nice',
                 'Hello, beautiful and nice world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> and <b class="cross-field-highlighter">nice</b> world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> and <b class="cross-field-highlighter">nice</b> world!'),
            Case("back slash in collocation",
                 'beautiful\\nice',
                 'Hello, beautiful and nice world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> and <b class="cross-field-highlighter">nice</b> world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> and <b class="cross-field-highlighter">nice</b> world!'),
            Case("angle brackets in collocation",
                 'beautiful>nice<perfect',
                 'Hello, beautiful, nice, and perfect world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b>, <b class="cross-field-highlighter">nice</b>, and <b class="cross-field-highlighter">perfect</b> world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b>, <b class="cross-field-highlighter">nice</b>, and <b class="cross-field-highlighter">perfect</b> world!'),
            Case("square brackets",
                 'beautiful',
                 'Hello, [beautiful] [world]!',
                 'Hello, [<b class="cross-field-highlighter">beautiful</b>] [world]!',
                 'Hello, [<b class="cross-field-highlighter">beautiful</b>] [world]!')
        ]

    def create_case_notes(self) -> list[CaseNote]:
        res: list[(NoteId, FieldContent, FieldContent)] = []
        for case in self.cases():
            collocation_content: FieldContent = FieldContent(case.collocation)
            original_content: FieldContent = FieldContent(case.original_text)
            highlighted_content_space_delimited: FieldContent = FieldContent(case.highlighted_text_space_delimited)
            highlighted_content_non_space_delimited: FieldContent = FieldContent(
                case.highlighted_text_non_space_delimited)
            note: Note = self.create_basic_note_1(FieldContent(collocation_content),
                                                  FieldContent(original_content))
            res.append(CaseNote(note, original_content, highlighted_content_space_delimited,
                                highlighted_content_non_space_delimited))
        return res

    def read_config(self) -> Config:
        return Config.from_path(self.config_json)

    def read_config_updated(self, overwrites: dict[str, Any]) -> Config:
        return Config.from_path_updated(self.config_json, overwrites)

    def assert_original_case_notes(self, case_notes: list[CaseNote]):
        for case_note in case_notes:
            act_note: Note = self.col.get_note(case_note.note.id)
            assert act_note[DefaultFields.basic_back] == case_note.original_content

    def assert_highlighted_case_notes(self, case_notes: list[CaseNote], space_delimited_language: bool):
        for case_note in case_notes:
            act_note: Note = self.col.get_note(case_note.note.id)
            act_content: str = act_note[DefaultFields.basic_back]
            if space_delimited_language:
                exp_content: FieldContent = case_note.highlighted_content_space_delimited
            else:
                exp_content: FieldContent = case_note.highlighted_content_non_space_delimited
            assert act_content == exp_content, f"Field content: '{act_content}' != '{exp_content}'"
