import logging
from logging import Logger
from typing import Optional

from anki.collection import Collection
from anki.notes import NoteId, Note
from aqt import QWidget
from aqt.operations import QueryOp
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from aqt.utils import show_critical, show_info

from ..highlighter.formatter.highlight_format import HighlightFormat
from ..highlighter.notes.notes_highlighter import NotesHighlighter
from ..highlighter.types import FieldName, Word

log: Logger = logging.getLogger(__name__)


class HighlighterOp(QueryOp):
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self, col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                 progress_manager: ProgressManager, parent: QWidget, note_ids: set[NoteId], source_field: FieldName,
                 destination_field: FieldName, stop_words: set[Word], highlight_format: HighlightFormat):
        super().__init__(parent=parent, op=self.__background_op, success=self.__on_success)
        self.with_progress("Note Size cache initializing")
        self.failure(self.__on_failure)
        self.__col: Collection = col
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        self.__parent: QWidget = parent
        self.__note_ids: set[NoteId] = note_ids
        self.__source_field: FieldName = source_field
        self.__destination_field: FieldName = destination_field
        self.__stop_words: set[Word] = stop_words
        self.__highlight_format: HighlightFormat = highlight_format
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __background_op(self, _: Collection) -> int:
        return self.__highlight_in_background(self.__note_ids, self.__source_field, self.__destination_field,
                                              self.__stop_words, self.__highlight_format)

    def __highlight_in_background(self, note_ids: set[NoteId], source_field: FieldName, destination_field: FieldName,
                                  stop_words: set[Word], highlight_format: HighlightFormat) -> int:
        c: int = 30
        note_ids_list: list[NoteId] = list(note_ids)
        note_ids_slices: list[list[NoteId]] = [note_ids_list[i:i + c] for i in range(0, len(note_ids_list), c)]
        highlighted_counter: int = 0
        for note_ids_slice in note_ids_slices:
            notes: list[Note] = [self.__col.get_note(note_id) for note_id in note_ids_slice]
            log.debug(f"Original notes: {notes}")
            highlighted_notes: list[Note] = self.__notes_highlighter.highlight(notes, source_field, destination_field,
                                                                               stop_words, highlight_format)
            self.__col.update_notes(highlighted_notes)
            log.debug(f"Highlighted notes: {highlighted_notes}")
            highlighted_counter += len(highlighted_notes)
            self.__update_progress("Highlighting", highlighted_counter, len(note_ids))
            if self.__progress_manager.want_cancel():
                return highlighted_counter
        return len(note_ids_list)

    def __update_progress(self, label: str, value: int, max_value: int) -> None:
        self.__task_manager.run_on_main(lambda: self.__update_progress_in_main(label, value, max_value))

    def __update_progress_in_main(self, label: str, value: Optional[int], max_value: Optional[int]) -> None:
        self.__progress_manager.set_title(self.__progress_dialog_title)
        self.__progress_manager.update(label=label, value=value, max=max_value)

    def __on_success(self, count: int) -> None:
        log.info(f"Highlighting finished: {count}")
        show_info(title=self.__progress_dialog_title, text=f"Notes were highlighted)", parent=self.__parent)

    def __on_failure(self, e: Exception) -> None:
        log.error("Error during highlighting", exc_info=e)
        show_critical(title=self.__progress_dialog_title, text="Error during highlighting (see logs)",
                      parent=self.__parent)
