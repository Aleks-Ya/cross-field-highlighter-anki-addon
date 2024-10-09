from anki.collection import Collection
from anki.notes import Note

from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.types import FieldContent
from tests.data import Data, DefaultFields


def __tests(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection,
            collocation: str, original: str, highlighted: str):
    note: Note = td.create_note_with_fields(FieldContent(collocation), FieldContent(original))
    stop_words: set[str] = {"to", "a", "an"}

    # Highlight 1st time
    note_act: Note = start_with_note_highlighter.highlight(note, DefaultFields.word_field_name,
                                                           DefaultFields.text_field_name, stop_words)
    assert note_act[DefaultFields.text_field_name] == highlighted

    # Highlight again
    note_act: Note = start_with_note_highlighter.highlight(note, DefaultFields.word_field_name,
                                                           DefaultFields.text_field_name, stop_words)
    assert note_act[DefaultFields.text_field_name] == highlighted

    # Erase
    note_act: Note = start_with_note_highlighter.erase(note, DefaultFields.text_field_name)
    assert note_act[DefaultFields.text_field_name] == original


def test_normal(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'beautiful',
            'Hello, beautiful world!',
            'Hello, <b>beautiful</b> world!')


def test_highlight_several_words(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'beautiful',
            'Hello, beautiful world and beautiful day!',
            'Hello, <b>beautiful</b> world and <b>beautiful</b> day!')


def test_sub_word(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'hip',
            'Her children is at her hip.',
            'Her children is at her <b>hip</b>.')


def test_case_insensitive(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'beautiful',
            'Hello, Beautiful world!',
            'Hello, <b>Beautiful</b> world!')


def test_ing_base(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'abstain',
            'Abstaining from chocolate',
            '<b>Abstaining</b> from chocolate')


def test_ing_banging(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'overtake',
            'A driver was overtaking a slower vehicle.',
            'A driver was <b>overtaking</b> a slower vehicle.')


def test_ing_changing_short(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'lie',
            'A cat was lying on the floor.',
            'A cat was lying on the floor.')


def test_prefix_to(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'to overtake',
            'Driver was overtaking a slower vehicle.',
            'Driver was <b>overtaking</b> a slower vehicle.')


def test_prefix_a(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'a driver',
            'Driver was overtaking a slower vehicle.',
            '<b>Driver</b> was overtaking a slower vehicle.')


def test_prefix_an(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'an automobile',
            'Automobile was overtaking a slower vehicle.',
            '<b>Automobile</b> was overtaking a slower vehicle.')


def test_collocation(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'take forever',
            'Downloading a movie takes forever.',
            'Downloading a movie <b>takes forever</b>.')


def test_tag_li(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'lid',
            '<li>I opened the lid of the jar to get some jam.</li>',
            '<li>I opened the <b>lid</b> of the jar to get some jam.</li>')


def test_tag_div(start_with_note_highlighter: StartWithNoteHighlighter, td: Data, col: Collection):
    __tests(start_with_note_highlighter, td, col,
            'ivy',
            '<li><div>There is ivy trailing all over the wall.</div></li>',
            '<li><div>There is <b>ivy</b> trailing all over the wall.</div></li>')
