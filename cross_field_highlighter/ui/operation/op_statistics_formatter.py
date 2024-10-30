import logging
from logging import Logger

from cross_field_highlighter.ui.operation.op_statistics import OpStatistics

log: Logger = logging.getLogger(__name__)


class OpStatisticsFormatter:
    __notes_selected_key: str = 'notes_selected'
    __notes_processed_key: str = 'notes_processed'
    __notes_modified_key: str = 'notes_modified'

    def __init__(self):
        log.debug(f"{self.__class__.__name__} was instantiated")

    def format(self, op_statistics: OpStatistics):
        row1: str = f"Notes selected in Browser: {op_statistics.get_notes_selected()}"
        row2: str = f"Notes processed: {op_statistics.get_notes_processed()}"
        row3: str = f"Notes modified: {op_statistics.get_notes_modified()}"
        return "\n".join([row1, row2, row3])

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
