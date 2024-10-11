import tempfile
from pathlib import Path

import aqt
import pytest
from anki.collection import Collection
from aqt import ProfileManager, AnkiQt
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from mock.mock import MagicMock

from cross_field_highlighter.highlighter.formatter.bold_formatter import BoldFormatter
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.italic_formatter import ItalicFormatter
from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
from cross_field_highlighter.highlighter.tokenizer.regex_tokenizer import RegExTokenizer
from tests.data import Data


@pytest.fixture
def profile_name() -> str:
    return "User1"


@pytest.fixture
def base_dir() -> Path:
    return Path(tempfile.mkdtemp(prefix="anki-base-dir"))


@pytest.fixture
def profile_manager(base_dir: Path, profile_name: str) -> ProfileManager:
    anki_base_dir: Path = ProfileManager.get_created_base_folder(str(base_dir))
    pm: ProfileManager = ProfileManager(base=anki_base_dir)
    pm.setupMeta()
    pm.create(profile_name)
    pm.openProfile(profile_name)
    pm.save()
    return pm


@pytest.fixture
def col(profile_manager: ProfileManager) -> Collection:
    collection_file: str = profile_manager.collectionPath()
    col: Collection = Collection(collection_file)
    yield col
    col.close()


@pytest.fixture
def start_with_text_highlighter(formatter_facade: FormatterFacade,
                                regex_tokenizer: RegExTokenizer) -> StartWithTextHighlighter:
    return StartWithTextHighlighter(formatter_facade, regex_tokenizer)


@pytest.fixture
def start_with_note_highlighter(start_with_text_highlighter: StartWithTextHighlighter) -> StartWithNoteHighlighter:
    return StartWithNoteHighlighter(start_with_text_highlighter)


@pytest.fixture
def notes_highlighter(start_with_note_highlighter: StartWithNoteHighlighter) -> NotesHighlighter:
    return NotesHighlighter(start_with_note_highlighter)


@pytest.fixture
def bold_formatter() -> BoldFormatter:
    return BoldFormatter()


@pytest.fixture
def italic_formatter() -> ItalicFormatter:
    return ItalicFormatter()


@pytest.fixture
def formatter_facade(bold_formatter: BoldFormatter, italic_formatter: ItalicFormatter) -> FormatterFacade:
    return FormatterFacade(bold_formatter, italic_formatter)


@pytest.fixture
def regex_tokenizer() -> RegExTokenizer:
    return RegExTokenizer()


@pytest.fixture
def td(col: Collection) -> Data:
    return Data(col)


@pytest.fixture
def mw() -> AnkiQt:
    mw: MagicMock = MagicMock()
    aqt.mw = mw
    return mw


@pytest.fixture
def task_manager(mw: AnkiQt) -> TaskManager:
    task_manager: TaskManager = TaskManager(mw)
    aqt.mw.taskman = TaskManager(mw)
    return task_manager


@pytest.fixture
def progress_manager(mw: AnkiQt) -> ProgressManager:
    return ProgressManager(mw)
