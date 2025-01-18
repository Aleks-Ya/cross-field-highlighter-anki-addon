import logging
from logging import Logger
from typing import Optional, Callable

from anki.notes import NoteId
from aqt import QWidget
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from .op import Op
from ...common.collection_holder import CollectionHolder
from ...config.config import Config
from ...highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from ...highlighter.types import Notes
from ...ui.operation.highlight_op_params import HighlightOpParams
from ...ui.operation.op_statistics_formatter import OpStatisticsFormatter

log: Logger = logging.getLogger(__name__)


class HighlightOp(Op):
    def __init__(self, collection_holder: CollectionHolder, notes_highlighter: NotesHighlighter,
                 task_manager: TaskManager, progress_manager: ProgressManager, note_ids: set[NoteId],
                 op_statistics_formatter: OpStatisticsFormatter, show_statistics: bool,
                 finished_callback: Callable[[], None], parent: Optional[QWidget],
                 highlight_op_params: HighlightOpParams, config: Config):
        super().__init__(collection_holder, notes_highlighter, task_manager, progress_manager, note_ids,
                         op_statistics_formatter, show_statistics, finished_callback, parent, "Highlight",
                         "Highlighting", highlight_op_params.note_type_id, config)
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__params: HighlightOpParams = highlight_op_params
        log.debug(f"{self.__class__.__name__} was instantiated")

    def _process_slice(self, notes_with_note_type: Notes) -> NotesHighlighterResult:
        return self.__notes_highlighter.highlight(
            notes_with_note_type, self.__params.source_field, self.__params.destination_fields,
            self.__params.stop_words, self.__params.space_delimited_language,
            self.__params.highlight_format)
