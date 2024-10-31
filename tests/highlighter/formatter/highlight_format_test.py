from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormatCode, HighlightFormat, \
    HighlightFormats


def test_str(bold_format: HighlightFormat):
    assert str(bold_format) == "HighlightFormat(Bold, BOLD)"


def test_repr(bold_format: HighlightFormat):
    formats: HighlightFormats = HighlightFormats([bold_format])
    assert str(formats) == "[HighlightFormat(Bold, BOLD)]"


def test_eq():
    highlight_format_1: HighlightFormat = HighlightFormat("Bold", HighlightFormatCode.BOLD)
    highlight_format_2: HighlightFormat = HighlightFormat("Bold", HighlightFormatCode.BOLD)
    assert highlight_format_1 == highlight_format_2
