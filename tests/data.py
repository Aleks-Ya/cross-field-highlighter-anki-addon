from pathlib import Path

from anki.collection import Collection
from anki.decks import DeckId
from anki.models import NoteType, FieldDict
from anki.notes import Note, NoteId
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


class DefaultConfig:
    stop_words: str = "a an to"
    highlight_shortcut: str = "Ctrl+Shift+H"
    erase_shortcut: str = ""
    highlight: dict[str, str] = {"Default Stop Words": stop_words, "Editor Shortcut": highlight_shortcut}
    erase: dict[str, str] = {"Editor Shortcut": erase_shortcut}


class DefaultTags:
    latest_modified: str = "cross-field-highlighter::modified-by-latest-run"


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
        return [
            Case("General: single word repeats one time",
                 'beautiful',
                 'Hello, beautiful world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world!'),
            Case("General: single word repeats several times",
                 'beautiful',
                 'Hello, beautiful world and beautiful day!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world and <b class="cross-field-highlighter">beautiful</b> day!'),
            Case("General: case insensitive",
                 'beautiful',
                 'Hello, Beautiful world!',
                 'Hello, <b class="cross-field-highlighter">Beautiful</b> world!'),
            Case("General: collocation",
                 'take forever',
                 'Downloading a movie takes forever.',
                 'Downloading a movie <b class="cross-field-highlighter">takes</b> <b class="cross-field-highlighter">forever</b>.'),
            Case("General: the beginning of a sentence",
                 'hello',
                 'Hello beautiful world!',
                 '<b class="cross-field-highlighter">Hello</b> beautiful world!'),
            Case("General: empty collocation",
                 '',
                 'Hello, beautiful world!',
                 'Hello, beautiful world!'),
            Case("General: entire collocation as token (+case insensitive)",
                 'to hurry up',
                 'Need to hurry up. He Hurries everyone up.',
                 'Need to <b class="cross-field-highlighter">hurry</b> <b class="cross-field-highlighter">up</b>. He <b class="cross-field-highlighter">Hurries</b> everyone <b class="cross-field-highlighter">up</b>.'),
            Case("Word forms: s-suffix",
                 'intrusion',
                 'Resistant to intrusions.',
                 'Resistant to <b class="cross-field-highlighter">intrusions</b>.'),
            Case("Word forms: ing base (append)",
                 'drown',
                 'Protection against drowning.',
                 'Protection against <b class="cross-field-highlighter">drowning</b>.'),
            Case("Word forms: ing base (case insensitive)",
                 'abstain',
                 'Abstaining from chocolate',
                 '<b class="cross-field-highlighter">Abstaining</b> from chocolate'),
            Case("Word forms: ing (dropping e)",
                 'overtake',
                 'A driver was overtaking a slower vehicle.',
                 'A driver was <b class="cross-field-highlighter">overtaking</b> a slower vehicle.'),
            Case("Word forms: ing (ie-ending)",
                 'lie',
                 'A cat was lying on the floor.',
                 'A cat was lying on the floor.'),
            Case("Word forms: forgotten",
                 'forget',
                 "I've forgotten your name.",
                 '''I've <b class="cross-field-highlighter">forgotten</b> your name.'''),
            Case("Word forms: forgetting",
                 'forget',
                 "I am forgetting my keys again.",
                 'I am <b class="cross-field-highlighter">forgetting</b> my keys again.'),
            Case("Short words: be",
                 'be',
                 'To be is to have been while being beautiful.',
                 'To <b class="cross-field-highlighter">be</b> is to have <b class="cross-field-highlighter">been</b> while <b class="cross-field-highlighter">being</b> beautiful.'),
            Case("Short words: minimum length (should not highlight 'our')",
                 'phase out',
                 'Our meetings phased out last year.',
                 'Our meetings <b class="cross-field-highlighter">phased</b> <b class="cross-field-highlighter">out</b> last year.'),
            Case("Short words: limit max length (should not highlight 'society')",
                 'so',
                 "Society changes so quickly.",
                 'Society changes <b class="cross-field-highlighter">so</b> quickly.'),
            Case("Stop words: to",
                 'to overtake',
                 'Driver was overtaking a slower vehicle.',
                 'Driver was <b class="cross-field-highlighter">overtaking</b> a slower vehicle.'),
            Case("Stop words: a",
                 'a driver',
                 'Driver was overtaking a slower vehicle.',
                 '<b class="cross-field-highlighter">Driver</b> was overtaking a slower vehicle.'),
            Case("Stop words: an",
                 'an automobile',
                 'Automobile was overtaking a slower vehicle.',
                 '<b class="cross-field-highlighter">Automobile</b> was overtaking a slower vehicle.'),
            Case("Stop words: entire collocation comprises stop words",
                 'an a to',
                 'An automobile is going to overtake a slower vehicle.',
                 'An automobile is going to overtake a slower vehicle.'),
            Case("Short words: should not highlight 'Measure'",
                 'mesh',
                 "Measure and mark the mesh size.",
                 'Measure and mark the <b class="cross-field-highlighter">mesh</b> size.'),
            Case("HTML tags: li",
                 'lid',
                 '<li>I opened the lid of the jar to get some jam.</li>',
                 '<li>I opened the <b class="cross-field-highlighter">lid</b> of the jar to get some jam.</li>'),
            Case("HTML tags: div",
                 'ivy',
                 '<li><div>There is ivy trailing all over the wall.</div></li>',
                 '<li><div>There is <b class="cross-field-highlighter">ivy</b> trailing all over the wall.</div></li>'),
            Case("HTML tags: collocation touches tag",
                 'hello',
                 '<li>Hello, beautiful world!</li>',
                 '<li><b class="cross-field-highlighter">Hello</b>, beautiful world!</li>'),
            Case("HTML tags: tag contains spaces",
                 'hello',
                 '<p class="big">Hello, beautiful world!</p>',
                 '<p class="big"><b class="cross-field-highlighter">Hello</b>, beautiful world!</p>'),
            Case("HTML tags: tag contains collocation",
                 'hello',
                 '<p class="hello">Hello, beautiful world!</p>',
                 '<p class="hello"><b class="cross-field-highlighter">Hello</b>, beautiful world!</p>'),
            Case("HTML tags: non-breakable space",
                 'beautiful',
                 'Hello,&nbsp;beautiful&nbsp;world!',
                 'Hello,&nbsp;<b class="cross-field-highlighter">beautiful</b>&nbsp;world!'),
            Case("HTML tags: tag in collocation",
                 '<i>beautiful</i>',
                 'Hello, beautiful world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> world!'),
            Case("HTML tags: tags in collocation",
                 '<i>beautiful</i> <b>world</b>',
                 'Hello, <i>beautiful</i> world!',
                 'Hello, <i><b class="cross-field-highlighter">beautiful</b></i> <b class="cross-field-highlighter">world</b>!'),
            Case("Cloze note: entire",
                 'study',
                 'I {{c1:study}} every day.',
                 'I {{c1:<b class="cross-field-highlighter">study</b>}} every day.'),
            Case("Cloze note: sub-word",
                 'study',
                 'He {{c2:also studies hard}} every day.',
                 'He {{c2:also <b class="cross-field-highlighter">studies</b> hard}} every day.'),
            Case("Furigana: ruby collocation, ruby text",
                 '<ruby>東京<rt>とうきょう</rt></ruby>',
                 '<p><ruby>東京<rt>とうきょう</rt></ruby>は首都です。</p>',
                 '<p><ruby><b class="cross-field-highlighter">東京</b><rt><b class="cross-field-highlighter">とうきょう</b></rt></ruby>は首都です。</p>'),
            Case("Furigana: ruby collocation, brackets text",
                 '<ruby>東京<rt>とうきょう</rt></ruby>',
                 '<p>東京[とうきょう]は首都です。</p>',
                 '<p><b class="cross-field-highlighter">東京</b>[<b class="cross-field-highlighter">とうきょう</b>]は首都です。</p>'),
            Case("Furigana: brackets collocation, ruby text",
                 '東京[とうきょう]',
                 '<p><ruby>東京<rt>とうきょう</rt></ruby>は首都です。</p>',
                 '<p><ruby><b class="cross-field-highlighter">東京</b><rt><b class="cross-field-highlighter">とうきょう</b></rt></ruby>は首都です。</p>'),
            Case("Furigana: brackets collocation, brackets text",
                 '東京[とうきょう]',
                 '<p>東京[とうきょう]は首都です。</p>',
                 '<p><b class="cross-field-highlighter">東京[とうきょう]</b>は首都です。</p>'),
            Case("Special symbols: collocation touches dot",
                 'hip',
                 'Her child is at her hip.',
                 'Her child is at her <b class="cross-field-highlighter">hip</b>.'),
            Case("Special symbols: collocation contains forward slash",
                 'beautiful/nice',
                 'Hello, beautiful and nice world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> and <b class="cross-field-highlighter">nice</b> world!'),
            Case("Special symbols: collocation contains back slash",
                 'beautiful\\nice',
                 'Hello, beautiful and nice world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b> and <b class="cross-field-highlighter">nice</b> world!'),
            Case("Special symbols: collocation contains angle brackets",
                 'beautiful>nice<perfect',
                 'Hello, beautiful, nice, and perfect world!',
                 'Hello, <b class="cross-field-highlighter">beautiful</b>, <b class="cross-field-highlighter">nice</b>, and <b class="cross-field-highlighter">perfect</b> world!'),
            Case("Special symbols: collocation contains square brackets",
                 'beautiful[nice]',
                 'Hello, [beautiful] and nice [world]!',
                 'Hello, [<b class="cross-field-highlighter">beautiful</b>] and <b class="cross-field-highlighter">nice</b> [world]!'),
            Case("Special symbols: curly quotes (smart quites)",
                 'rally',
                 'It is a “rally.”',
                 'It is a “<b class="cross-field-highlighter">rally</b>.”'),
            Case("Thai language",
                 'ดี',
                 'วันนี้เป็นวันที่ดีมาก',
                 'วันนี้เป็นวันที่<b class="cross-field-highlighter">ดี</b>มาก'),
            Case("Korean language",
                 '좋은',
                 '오늘은 정말 좋은 날이에요',
                 '오늘은 정말 <b class="cross-field-highlighter">좋은</b> 날이에요'),
            Case("Chinese language",
                 '天气',
                 '今天天气非常好',
                 '今天<b class="cross-field-highlighter">天气</b>非常好'),
            Case("Arabic language",
                 'جميل',
                 'الطقس اليوم جميل',
                 'الطقس اليوم <b class="cross-field-highlighter">جميل</b>'),
            Case("Hebrew language",
                 'נהדר',
                 'היום יום נהדר',
                 'היום יום <b class="cross-field-highlighter">נהדר</b>')
        ]

    def create_case_notes(self) -> list[CaseNote]:
        res: list[(NoteId, FieldContent, FieldContent)] = []
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
