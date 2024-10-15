import logging
from logging import Logger
from typing import Callable

from anki.collection import Collection
from anki.notes import NoteId
from aqt import QWidget
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from .erase_op import EraseOp
from .highlight_op import HighlightOp
from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter
from cross_field_highlighter.highlighter.types import FieldNames
from .highlight_op_params import HighlightOpParams

log: Logger = logging.getLogger(__name__)


class OpFactory:

    def __init__(self, col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                 progress_manager: ProgressManager):
        self.__col: Collection = col
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_highlight_op(self, note_ids: set[NoteId], highlight_op_params: HighlightOpParams,
                            callback: Callable[[], None]) -> HighlightOp:
        log.debug(f"Creating HighlightOp: note_ids={len(note_ids)}, params={highlight_op_params}")
        return HighlightOp(self.__col, self.__notes_highlighter, self.__task_manager, self.__progress_manager,
                           note_ids, highlight_op_params, callback)

    def create_erase_op(self, parent: QWidget, note_ids: set[NoteId], fields: FieldNames,
                        callback: Callable[[], None]) -> EraseOp:
        log.debug(f"Creating EraseOp: note_ids={len(note_ids)}, fields={fields}")
        return EraseOp(self.__col, self.__notes_highlighter, self.__task_manager, self.__progress_manager,
                       parent, note_ids, fields, callback)
