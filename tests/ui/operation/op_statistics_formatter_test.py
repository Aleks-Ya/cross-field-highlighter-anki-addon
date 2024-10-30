import textwrap

from anki.models import NotetypeId

from cross_field_highlighter.ui.operation.op_statistics import OpStatistics, OpStatisticsKey
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter


def test_format(op_statistics_formatter: OpStatisticsFormatter, basic_note_type_id: NotetypeId):
    statistics: OpStatistics = OpStatistics()
    statistics.set_value(OpStatisticsKey.TARGET_NOTE_TYPE_ID, basic_note_type_id)
    statistics.set_value(OpStatisticsKey.NOTES_SELECTED_ALL, 10)
    statistics.set_value(OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE, 8)
    statistics.increment_value(OpStatisticsKey.NOTES_PROCESSED, 7)
    statistics.increment_value(OpStatisticsKey.NOTES_MODIFIED, 3)
    formatted: str = op_statistics_formatter.format(statistics)
    assert formatted == textwrap.dedent('''\
                                        Notes selected in Browser: 10
                                        Notes of type "Basic": 8
                                        Notes processed: 7
                                        Notes modified: 3''')
