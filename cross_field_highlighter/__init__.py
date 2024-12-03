from pathlib import Path

from anki.collection import Collection
from aqt import mw, gui_hooks
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from .config.config import Config
from .config.config_loader import ConfigLoader
from .config.settings import Settings
from .highlighter.formatter.formatter_facade import FormatterFacade
from .highlighter.note.note_field_highlighter import NoteFieldHighlighter
from .highlighter.note.start_with_note_field_highlighter import StartWithNoteFieldHighlighter
from .highlighter.note_type_details_factory import NoteTypeDetailsFactory
from .highlighter.notes.notes_highlighter import NotesHighlighter
from .highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
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
from .ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from .ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from .ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from .ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from .ui.menu.dialog_params_factory import DialogParamsFactory
from .ui.operation.op_statistics_formatter import OpStatisticsFormatter
from .ui.operation.op_factory import OpFactory


def __initialize(col: Collection):
    module_dir: Path = Path(__file__).parent
    module_name: str = module_dir.stem
    log_dir: Path = mw.addonManager.logs_folder(module_name)
    logs: Logs = Logs(log_dir)
    logs.set_level("DEBUG")
    tokenizer: RegExTokenizer = RegExTokenizer()
    formatter_facade: FormatterFacade = FormatterFacade()
    stop_words_tokenizer: StopWordsTokenizer = StopWordsTokenizer()
    start_with_token_highlighter: StartWithTokenHighlighter = StartWithTokenHighlighter(formatter_facade)
    find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter = FindAndReplaceTokenHighlighter(
        formatter_facade)
    text_highlighter: TextHighlighter = StartWithTextHighlighter(
        start_with_token_highlighter, find_and_replace_token_highlighter, formatter_facade, tokenizer,
        stop_words_tokenizer)
    note_field_highlighter: NoteFieldHighlighter = StartWithNoteFieldHighlighter(text_highlighter)
    notes_highlighter: NotesHighlighter = NotesHighlighter(note_field_highlighter)
    task_manager: TaskManager = mw.taskman
    progress_manager: ProgressManager = mw.progress
    settings: Settings = Settings(module_dir, module_name, mw.addonManager.logs_folder(module_name))
    config_loader: ConfigLoader = ConfigLoader(mw.addonManager, settings)
    config: Config = config_loader.load_config()
    adhoc_highlight_dialog_model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    note_type_details_factory: NoteTypeDetailsFactory = NoteTypeDetailsFactory(col)
    adhoc_highlight_dialog_view: AdhocHighlightDialogView = AdhocHighlightDialogView(adhoc_highlight_dialog_model)
    adhoc_highlight_dialog_controller: AdhocHighlightDialogController = AdhocHighlightDialogController(
        adhoc_highlight_dialog_model, adhoc_highlight_dialog_view, note_type_details_factory, formatter_facade, config,
        config_loader)
    adhoc_erase_dialog_model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    adhoc_erase_dialog_view: AdhocEraseDialogView = AdhocEraseDialogView(adhoc_erase_dialog_model)
    adhoc_erase_dialog_controller: AdhocEraseDialogController = AdhocEraseDialogController(
        adhoc_erase_dialog_model, adhoc_erase_dialog_view, note_type_details_factory, config, config_loader)
    op_statistics_formatter: OpStatisticsFormatter = OpStatisticsFormatter(col)
    op_factory: OpFactory = OpFactory(col, notes_highlighter, task_manager, progress_manager, op_statistics_formatter)
    dialog_params_factory: DialogParamsFactory = DialogParamsFactory(col, note_type_details_factory)
    browser_hooks: BrowserHooks = BrowserHooks(op_factory, adhoc_highlight_dialog_controller,
                                               adhoc_erase_dialog_controller, dialog_params_factory)
    browser_hooks.setup_hooks()


gui_hooks.collection_did_load.append(__initialize)
