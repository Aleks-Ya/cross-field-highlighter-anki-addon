import shutil
import tempfile
from pathlib import Path
from typing import Callable

import aqt
import pytest
from anki.collection import Collection
from anki.models import NoteType, NotetypeId, FieldDict
from aqt import ProfileManager, AnkiQt, QApplication, QWidget, QDesktopServices
from aqt.addons import AddonManager
from aqt.editor import Editor
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from aqt.theme import ThemeManager
from mock.mock import MagicMock
from pytestqt.qtbot import QtBot

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.config.settings import Settings
from cross_field_highlighter.config.url_manager import UrlManager
from cross_field_highlighter.config.user_folder_storage import UserFolderStorage
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode, \
    HighlightFormats
from cross_field_highlighter.highlighter.note.regex_field_highlighter import RegexFieldHighlighter
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.token.find_and_replace_token_highlighter import FindAndReplaceTokenHighlighter
from cross_field_highlighter.highlighter.token.start_with_token_highlighter import StartWithTokenHighlighter
from cross_field_highlighter.highlighter.tokenizer.stop_words_tokenizer import StopWordsTokenizer
from cross_field_highlighter.highlighter.text.regex_text_highlighter import RegexTextHighlighter
from cross_field_highlighter.highlighter.tokenizer.regex_tokenizer import RegExTokenizer
from cross_field_highlighter.highlighter.types import FieldNames, FieldName, NoteTypeName
from cross_field_highlighter.ui.about.about_view import AboutView
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model_serde import \
    AdhocHighlightDialogModelSerDe
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.editor.editor_button_creator import EditorButtonCreator
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from cross_field_highlighter.ui.operation.op_factory import OpFactory
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter
from tests.data import Data, DefaultFields
from tests.ui.dialog.adhoc.erase.adhoc_erase_dialog_view_scaffold import AdhocEraseDialogViewScaffold
from tests.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view_scaffold import AdhocHighlightDialogViewScaffold
from tests.visual_qtbot import VisualQtBot


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
def start_with_token_highlighter(formatter_facade: FormatterFacade) -> StartWithTokenHighlighter:
    return StartWithTokenHighlighter(formatter_facade)


@pytest.fixture
def find_and_replace_token_highlighter(formatter_facade: FormatterFacade) -> FindAndReplaceTokenHighlighter:
    return FindAndReplaceTokenHighlighter(formatter_facade)


@pytest.fixture
def regex_text_highlighter(start_with_token_highlighter: StartWithTokenHighlighter,
                           find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter,
                           formatter_facade: FormatterFacade, regex_tokenizer: RegExTokenizer,
                           stop_words_tokenizer: StopWordsTokenizer) -> RegexTextHighlighter:
    return RegexTextHighlighter(start_with_token_highlighter, find_and_replace_token_highlighter, formatter_facade,
                                regex_tokenizer, stop_words_tokenizer)


@pytest.fixture
def regex_field_highlighter(regex_text_highlighter: RegexTextHighlighter) -> RegexFieldHighlighter:
    return RegexFieldHighlighter(regex_text_highlighter)


@pytest.fixture
def notes_highlighter(regex_field_highlighter: RegexFieldHighlighter, config: Config) -> NotesHighlighter:
    return NotesHighlighter(regex_field_highlighter, config)


@pytest.fixture
def formatter_facade() -> FormatterFacade:
    return FormatterFacade()


@pytest.fixture
def all_highlight_formats(formatter_facade: FormatterFacade) -> HighlightFormats:
    return formatter_facade.get_all_formats()


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
    ignore_patterns: Callable[[any, list[str]], set[str]] = shutil.ignore_patterns("__pycache__")
    shutil.copytree(addon_project_dir, module_dir, ignore=ignore_patterns)
    return module_dir


@pytest.fixture
def td(col: Collection, module_dir: Path, basic_note_type: NoteType, cloze_note_type: NoteType,
       config_loader: ConfigLoader) -> Data:
    return Data(col, module_dir, basic_note_type, cloze_note_type, config_loader)


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
def version() -> str:
    return "0.1.0"


