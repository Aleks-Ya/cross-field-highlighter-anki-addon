from anki.collection import Collection
from anki.notes import Note, NoteId

from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.types import FieldContent
from tests.data import Data, DefaultFields


def __create_notes(td: Data, contents: list[(str, str, str)]) -> list[(NoteId, FieldContent, FieldContent)]:
    res: list[(NoteId, FieldContent, FieldContent)] = []
    for content_tuple in contents:
        word_content: FieldContent = FieldContent(content_tuple[0])
        original_content: FieldContent = FieldContent(content_tuple[1])
        highlighted_content: FieldContent = FieldContent(content_tuple[2])
        note: Note = td.create_note_with_fields(FieldContent(word_content), FieldContent(original_content))
        res.append((note.id, original_content, highlighted_content))
    return res


def __assert_highlighted_notes(col: Collection, contents: list[(NoteId, FieldContent, FieldContent)]) -> None:
    for content_tuple in contents:
        note: Note = col.get_note(content_tuple[0])
        assert note[DefaultFields.text_field_name] == content_tuple[2]


def __assert_original_notes(col: Collection, contents: list[(NoteId, FieldContent, FieldContent)]) -> None:
    for content_tuple in contents:
        note: Note = col.get_note(content_tuple[0])
        assert note[DefaultFields.text_field_name] == content_tuple[1]


def test_highlight_erase(notes_highlighter: NotesHighlighter, td: Data, col: Collection):
    notes_list: list[(NoteId, FieldContent, FieldContent)] = __create_notes(td, [
        ('beautiful', 'Hello, beautiful world!', 'Hello, <b>beautiful</b> world!'),
        ('beautiful', 'Hello, beautiful world and beautiful day!',
         'Hello, <b>beautiful</b> world and <b>beautiful</b> day!'),
        ('hip', 'Her children is at her hip.', 'Her children is at her <b>hip</b>.'),
        ('beautiful', 'Hello, Beautiful world!', 'Hello, <b>Beautiful</b> world!'),
        ('abstain', 'Abstaining from chocolate', '<b>Abstaining</b> from chocolate'),
        ('overtake', 'A driver was overtaking a slower vehicle.', 'A driver was <b>overtaking</b> a slower vehicle.'),
        ('lie', 'A cat was lying on the floor.', 'A cat was lying on the floor.'),
        ('to overtake', 'Driver was overtaking a slower vehicle.', 'Driver was <b>overtaking</b> a slower vehicle.'),
        ('a driver', 'Driver was overtaking a slower vehicle.', '<b>Driver</b> was overtaking a slower vehicle.'),
        ('an automobile', 'Automobile was overtaking a slower vehicle.',
         '<b>Automobile</b> was overtaking a slower vehicle.'),
        ('take forever', 'Downloading a movie takes forever.', 'Downloading a movie <b>takes forever</b>.'),
        ('lid', '<li>I opened the lid of the jar to get some jam.</li>',
         '<li>I opened the <b>lid</b> of the jar to get some jam.</li>'),
        ('ivy', '<li><div>There is ivy trailing all over the wall.</div></li>',
         '<li><div>There is <b>ivy</b> trailing all over the wall.</div></li>')
    ])
    note_ids: set[NoteId] = {note_tuple[0] for note_tuple in notes_list}
    stop_words: set[str] = {"to", "a", "an"}

    # Highlight 1st time
    notes_highlighter.highlight(note_ids, DefaultFields.word_field_name, DefaultFields.text_field_name, stop_words)
    __assert_highlighted_notes(col, notes_list)

    # Highlight again
    notes_highlighter.highlight(note_ids, DefaultFields.word_field_name, DefaultFields.text_field_name, stop_words)
    __assert_highlighted_notes(col, notes_list)

    # Erase
    notes_highlighter.erase(note_ids, DefaultFields.text_field_name)
    __assert_original_notes(col, notes_list)
