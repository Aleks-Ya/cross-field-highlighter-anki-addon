from pathlib import Path

from anki.collection import Collection
from aqt import mw, gui_hooks
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from cross_field_highlighter.highlighter.formatter.bold_formatter import BoldFormatter
from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.italic_formatter import ItalicFormatter
from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter
from cross_field_highlighter.highlighter.note.start_with_note_highlighter import StartWithNoteHighlighter
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.ui.browser_hooks import BrowserHooks
from cross_field_highlighter.log.logs import Logs
from cross_field_highlighter.ui.highlighter_op_factory import HighlighterOpFactory


def __initialize(col: Collection):
    module_dir: Path = Path(__file__).parent
    module_name: str = module_dir.stem
    log_dir: Path = mw.addonManager.logs_folder(module_name)
    logs: Logs = Logs(log_dir)
    logs.set_level("DEBUG")
    bold_formatter: BoldFormatter = BoldFormatter()
    italic_formatter: ItalicFormatter = ItalicFormatter()
    formatter_facade: FormatterFacade = FormatterFacade(bold_formatter, italic_formatter)
    text_highlighter: TextHighlighter = StartWithTextHighlighter(formatter_facade)
    note_highlighter: NoteHighlighter = StartWithNoteHighlighter(text_highlighter)
    notes_highlighter: NotesHighlighter = NotesHighlighter(note_highlighter)
    task_manager: TaskManager = mw.taskman
    progress_manager: ProgressManager = mw.progress
    highlighter_op_factory: HighlighterOpFactory = HighlighterOpFactory(col, notes_highlighter, task_manager,
                                                                        progress_manager)
    browser_hooks: BrowserHooks = BrowserHooks(highlighter_op_factory)
    browser_hooks.setup_hooks()


gui_hooks.collection_did_load.append(__initialize)
