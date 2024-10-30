import logging
from logging import Logger

from anki.collection import Collection

from cross_field_highlighter.ui.operation.op_statistics import OpStatistics, OpStatisticsKey

log: Logger = logging.getLogger(__name__)


class OpStatisticsFormatter:
    def __init__(self, col: Collection):
        self.__col: Collection = col
        log.debug(f"{self.__class__.__name__} was instantiated")

    def format(self, op_statistics: OpStatistics):
        note_type_name: str = self.__col.models.get(op_statistics.get_value(OpStatisticsKey.TARGET_NOTE_TYPE_ID))[
            'name']
        return "\n".join(
            [f'Notes selected in Browser: {op_statistics.get_value(OpStatisticsKey.NOTES_SELECTED_ALL)}',
             f'Notes of type "{note_type_name}": {op_statistics.get_value(OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE)}',
             f'Notes processed: {op_statistics.get_value(OpStatisticsKey.NOTES_PROCESSED)}',
             f'Notes modified: {op_statistics.get_value(OpStatisticsKey.NOTES_MODIFIED)}'])

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
