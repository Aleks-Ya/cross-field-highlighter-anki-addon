from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode
from cross_field_highlighter.highlighter.types import Text


def test_erase(formatter_facade: FormatterFacade):
    highlighted_text: Text = Text('I <b class="cross-field-highlighter">see</b> '
                                  'an <i class="cross-field-highlighter">ocean</i> '
                                  'on <b class="cross-field-highlighter">the</b> '
                                  '<i class="cross-field-highlighter">horizon</i>.')
    clean_text: Text = formatter_facade.erase(highlighted_text)
    assert clean_text == 'I see an ocean on the horizon.'


def test_erase_skip(formatter_facade: FormatterFacade):
    highlighted_text: Text = Text('I <b class="cross-field-highlighter">see</b> '
                                  'an <i class="cross-field-highlighter">ocean</i> '
                                  'on <b>the</b> '
                                  '<i>horizon</i>.')
    clean_text: Text = formatter_facade.erase(highlighted_text)
    assert clean_text == "I see an ocean on <b>the</b> <i>horizon</i>."


def test_get_all_formats(formatter_facade: FormatterFacade):
    assert formatter_facade.get_all_formats() == [HighlightFormat("Bold", HighlightFormatCode.BOLD),
                                                  HighlightFormat("Italic", HighlightFormatCode.ITALIC),
                                                  HighlightFormat("Underline", HighlightFormatCode.UNDERLINE),
                                                  HighlightFormat("Yellow background", HighlightFormatCode.MARK)]
