from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormatCode, HighlightFormat


def test_str(formatter_facade: FormatterFacade):
    highlight_format: HighlightFormat = formatter_facade.get_format_by_code(HighlightFormatCode.BOLD)
    assert str(highlight_format) == "HighlightFormat(Bold, BOLD)"


def test_repr(formatter_facade: FormatterFacade):
    highlight_format: HighlightFormat = formatter_facade.get_format_by_code(HighlightFormatCode.BOLD)
    formats: list[HighlightFormat] = [highlight_format]
    assert str(formats) == "[HighlightFormat(Bold, BOLD)]"


def test_eq():
    highlight_format_1: HighlightFormat = HighlightFormat("Bold", HighlightFormatCode.BOLD)
    highlight_format_2: HighlightFormat = HighlightFormat("Bold", HighlightFormatCode.BOLD)
    assert highlight_format_1 == highlight_format_2
