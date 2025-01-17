import logging
from abc import abstractmethod
from logging import Logger
from typing import Optional, Callable, Sequence

from anki.collection import Collection
from anki.models import NotetypeId
from anki.notes import NoteId
from aqt import QWidget
from aqt.operations import QueryOp
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from aqt.utils import show_critical, show_info

from ...config.config import Config
from ...highlighter.notes.notes_highlighter import NotesHighlighter, NotesHighlighterResult
from ...highlighter.types import Notes
from ...ui.operation.op_statistics import OpStatistics, OpStatisticsKey
from ...ui.operation.op_statistics_formatter import OpStatisticsFormatter

log: Logger = logging.getLogger(__name__)


class Op(QueryOp):
    def __init__(self, col: Collection, notes_highlighter: NotesHighlighter, task_manager: TaskManager,
                 progress_manager: ProgressManager, note_ids: set[NoteId],
                 op_statistics_formatter: OpStatisticsFormatter, show_statistics: bool,
                 finished_callback: Callable[[], None], parent: Optional[QWidget], progress_dialog_title: str,
                 operation_title: str, note_type_id: NotetypeId, config: Config):
        super().__init__(parent=parent, op=self.__background_op, success=self.__on_success)
        self.with_progress("Initializing")
        self.failure(self.__on_failure)
        self.__col: Collection = col
        self.__notes_highlighter: NotesHighlighter = notes_highlighter
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        self.__parent: QWidget = parent
        self.__note_ids: set[NoteId] = note_ids
        self.__op_statistics_formatter: OpStatisticsFormatter = op_statistics_formatter
        self.__show_statistics: bool = show_statistics
        self.__finished_callback: Callable[[], None] = finished_callback
        self.__statistics: OpStatistics = OpStatistics()
        self.__note_type_id: NotetypeId = note_type_id
        self.__progress_dialog_title: str = progress_dialog_title
        self.__operation_title: str = operation_title
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_statistics(self) -> OpStatistics:
        return self.__statistics

    def __background_op(self, _: Collection) -> int:
        log.debug("Stringing background operation")
        self.__statistics.set_value(OpStatisticsKey.TARGET_NOTE_TYPE_ID, self.__note_type_id)
        slice_size: int = 30
        note_ids_list: list[NoteId] = list(self.__note_ids)
        self.__statistics.set_value(OpStatisticsKey.NOTES_SELECTED_ALL, len(note_ids_list))
        note_ids_slices: list[list[NoteId]] = [note_ids_list[i:i + slice_size] for i in
                                               range(0, len(note_ids_list), slice_size)]
        updated_notes_counter: int = 0
        total_note_number: int = len(self.__note_ids)
        self.__remove_tag(note_ids_list)
        for note_ids_slice in note_ids_slices:
            notes: Notes = Notes([self.__col.get_note(note_id) for note_id in note_ids_slice])
            notes_with_note_type: Notes = Notes(
                [note for note in notes if note.mid == self.__note_type_id])
            self.__statistics.increment_value(OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE, len(notes_with_note_type))
            result: NotesHighlighterResult = self._process_slice(notes_with_note_type)
            self.__statistics.increment_value(OpStatisticsKey.NOTES_PROCESSED, result.total_notes)
            self.__statistics.increment_value(OpStatisticsKey.NOTES_MODIFIED, result.modified_notes)
            self.__statistics.increment_value(OpStatisticsKey.FIELDS_PROCESSED, result.total_fields)
            self.__statistics.increment_value(OpStatisticsKey.FIELDS_MODIFIED, result.modified_fields)
            self.__col.update_notes(result.notes)
            updated_notes_counter += len(result.notes)
            log.debug(f"Updated notes: {updated_notes_counter} of {total_note_number}")
            self.__update_progress(updated_notes_counter, total_note_number)
            if self.__progress_manager.want_cancel():
                log.info(f"Progress dialog was cancelled: updated_notes_counter={updated_notes_counter}")
                return updated_notes_counter
        log.debug("Finished background operation")
        return updated_notes_counter

    def __remove_tag(self, note_ids_list: list[NoteId]):
        latest_modified_notes_tag: str = self.__config.get_latest_modified_notes_tag()
        if self.__config.get_latest_modified_notes_enabled():
            log.debug(f"Removing tag from {len(note_ids_list)} notes")
            note_ids: Sequence[NoteId] = self.__col.find_notes(f"tag:{latest_modified_notes_tag}")
            self.__col.tags.bulk_remove(note_ids, latest_modified_notes_tag)
            log.debug(f"Removing tag from {len(note_ids_list)} notes finished")
        else:
            log.debug("Deleting latest modified notes tag because it is disabled")
            self.__col.tags.remove(latest_modified_notes_tag)
            log.debug("Deleting latest modified notes tag finished")

    @abstractmethod
    def _process_slice(self, notes_with_note_type: Notes) -> NotesHighlighterResult:
        ...

    def __update_progress(self, value: int, max_value: int) -> None:
        self.__task_manager.run_on_main(lambda: self.__update_progress_in_main(value, max_value))

    def __update_progress_in_main(self, value: Optional[int], max_value: Optional[int]) -> None:
        self.__progress_manager.set_title(self.__progress_dialog_title)
        label: str = f"{self.__operation_title}: {value} of {max_value} notes"
        self.__progress_manager.update(label=label, value=value, max=max_value)

    def __on_success(self, count: int) -> None:
        log.info(f"Operation finished: {count}")
        if self.__show_statistics:
            show_info(title=self.__progress_dialog_title,
                      text=self.__op_statistics_formatter.format(self.get_statistics()), parent=self.__parent)
        else:
            log.debug("Statistics are not shown")
        self.__finished_callback()

    def __on_failure(self, e: Exception) -> None:
        log.error("Error during operation", exc_info=e)
        show_critical(title=self.__progress_dialog_title,
                      text=f"Error during {self.__operation_title.lower()} (see logs)", parent=self.__parent)
        self.__finished_callback()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
