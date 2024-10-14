import logging
from logging import Logger

log: Logger = logging.getLogger(__name__)


class EraseOpStatistics:
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self):
        self.__notes_selected: int = 0
        self.__notes_highlighted: int = 0
        log.debug(f"{self.__class__.__name__} was instantiated")

    def set_notes_selected(self, notes_selected: int):
        self.__notes_selected = notes_selected

    def increment_notes_erased(self):
        self.__notes_highlighted += 1
