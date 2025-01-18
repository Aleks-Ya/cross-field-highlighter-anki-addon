import logging
from logging import Logger
from typing import Optional

from anki.models import NotetypeId, NoteType

from ..number_formatter import NumberFormatter
from ...common.collection_holder import CollectionHolder
from ...ui.operation.op_statistics import OpStatistics, OpStatisticsKey

log: Logger = logging.getLogger(__name__)


class OpStatisticsFormatter:
    def __init__(self, collection_holder: CollectionHolder):
        self.__collection_holder: CollectionHolder = collection_holder
        log.debug(f"{self.__class__.__name__} was instantiated")

    def format(self, op_statistics: OpStatistics):
        note_type_id: NotetypeId = NotetypeId(op_statistics.get_value(OpStatisticsKey.TARGET_NOTE_TYPE_ID))
        log.debug(f"Formatting statistics for Note Type ID: {note_type_id}")
        note_type: Optional[NoteType] = self.__collection_holder.col().models.get(note_type_id)
        note_type_name: str = note_type['name'] if note_type else "N/A"
        return "\n".join([
            f'Notes selected in Browser: {NumberFormatter.with_thousands_separator(op_statistics.get_value(OpStatisticsKey.NOTES_SELECTED_ALL))}',
            f'Notes of type "{note_type_name}": {NumberFormatter.with_thousands_separator(op_statistics.get_value(OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE))}',
            f'Notes processed: {NumberFormatter.with_thousands_separator(op_statistics.get_value(OpStatisticsKey.NOTES_PROCESSED))}',
            f'Notes modified: {NumberFormatter.with_thousands_separator(op_statistics.get_value(OpStatisticsKey.NOTES_MODIFIED))}',
            f'Fields processed: {NumberFormatter.with_thousands_separator(op_statistics.get_value(OpStatisticsKey.FIELDS_PROCESSED))}',
            f'Fields modified: {NumberFormatter.with_thousands_separator(op_statistics.get_value(OpStatisticsKey.FIELDS_MODIFIED))}'
        ])

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
