import logging
from logging import Logger

log: Logger = logging.getLogger(__name__)


class EraseOpStatistics:
    __notes_selected_key: str = 'notes_selected'
    __notes_processed_key: str = 'notes_processed'
    __notes_modified_key: str = 'notes_modified'

    def __init__(self):
        self.__data: dict[str, int] = {
            self.__notes_selected_key: 0,
            self.__notes_processed_key: 0,
            self.__notes_modified_key: 0
        }
        log.debug(f"{self.__class__.__name__} was instantiated")

    def set_notes_selected(self, notes_selected: int):
        self.__data[self.__notes_selected_key] = notes_selected

    def increment_notes_processed(self, note_count: int):
        self.__data[self.__notes_processed_key] += note_count

    def increment_notes_modified(self, note_count: int):
        self.__data[self.__notes_modified_key] += note_count

    def get_notes_selected(self) -> int:
        return self.__data[self.__notes_selected_key]

    def get_notes_processed(self) -> int:
        return self.__data[self.__notes_processed_key]

    def get_notes_modified(self) -> int:
        return self.__data[self.__notes_modified_key]

    def as_dict(self) -> dict[str, int]:
        return self.__data

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
