from pathlib import Path

from anki.collection import Collection
from aqt import mw, gui_hooks
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.config.settings import Settings
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter
from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.highlighter.tokenizer.regex_tokenizer import RegExTokenizer
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokenizer
from cross_field_highlighter.ui.browser_hooks import BrowserHooks
from cross_field_highlighter.log.logs import Logs
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from cross_field_highlighter.ui.operation.op_factory import OpFactory


def __initialize(col: Collection):
    module_dir: Path = Path(__file__).parent
    module_name: str = module_dir.stem
    log_dir: Path = mw.addonManager.logs_folder(module_name)
    logs: Logs = Logs(log_dir)
    logs.set_level("DEBUG")
    tokenizer: RegExTokenizer = RegExTokenizer()
    formatter_facade: FormatterFacade = FormatterFacade(tokenizer)
    text_highlighter: TextHighlighter = StartWithTextHighlighter(formatter_facade, tokenizer)
    note_highlighter: NoteHighlighter = StartWithNoteHighlighter(text_highlighter)
    notes_highlighter: NotesHighlighter = NotesHighlighter(note_highlighter)
    task_manager: TaskManager = mw.taskman
    progress_manager: ProgressManager = mw.progress
    settings: Settings = Settings(module_dir, module_name, mw.addonManager.logs_folder(module_name))
    config_loader: ConfigLoader = ConfigLoader(mw.addonManager, settings)
    config: Config = config_loader.load_config()
    adhoc_highlight_dialog_model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
    adhoc_highlight_dialog_view: AdhocHighlightDialogView = AdhocHighlightDialogView(adhoc_highlight_dialog_model)
    adhoc_highlight_dialog_controller: AdhocHighlightDialogController = AdhocHighlightDialogController(
        adhoc_highlight_dialog_model, adhoc_highlight_dialog_view, formatter_facade, config, config_loader)
    adhoc_erase_dialog_model: AdhocEraseDialogModel = AdhocEraseDialogModel()
    adhoc_erase_dialog_view: AdhocEraseDialogView = AdhocEraseDialogView(adhoc_erase_dialog_model)
    adhoc_erase_dialog_controller: AdhocEraseDialogController = AdhocEraseDialogController(
        adhoc_erase_dialog_model, adhoc_erase_dialog_view, config, config_loader)
    op_factory: OpFactory = OpFactory(col, notes_highlighter, task_manager, progress_manager)
    dialog_params_factory: DialogParamsFactory = DialogParamsFactory(col)
    browser_hooks: BrowserHooks = BrowserHooks(op_factory, adhoc_highlight_dialog_controller,
                                               adhoc_erase_dialog_controller, dialog_params_factory)
    browser_hooks.setup_hooks()


gui_hooks.collection_did_load.append(__initialize)
