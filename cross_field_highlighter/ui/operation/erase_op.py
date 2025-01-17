import logging
from logging import Logger
from typing import Optional, Callable

from anki.collection import Collection
from anki.notes import NoteId
from aqt import QWidget
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from .erase_op_params import EraseOpParams
from .op import Op
from ...config.config import Config
from ...highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from ...highlighter.types import Notes
from ...ui.operation.op_statistics_formatter import OpStatisticsFormatter

log: Logger = logging.getLogger(__name__)


class EraseOp(Op):
    def __init__(self, col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                 progress_manager: ProgressManager, note_ids: set[NoteId],
                 op_statistics_formatter: OpStatisticsFormatter, show_statistics: bool,
                 finished_callback: Callable[[], None], parent: Optional[QWidget], erase_op_params: EraseOpParams,
                 config: Config):
        super().__init__(col, notes_highlighter, task_manager, progress_manager, note_ids,
                         op_statistics_formatter, show_statistics, finished_callback, parent, "Erase", "Erasing",
                         erase_op_params.note_type_id, config)
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__params: EraseOpParams = erase_op_params
        log.debug(f"{self.__class__.__name__} was instantiated")

    def _process_slice(self, notes_with_note_type: Notes) -> NotesHighlighterResult:
        return self.__notes_highlighter.erase(notes_with_note_type, self.__params.fields)
