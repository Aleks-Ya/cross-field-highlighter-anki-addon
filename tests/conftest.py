import shutil
import tempfile
from pathlib import Path
from typing import Callable, Any

import aqt
import pytest
from anki.collection import Collection
from anki.models import NoteType, NotetypeId
from aqt import ProfileManager, AnkiQt, QApplication
from aqt.addons import AddonManager
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from aqt.theme import ThemeManager
from mock.mock import MagicMock
from pytestqt.qtbot import QtBot

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.config.settings import Settings
from cross_field_highlighter.config.url_manager import UrlManager
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode
from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.tokenizer.stop_words_tokenizer import StopWordsTokenizer
from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
from cross_field_highlighter.highlighter.tokenizer.regex_tokenizer import RegExTokenizer
from cross_field_highlighter.highlighter.types import FieldNames, FieldName, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter
from tests.data import Data, DefaultFields


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
def start_with_text_highlighter(formatter_facade: FormatterFacade, regex_tokenizer: RegExTokenizer,
                                stop_words_tokenizer: StopWordsTokenizer) -> StartWithTextHighlighter:
    return StartWithTextHighlighter(formatter_facade, regex_tokenizer, stop_words_tokenizer)


@pytest.fixture
def start_with_note_highlighter(start_with_text_highlighter: StartWithTextHighlighter) -> StartWithNoteHighlighter:
    return StartWithNoteHighlighter(start_with_text_highlighter)


@pytest.fixture
def notes_highlighter(start_with_note_highlighter: StartWithNoteHighlighter) -> NotesHighlighter:
    return NotesHighlighter(start_with_note_highlighter)


@pytest.fixture
def formatter_facade() -> FormatterFacade:
    return FormatterFacade()


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
def mw(profile_manager: ProfileManager, qapp: QApplication) -> AnkiQt:
    mw_mock: MagicMock = MagicMock()
    mw_mock.pm = profile_manager
    mw_mock.app = qapp
    aqt.mw = mw_mock
    return mw_mock


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
def italic_format(formatter_facade: FormatterFacade) -> HighlightFormat:
    return formatter_facade.get_format_by_code(HighlightFormatCode.ITALIC)


@pytest.fixture
def underline_format(formatter_facade: FormatterFacade) -> HighlightFormat:
    return formatter_facade.get_format_by_code(HighlightFormatCode.UNDERLINE)


@pytest.fixture
def mark_format(formatter_facade: FormatterFacade) -> HighlightFormat:
    return formatter_facade.get_format_by_code(HighlightFormatCode.MARK)


@pytest.fixture
def dialog_params_factory(col: Collection, note_type_details_factory: NoteTypeDetailsFactory) -> DialogParamsFactory:
    return DialogParamsFactory(col, note_type_details_factory)


@pytest.fixture
def basic_note_type(col: Collection) -> NoteType:
    return col.models.by_name('Basic')


@pytest.fixture
def basic_note_type_id(basic_note_type: NoteType) -> NotetypeId:
    return basic_note_type["id"]


@pytest.fixture
def basic_note_type_name(basic_note_type: NoteType) -> NoteTypeName:
    return basic_note_type["name"]


@pytest.fixture
def cloze_note_type(col: Collection) -> NoteType:
    return col.models.by_name('Cloze')


@pytest.fixture
def basic_note_type_details(basic_note_type_id: NotetypeId, basic_note_type_name: NoteTypeName) -> NoteTypeDetails:
    return NoteTypeDetails(
        basic_note_type_id, basic_note_type_name,
        FieldNames([FieldName(DefaultFields.basic_front_field), FieldName(DefaultFields.basic_back_field)]))


@pytest.fixture
def cloze_note_type_details(cloze_note_type: NoteType) -> NoteTypeDetails:
    return NoteTypeDetails(
        cloze_note_type["id"], cloze_note_type["name"],
        FieldNames([FieldName(DefaultFields.cloze_text_field), FieldName(DefaultFields.cloze_extra_field)]))


@pytest.fixture
def theme_manager() -> ThemeManager:
    return ThemeManager()


@pytest.fixture
def config(config_loader: ConfigLoader) -> Config:
    return config_loader.load_config()


@pytest.fixture
def adhoc_highlight_dialog_model() -> AdhocHighlightDialogModel:
    return AdhocHighlightDialogModel()


@pytest.fixture
def adhoc_highlight_dialog_view(adhoc_highlight_dialog_model: AdhocHighlightDialogModel, qtbot: QtBot,
                                theme_manager: ThemeManager, mw: AnkiQt) -> AdhocHighlightDialogView:
    assert mw is not None  # initialize aqt.mw
    view: AdhocHighlightDialogView = AdhocHighlightDialogView(adhoc_highlight_dialog_model)
    theme_manager.apply_style()
    qtbot.addWidget(view)
    return view


@pytest.fixture
def adhoc_highlight_dialog_controller(adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                      note_type_details_factory: NoteTypeDetailsFactory,
                                      formatter_facade: FormatterFacade, config: Config,
                                      config_loader: ConfigLoader) -> AdhocHighlightDialogController:
    return AdhocHighlightDialogController(
        adhoc_highlight_dialog_model, note_type_details_factory, formatter_facade, config, config_loader)


@pytest.fixture
def adhoc_erase_dialog_model() -> AdhocEraseDialogModel:
    return AdhocEraseDialogModel()


@pytest.fixture
def adhoc_erase_dialog_view(adhoc_erase_dialog_model: AdhocEraseDialogModel, theme_manager: ThemeManager,
                            qtbot: QtBot, mw: AnkiQt) -> AdhocEraseDialogView:
    assert mw is not None  # initialize aqt.mw
    view: AdhocEraseDialogView = AdhocEraseDialogView(adhoc_erase_dialog_model)
    theme_manager.apply_style()
    qtbot.addWidget(view)
    return view


@pytest.fixture
def adhoc_erase_dialog_controller(adhoc_erase_dialog_model: AdhocEraseDialogModel,
                                  note_type_details_factory: NoteTypeDetailsFactory, config: Config,
                                  config_loader: ConfigLoader) -> AdhocEraseDialogController:
    return AdhocEraseDialogController(adhoc_erase_dialog_model, note_type_details_factory, config, config_loader)


@pytest.fixture
def note_type_details_factory(col: Collection) -> NoteTypeDetailsFactory:
    return NoteTypeDetailsFactory(col)


@pytest.fixture
def stop_words_tokenizer() -> StopWordsTokenizer:
    return StopWordsTokenizer()


@pytest.fixture
def op_statistics_formatter() -> OpStatisticsFormatter:
    return OpStatisticsFormatter()
