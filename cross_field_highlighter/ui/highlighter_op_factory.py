import logging
from logging import Logger

from anki.collection import Collection
from anki.notes import NoteId
from aqt import QWidget
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager

from .highlighter_op import HighlighterOp
from ..highlighter.notes.notes_highlighter import NotesHighlighter
from ..highlighter.types import FieldName

log: Logger = logging.getLogger(__name__)


class HighlighterOpFactory:

    def __init__(self, col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                 progress_manager: ProgressManager):
        self.__col: Collection = col
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_op(self, parent: QWidget, note_ids: set[NoteId], source_field: FieldName,
                  destination_field: FieldName, stop_words: set[str]) -> HighlighterOp:
        return HighlighterOp(self.__col, self.__notes_highlighter, self.__task_manager, self.__progress_manager,
                             parent, note_ids, source_field, destination_field, stop_words)