@pytest.fixture
def settings(module_dir: Path, module_name: str, logs_dir: Path, version: str) -> Settings:
    return Settings(module_dir, module_name, logs_dir, version)


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
    note_type: NoteType = col.models.by_name('Basic')
    field: FieldDict = col.models.new_field(DefaultFields.basic_extra)
    col.models.add_field(note_type, field)
    col.models.save(note_type)
    return note_type


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
def cloze_note_type_id(cloze_note_type: NoteType) -> NotetypeId:
    return cloze_note_type["id"]


@pytest.fixture
def basic_note_type_details(basic_note_type_id: NotetypeId, basic_note_type_name: NoteTypeName) -> NoteTypeDetails:
    return NoteTypeDetails(basic_note_type_id, basic_note_type_name,
                           FieldNames([FieldName(DefaultFields.basic_front),
                                       FieldName(DefaultFields.basic_back),
                                       FieldName(DefaultFields.basic_extra)]))


@pytest.fixture
def cloze_note_type_details(cloze_note_type: NoteType) -> NoteTypeDetails:
    return NoteTypeDetails(
        cloze_note_type["id"], cloze_note_type["name"],
        FieldNames([FieldName(DefaultFields.cloze_text), FieldName(DefaultFields.cloze_back_extra)]))


@pytest.fixture
def all_note_type_details(basic_note_type_details: NoteTypeDetails,
                          cloze_note_type_details: NoteTypeDetails) -> list[NoteTypeDetails]:
    return [basic_note_type_details, cloze_note_type_details]


@pytest.fixture
def theme_manager() -> ThemeManager:
    return ThemeManager()


@pytest.fixture
def config(config_loader: ConfigLoader) -> Config:
    return Config(config_loader)


@pytest.fixture
def adhoc_highlight_dialog_model() -> AdhocHighlightDialogModel:
    return AdhocHighlightDialogModel()


@pytest.fixture
def adhoc_highlight_dialog_model_serde() -> AdhocHighlightDialogModelSerDe:
    return AdhocHighlightDialogModelSerDe()


@pytest.fixture
def adhoc_highlight_dialog_view(adhoc_highlight_dialog_model: AdhocHighlightDialogModel, visual_qtbot: VisualQtBot,
                                theme_manager: ThemeManager, mw: AnkiQt) -> AdhocHighlightDialogView:
    assert mw is not None  # initialize aqt.mw
    view: AdhocHighlightDialogView = AdhocHighlightDialogView(adhoc_highlight_dialog_model)
    theme_manager.apply_style()
    visual_qtbot.add_widget(view)
    return view


@pytest.fixture
def adhoc_highlight_dialog_controller(adhoc_highlight_dialog_model: AdhocHighlightDialogModel,
                                      adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                      adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe,
                                      note_type_details_factory: NoteTypeDetailsFactory,
                                      formatter_facade: FormatterFacade, config: Config,
                                      user_folder_storage: UserFolderStorage) -> AdhocHighlightDialogController:
    return AdhocHighlightDialogController(adhoc_highlight_dialog_model, adhoc_highlight_dialog_view,
                                          note_type_details_factory, formatter_facade,
                                          adhoc_highlight_dialog_model_serde, config, user_folder_storage)


@pytest.fixture
def adhoc_highlight_dialog_view_scaffold(adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                         visual_qtbot: VisualQtBot) -> AdhocHighlightDialogViewScaffold:
    return AdhocHighlightDialogViewScaffold(adhoc_highlight_dialog_view, visual_qtbot)


@pytest.fixture
def adhoc_erase_dialog_model() -> AdhocEraseDialogModel:
    return AdhocEraseDialogModel()


@pytest.fixture
def adhoc_erase_dialog_model_serde() -> AdhocEraseDialogModelSerDe:
    return AdhocEraseDialogModelSerDe()


