from cross_field_highlighter.ui.operation.op_statistics import OpStatistics
from cross_field_highlighter.ui.operation.op_statistics_formatter import OpStatisticsFormatter


def test_format(op_statistics_formatter: OpStatisticsFormatter):
    statistics: OpStatistics = OpStatistics()
    statistics.set_notes_selected(10)
    statistics.increment_notes_processed(7)
    statistics.increment_notes_modified(3)
    formatted: str = op_statistics_formatter.format(statistics)
    assert formatted == "Notes selected in Browser: 10\nNotes processed: 7\nNotes modified: 3"
