from cross_field_highlighter.highlighter.formatter.underline_formatter import UnderlineFormatter
from cross_field_highlighter.highlighter.types import Word, Text


def test_highlight(underline_formatter: UnderlineFormatter):
    clean_word: Word = Word('ocean')
    highlighted_word: Word = underline_formatter.highlight(clean_word)
    assert highlighted_word == '<u class="cross-field-highlighter">ocean</u>'


def test_highlight_twice(underline_formatter: UnderlineFormatter):
    clean_word: Word = Word('ocean')
    highlighted_word_1: Word = underline_formatter.highlight(clean_word)
    highlighted_word_2: Word = underline_formatter.highlight(highlighted_word_1)
    assert highlighted_word_1 == '<u class="cross-field-highlighter">ocean</u>'
    assert highlighted_word_2 == '<u class="cross-field-highlighter">ocean</u>'


def test_erase(underline_formatter: UnderlineFormatter):
    highlighted_text: Text = Text('I see an <u class="cross-field-highlighter">ocean</u>.')
    clean_word: Text = underline_formatter.erase(highlighted_text)
    assert clean_word == "I see an ocean."


def test_erase_skip(underline_formatter: UnderlineFormatter):
    highlighted_text: Text = Text('I <u class="cross-field-highlighter">see</u> an <u>ocean</u>.')
    clean_text: Text = underline_formatter.erase(highlighted_text)
    assert clean_text == 'I see an <u>ocean</u>.'
