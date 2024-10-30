import logging
from enum import Enum
from logging import Logger

log: Logger = logging.getLogger(__name__)


class OpStatisticsKey(Enum):
    TARGET_NOTE_TYPE_ID = "TARGET_NOTE_TYPE_ID"
    NOTES_SELECTED_ALL = "NOTES_SELECTED_ALL"
    NOTES_SELECTED_TARGET_TYPE = "NOTES_SELECTED_TARGET_TYPE"
    NOTES_PROCESSED = "NOTES_PROCESSED"
    NOTES_MODIFIED = "NOTES_MODIFIED"


class OpStatistics:
    def __init__(self):
        self.__data: dict[OpStatisticsKey, int] = {
            OpStatisticsKey.TARGET_NOTE_TYPE_ID: -1,
            OpStatisticsKey.NOTES_SELECTED_ALL: 0,
            OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE: 0,
            OpStatisticsKey.NOTES_PROCESSED: 0,
            OpStatisticsKey.NOTES_MODIFIED: 0
        }
        log.debug(f"{self.__class__.__name__} was instantiated")

    def set_value(self, key: OpStatisticsKey, value: int):
        self.__data[key] = value

    def increment_value(self, key: OpStatisticsKey, value: int):
        self.__data[key] += value

    def get_value(self, key: OpStatisticsKey) -> int:
        return self.__data[key]

    def as_dict(self) -> dict[OpStatisticsKey, int]:
        return self.__data

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
