import logging
from logging import Logger
from typing import Optional, Callable

from anki.collection import Collection
from anki.notes import NoteId
from aqt import QWidget
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from .op import Op
from ...highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from ...highlighter.types import Notes
from ...ui.operation.op_statistics_formatter import OpStatisticsFormatter
from ...ui.operation.highlight_op_params import HighlightOpParams

log: Logger = logging.getLogger(__name__)


class HighlightOp(Op):
    def __init__(self, col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                 progress_manager: ProgressManager, note_ids: set[NoteId],
                 op_statistics_formatter: OpStatisticsFormatter, finished_callback: Callable[[], None],
                 parent: Optional[QWidget], highlight_op_params: HighlightOpParams):
        super().__init__(col, notes_highlighter, task_manager, progress_manager, note_ids, op_statistics_formatter,
                         finished_callback, parent, "Highlight", "Highlighting",
                         highlight_op_params.note_type_id)
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__params: HighlightOpParams = highlight_op_params
        log.debug(f"{self.__class__.__name__} was instantiated")

    def _process_slice(self, notes_with_note_type: Notes) -> NotesHighlighterResult:
        return self.__notes_highlighter.highlight(
            notes_with_note_type, self.__params.source_field, self.__params.destination_fields,
            self.__params.stop_words, self.__params.space_delimited_language,
            self.__params.highlight_format)
