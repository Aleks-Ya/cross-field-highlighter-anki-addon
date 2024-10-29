import logging
from logging import Logger

log: Logger = logging.getLogger(__name__)


class EraseOpStatistics:
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self):
        self.__notes_selected: int = 0
        self.__notes_processed: int = 0
        self.__notes_modified: int = 0
        log.debug(f"{self.__class__.__name__} was instantiated")

    def set_notes_selected(self, notes_selected: int):
        self.__notes_selected = notes_selected

    def increment_notes_processed(self, note_count: int):
        self.__notes_processed += note_count

    def increment_notes_modified(self, note_count: int):
        self.__notes_modified += note_count

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
