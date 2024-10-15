import logging
from logging import Logger
from typing import Optional, Callable

from anki.collection import Collection
from anki.models import NotetypeId
from anki.notes import NoteId
from aqt import QWidget
from aqt.operations import QueryOp
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from aqt.utils import show_critical, show_info

from cross_field_highlighter.highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from cross_field_highlighter.highlighter.types import FieldNames, Notes
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from cross_field_highlighter.ui.operation.erase_op_statistics import EraseOpStatistics

log: Logger = logging.getLogger(__name__)


class EraseOp(QueryOp):
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self, col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                 progress_manager: ProgressManager, note_ids: set[NoteId],
                 params: EraseOpParams, callback: Callable[[], None]):
        super().__init__(parent=params.parent, op=self.__background_op, success=self.__on_success)
        self.with_progress("Note Size cache initializing")
        self.failure(self.__on_failure)
        self.__col: Collection = col
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        self.__parent: QWidget = params.parent
        self.__note_type_id: NotetypeId = params.note_type_id
        self.__note_ids: set[NoteId] = note_ids
        self.__destination_fields: FieldNames = params.fields
        self.__callback: Callable[[], None] = callback
        self.__statistics: EraseOpStatistics = EraseOpStatistics()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_statistics(self) -> EraseOpStatistics:
        return self.__statistics

    def __background_op(self, _: Collection) -> int:
        c: int = 30
        note_ids_list: list[NoteId] = list(self.__note_ids)
        self.__statistics.set_notes_selected(len(note_ids_list))
        note_ids_slices: list[list[NoteId]] = [note_ids_list[i:i + c] for i in range(0, len(note_ids_list), c)]
        highlighted_counter: int = 0
        for note_ids_slice in note_ids_slices:
            notes: Notes = Notes([self.__col.get_note(note_id) for note_id in note_ids_slice])
            log.debug(f"All notes: {len(notes)}")
            notes_with_note_type: Notes = Notes([note for note in notes if note.mid == self.__note_type_id])
            log.debug(f"Notes with note type {self.__note_type_id}: {len(notes_with_note_type)}")
            highlighted_notes: Notes = Notes([])
            for field in self.__destination_fields:
                result: NotesHighlighterResult = self.__notes_highlighter.erase(notes_with_note_type, field)
                processed_notes: Notes = result.notes
                highlighted_notes += processed_notes
                self.__statistics.increment_notes_processed(len(processed_notes))
                self.__statistics.increment_notes_modified(result.modified_notes)
            self.__col.update_notes(highlighted_notes)
            log.debug(f"Highlighted notes: {highlighted_notes}")
            highlighted_counter += len(highlighted_notes)
            self.__update_progress("Highlighting", highlighted_counter, len(self.__note_ids))
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
        show_info(title=self.__progress_dialog_title, text=f"{count} notes were erased", parent=self.__parent)
        self.__callback()

    def __on_failure(self, e: Exception) -> None:
        log.error("Error during highlighting", exc_info=e)
        show_critical(title=self.__progress_dialog_title, text="Error during highlighting (see logs)",
                      parent=self.__parent)
        self.__callback()
