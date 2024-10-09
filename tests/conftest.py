import tempfile
from pathlib import Path

import pytest
from anki.collection import Collection
from aqt import ProfileManager

from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
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
def start_with_text_highlighter() -> StartWithTextHighlighter:
    return StartWithTextHighlighter()


@pytest.fixture
def start_with_note_highlighter(col: Collection,
                                start_with_text_highlighter: StartWithTextHighlighter) -> StartWithNoteHighlighter:
    return StartWithNoteHighlighter(col, start_with_text_highlighter)


@pytest.fixture
def td(col: Collection) -> Data:
    return Data(col)
