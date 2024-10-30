from cross_field_highlighter.ui.operation.op_statistics import OpStatistics, OpStatisticsKey
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter


def test_format(op_statistics_formatter: OpStatisticsFormatter):
    statistics: OpStatistics = OpStatistics()
    statistics.set_value(OpStatisticsKey.NOTES_SELECTED, 10)
    statistics.increment_value(OpStatisticsKey.NOTES_PROCESSED, 7)
    statistics.increment_value(OpStatisticsKey.NOTES_MODIFIED, 3)
    formatted: str = op_statistics_formatter.format(statistics)
    assert formatted == "Notes selected in Browser: 10\nNotes processed: 7\nNotes modified: 3"