@pytest.fixture
def adhoc_erase_dialog_view(adhoc_erase_dialog_model: AdhocEraseDialogModel, theme_manager: ThemeManager,
                            visual_qtbot: VisualQtBot, mw: AnkiQt) -> AdhocEraseDialogView:
    assert mw is not None  # initialize aqt.mw
    view: AdhocEraseDialogView = AdhocEraseDialogView(adhoc_erase_dialog_model)
    theme_manager.apply_style()
    visual_qtbot.add_widget(view)
    return view


@pytest.fixture
def adhoc_erase_dialog_controller(adhoc_erase_dialog_model: AdhocEraseDialogModel,
                                  adhoc_erase_dialog_view: AdhocEraseDialogView,
                                  adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe,
                                  note_type_details_factory: NoteTypeDetailsFactory,
                                  user_folder_storage: UserFolderStorage) -> AdhocEraseDialogController:
    return AdhocEraseDialogController(adhoc_erase_dialog_model, adhoc_erase_dialog_view, note_type_details_factory,
                                      adhoc_erase_dialog_model_serde, user_folder_storage)


@pytest.fixture
def adhoc_erase_dialog_view_scaffold(adhoc_erase_dialog_view: AdhocEraseDialogView,
                                     visual_qtbot: VisualQtBot) -> AdhocEraseDialogViewScaffold:
    return AdhocEraseDialogViewScaffold(adhoc_erase_dialog_view, visual_qtbot)


@pytest.fixture
def note_type_details_factory(col: Collection) -> NoteTypeDetailsFactory:
    return NoteTypeDetailsFactory(col)


@pytest.fixture
def stop_words_tokenizer() -> StopWordsTokenizer:
    return StopWordsTokenizer()


@pytest.fixture
def op_statistics_formatter(col: Collection) -> OpStatisticsFormatter:
    return OpStatisticsFormatter(col)


@pytest.fixture
def visual_qtbot(qtbot: QtBot) -> VisualQtBot:
    return VisualQtBot(qtbot, 0)


def __editor(mw: AnkiQt, add_mode: bool) -> Editor:
    widget: QWidget = QWidget()
    parent_widget: QWidget = QWidget()
    return Editor(mw, widget, parent_widget, add_mode)


@pytest.fixture
def editor_add_mode(mw: AnkiQt) -> Editor:
    return __editor(mw, True)


@pytest.fixture
def editor_edit_mode(mw: AnkiQt) -> Editor:
    return __editor(mw, False)


@pytest.fixture
def op_factory(col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
               progress_manager: ProgressManager, op_statistics_formatter: OpStatisticsFormatter,
               config: Config) -> OpFactory:
    return OpFactory(col, notes_highlighter, task_manager, progress_manager, op_statistics_formatter, config)


@pytest.fixture
def editor_button_creator(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                          adhoc_erase_dialog_controller: AdhocEraseDialogController,
                          note_type_details_factory: NoteTypeDetailsFactory,
                          regex_field_highlighter: RegexFieldHighlighter, config: Config,
                          settings: Settings) -> EditorButtonCreator:
    return EditorButtonCreator(adhoc_highlight_dialog_controller, adhoc_erase_dialog_controller,
                               note_type_details_factory, regex_field_highlighter, config, settings)


@pytest.fixture
def user_folder_storage(settings: Settings) -> UserFolderStorage:
    return UserFolderStorage(settings)


@pytest.fixture
def desktop_services() -> QDesktopServices:
    return QDesktopServices()


@pytest.fixture
def parent() -> QWidget:
    return QWidget()


@pytest.fixture
def about_view(parent: QWidget, url_manager: UrlManager, desktop_services: QDesktopServices, settings: Settings,
               visual_qtbot: VisualQtBot, mw: AnkiQt) -> AboutView:
    assert mw is not None  # initialize aqt.mw
    return AboutView(parent, url_manager, desktop_services, settings)
