import shutil
import tempfile
from pathlib import Path
from typing import Callable, Any

import aqt
import pytest
from anki.collection import Collection
from anki.models import NoteType
from aqt import ProfileManager, AnkiQt
from aqt.addons import AddonManager
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from mock.mock import MagicMock

from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.config.settings import Settings
from cross_field_highlighter.config.url_manager import UrlManager
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode
from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
from cross_field_highlighter.highlighter.tokenizer.regex_tokenizer import RegExTokenizer
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
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
def formatter_facade(regex_tokenizer: RegExTokenizer) -> FormatterFacade:
    return FormatterFacade(regex_tokenizer)


@pytest.fixture
def regex_tokenizer() -> RegExTokenizer:
    return RegExTokenizer()


@pytest.fixture
def module_name() -> str:
    return "cross_field_highlighter"


@pytest.fixture
def addons_dir(base_dir: Path) -> Path:
    return base_dir / "addons21"


@pytest.fixture
def project_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture
def module_dir(addons_dir: Path, module_name: str, project_dir: Path) -> Path:
    addon_project_dir: Path = project_dir.joinpath("cross_field_highlighter")
    module_dir: Path = addons_dir.joinpath(module_name)
    ignore_patterns: Callable[[Any, list[str]], set[str]] = shutil.ignore_patterns("__pycache__")
    shutil.copytree(addon_project_dir, module_dir, ignore=ignore_patterns)
    return module_dir


@pytest.fixture
def td(col: Collection, module_dir: Path, basic_note_type: NoteType, cloze_note_type: NoteType) -> Data:
    return Data(col, module_dir, basic_note_type, cloze_note_type)


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


@pytest.fixture
def config_loader(addon_manager: AddonManager, settings: Settings) -> ConfigLoader:
    return ConfigLoader(addon_manager, settings)


@pytest.fixture
def settings(module_dir: Path, module_name: str, logs_dir: Path) -> Settings:
    return Settings(module_dir, module_name, logs_dir)


@pytest.fixture
def addon_manager(addons_dir: Path) -> AddonManager:
    mw: MagicMock = MagicMock()
    mw.pm.addonFolder.return_value = addons_dir
    return AddonManager(mw)


@pytest.fixture
def logs_dir(base_dir: Path, module_name: str) -> Path:
    return base_dir / "logs" / "addons" / module_name


@pytest.fixture
def url_manager() -> UrlManager:
    return UrlManager()


@pytest.fixture
def bold_format(formatter_facade: FormatterFacade) -> HighlightFormat:
    return formatter_facade.get_format_by_code(HighlightFormatCode.BOLD)


@pytest.fixture
def dialog_params_factory(col: Collection) -> DialogParamsFactory:
    return DialogParamsFactory(col)


@pytest.fixture
def basic_note_type(col: Collection) -> NoteType:
    return col.models.by_name('Basic')


@pytest.fixture
def cloze_note_type(col: Collection) -> NoteType:
    return col.models.by_name('Cloze')
