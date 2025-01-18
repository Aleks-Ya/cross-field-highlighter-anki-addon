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
    statistics.increment_value(OpStatisticsKey.FIELDS_PROCESSED, 14)
    statistics.increment_value(OpStatisticsKey.FIELDS_MODIFIED, 6)
    formatted: str = op_statistics_formatter.format(statistics)
    assert formatted == textwrap.dedent('''\
                                        Notes selected in Browser: 10
                                        Notes of type "Basic": 8
                                        Notes processed: 7
                                        Notes modified: 3
                                        Fields processed: 14
                                        Fields modified: 6''')


def test_thousand_delimiter(op_statistics_formatter: OpStatisticsFormatter, basic_note_type_id: NotetypeId):
    statistics: OpStatistics = OpStatistics()
    statistics.set_value(OpStatisticsKey.TARGET_NOTE_TYPE_ID, basic_note_type_id)
    statistics.set_value(OpStatisticsKey.NOTES_SELECTED_ALL, 10000)
    statistics.set_value(OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE, 8000)
    statistics.increment_value(OpStatisticsKey.NOTES_PROCESSED, 7000)
    statistics.increment_value(OpStatisticsKey.NOTES_MODIFIED, 3000)
    statistics.increment_value(OpStatisticsKey.FIELDS_PROCESSED, 14000)
    statistics.increment_value(OpStatisticsKey.FIELDS_MODIFIED, 6000)
    formatted: str = op_statistics_formatter.format(statistics)
    assert formatted == textwrap.dedent('''\
                                        Notes selected in Browser: 10 000
                                        Notes of type "Basic": 8 000
                                        Notes processed: 7 000
                                        Notes modified: 3 000
                                        Fields processed: 14 000
                                        Fields modified: 6 000''')


def test_format_note_type_absents(op_statistics_formatter: OpStatisticsFormatter):
    statistics: OpStatistics = OpStatistics()
    statistics.set_value(OpStatisticsKey.TARGET_NOTE_TYPE_ID, -1)
    statistics.set_value(OpStatisticsKey.NOTES_SELECTED_ALL, 10)
    statistics.set_value(OpStatisticsKey.NOTES_SELECTED_TARGET_TYPE, 8)
    statistics.increment_value(OpStatisticsKey.NOTES_PROCESSED, 7)
    statistics.increment_value(OpStatisticsKey.NOTES_MODIFIED, 3)
    statistics.increment_value(OpStatisticsKey.FIELDS_PROCESSED, 14)
    statistics.increment_value(OpStatisticsKey.FIELDS_MODIFIED, 6)
    formatted: str = op_statistics_formatter.format(statistics)
    assert formatted == textwrap.dedent('''\
                                        Notes selected in Browser: 10
                                        Notes of type "N/A": 8
                                        Notes processed: 7
                                        Notes modified: 3
                                        Fields processed: 14
                                        Fields modified: 6''')
