import time

from anki.collection import Collection
from anki.notes import Note, NoteId
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from mock.mock import MagicMock

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.types import FieldContent, Word
from cross_field_highlighter.ui.highlighter_op import HighlighterOp
from tests.data import Data, DefaultFields


def __create_notes(td: Data, contents: list[(str, str, str)]) -> list[(Note, FieldContent, FieldContent)]:
    res: list[(NoteId, FieldContent, FieldContent)] = []
    for content_tuple in contents:
        word_content: FieldContent = FieldContent(content_tuple[0])
        original_content: FieldContent = FieldContent(content_tuple[1])
        highlighted_content: FieldContent = FieldContent(content_tuple[2])
        note: Note = td.create_note_with_fields(FieldContent(word_content), FieldContent(original_content))
        res.append((note, original_content, highlighted_content))
    return res


def __assert_highlighted_notes(col: Collection, contents: list[(Note, FieldContent, FieldContent)]) -> None:
    for content_tuple in contents:
        exp_note: Note = content_tuple[0]
        act_note: Note = col.get_note(exp_note.id)
        highlighted_content: FieldContent = content_tuple[2]
        assert act_note[DefaultFields.text_field_name] == highlighted_content


def __assert_original_notes(col: Collection, contents: list[(Note, FieldContent, FieldContent)]) -> None:
    for content_tuple in contents:
        exp_note: Note = content_tuple[0]
        act_note: Note = col.get_note(exp_note.id)
        original_content: FieldContent = content_tuple[1]
        assert act_note[DefaultFields.text_field_name] == original_content


def test_highlight_erase(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                         progress_manager: ProgressManager, td: Data):
    notes_list: list[(Note, FieldContent, FieldContent)] = __create_notes(td, [
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
    notes: list[Note] = [note_tuple[0] for note_tuple in notes_list]
    note_ids: set[NoteId] = {note.id for note in notes}
    stop_words: set[Word] = {Word("to"), Word("a"), Word("an")}
    highlight_format: HighlightFormat = HighlightFormat.BOLD
    highlighter_op: HighlighterOp = HighlighterOp(col, notes_highlighter, task_manager, progress_manager,
                                                  MagicMock(), note_ids, DefaultFields.word_field_name,
                                                  DefaultFields.text_field_name, stop_words, highlight_format)

    highlighter_op.run_in_background()
    time.sleep(1)
    __assert_highlighted_notes(col, notes_list)
