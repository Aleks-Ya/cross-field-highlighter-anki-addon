import logging
from logging import Logger
from typing import Callable, Optional

from anki.collection import Collection
from anki.notes import NoteId
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from aqt import QWidget

from .erase_op import EraseOp
from .erase_op_params import EraseOpParams
from .highlight_op import HighlightOp
from .highlight_op_params import HighlightOpParams
from .op_statistics_formatter import OpStatisticsFormatter
from ...config.config import Config
from ...highlighter.notes.notes_highlighter import NotesHighlighter

log: Logger = logging.getLogger(__name__)


class OpFactory:

    def __init__(self, col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                 progress_manager: ProgressManager, op_statistics_formatter: OpStatisticsFormatter,
                 config: Config):
        self.__col: Collection = col
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        self.__op_statistics_formatter: OpStatisticsFormatter = op_statistics_formatter
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_highlight_op(self, note_ids: set[NoteId], callback: Callable[[], None],
                            parent: Optional[QWidget], highlight_op_params: HighlightOpParams) -> HighlightOp:
        log.debug("Creating HighlightOp")
        return HighlightOp(self.__col, self.__notes_highlighter, self.__task_manager, self.__progress_manager,
                           note_ids, self.__op_statistics_formatter, callback, parent, highlight_op_params,
                           self.__config)

    def create_erase_op(self, note_ids: set[NoteId], callback: Callable[[], None], parent: Optional[QWidget],
                        erase_op_params: EraseOpParams) -> EraseOp:
        log.debug(f"Creating EraseOp: note_ids={len(note_ids)}")
        return EraseOp(self.__col, self.__notes_highlighter, self.__task_manager, self.__progress_manager,
                       note_ids, self.__op_statistics_formatter, callback, parent, erase_op_params, self.__config)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
