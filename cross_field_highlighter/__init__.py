from pathlib import Path

from anki.collection import Collection
from aqt import mw, gui_hooks
from aqt.addons import AddonManager
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from .config.config import Config
from .config.config_loader import ConfigLoader
from .config.settings import Settings
from .config.user_folder_storage import UserFolderStorage
from .highlighter.formatter.formatter_facade import FormatterFacade
from .highlighter.note.field_highlighter import FieldHighlighter
from .highlighter.note.regex_field_highlighter import RegexFieldHighlighter
from .highlighter.note_type_details_factory import NoteTypeDetailsFactory
from .highlighter.notes.notes_highlighter import NotesHighlighter
from .highlighter.text.regex_text_highlighter import RegexTextHighlighter
from .highlighter.text.text_highlighter import TextHighlighter
from .highlighter.token.find_and_replace_token_highlighter import FindAndReplaceTokenHighlighter
from .highlighter.token.start_with_token_highlighter import StartWithTokenHighlighter
from .highlighter.token.token_highlighter import TokenHighlighter
from .highlighter.tokenizer.regex_tokenizer import RegExTokenizer
from .highlighter.tokenizer.stop_words_tokenizer import StopWordsTokenizer
from .highlighter.tokenizer.tokenizer import Tokenizer
from .ui.browser_hooks import BrowserHooks
from .log.logs import Logs
from .ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from .ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from .ui.dialog.adhoc.erase.adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
from .ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from .ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from .ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from .ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model_serde import AdhocHighlightDialogModelSerDe
from .ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from .ui.editor.editor_button_creator import EditorButtonCreator
from .ui.editor.editor_button_hooks import EditorButtonHooks
from .ui.menu.dialog_params_factory import DialogParamsFactory
from .ui.operation.op_statistics_formatter import OpStatisticsFormatter
from .ui.operation.op_factory import OpFactory


def __initialize(col: Collection):
    module_dir: Path = Path(__file__).parent
    module_name: str = module_dir.stem
    addon_manager: AddonManager = mw.addonManager
    log_dir: Path = addon_manager.logs_folder(module_name)
    logs: Logs = Logs(log_dir)
    logs.set_level("DEBUG")
    task_manager: TaskManager = mw.taskman
    progress_manager: ProgressManager = mw.progress
    settings: Settings = Settings(module_dir, module_name, addon_manager.logs_folder(module_name))
    config_loader: ConfigLoader = ConfigLoader(addon_manager, settings)
    config: Config = config_loader.load_config()
    tokenizer: RegExTokenizer = RegExTokenizer()
    formatter_facade: FormatterFacade = FormatterFacade()
    stop_words_tokenizer: StopWordsTokenizer = StopWordsTokenizer()
    start_with_token_highlighter: StartWithTokenHighlighter = StartWithTokenHighlighter(formatter_facade)
    find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter = FindAndReplaceTokenHighlighter(
        formatter_facade)
    text_highlighter: TextHighlighter = RegexTextHighlighter(
        start_with_token_highlighter, find_and_replace_token_highlighter, formatter_facade, tokenizer,
        stop_words_tokenizer)
    regex_field_highlighter: FieldHighlighter = RegexFieldHighlighter(text_highlighter)
    notes_highlighter: NotesHighlighter = NotesHighlighter(regex_field_highlighter, config)
    adhoc_highlight_dialog_model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    note_type_details_factory: NoteTypeDetailsFactory = NoteTypeDetailsFactory(col)
    user_folder_storage: UserFolderStorage = UserFolderStorage(settings)
    adhoc_highlight_dialog_view: AdhocHighlightDialogView = AdhocHighlightDialogView(adhoc_highlight_dialog_model)
    adhoc_highlight_dialog_model_serde: AdhocHighlightDialogModelSerDe = AdhocHighlightDialogModelSerDe()
    adhoc_highlight_dialog_controller: AdhocHighlightDialogController = AdhocHighlightDialogController(
        adhoc_highlight_dialog_model, adhoc_highlight_dialog_view, note_type_details_factory, formatter_facade,
        adhoc_highlight_dialog_model_serde, config, user_folder_storage)
    adhoc_erase_dialog_model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    adhoc_erase_dialog_view: AdhocEraseDialogView = AdhocEraseDialogView(adhoc_erase_dialog_model)
    adhoc_erase_dialog_model_serde: AdhocEraseDialogModelSerDe = AdhocEraseDialogModelSerDe()
    adhoc_erase_dialog_controller: AdhocEraseDialogController = AdhocEraseDialogController(
        adhoc_erase_dialog_model, adhoc_erase_dialog_view, note_type_details_factory, adhoc_erase_dialog_model_serde,
        user_folder_storage)
    op_statistics_formatter: OpStatisticsFormatter = OpStatisticsFormatter(col)
    op_factory: OpFactory = OpFactory(col, notes_highlighter, task_manager, progress_manager, op_statistics_formatter,
                                      config)
    dialog_params_factory: DialogParamsFactory = DialogParamsFactory(col, note_type_details_factory)
    browser_hooks: BrowserHooks = BrowserHooks(op_factory, adhoc_highlight_dialog_controller,
                                               adhoc_erase_dialog_controller, dialog_params_factory, config)
    browser_hooks.setup_hooks()
    editor_button_creator: EditorButtonCreator = EditorButtonCreator(
        adhoc_highlight_dialog_controller, adhoc_erase_dialog_controller, note_type_details_factory,
        regex_field_highlighter, settings)
    editor_button_hooks: EditorButtonHooks = EditorButtonHooks(editor_button_creator)
    editor_button_hooks.setup_hooks()


gui_hooks.collection_did_load.append(__initialize)
