from cross_field_highlighter.highlighter.formatter.italic_formatter import ItalicFormatter
from cross_field_highlighter.highlighter.types import Word, Text


def test_highlight(italic_formatter: ItalicFormatter):
    clean_word: Word = Word("ocean")
    highlighted_word: Word = italic_formatter.highlight(clean_word)
    assert highlighted_word == '<i class="cross-field-highlighter">ocean</i>'


def test_highlight_twice(italic_formatter: ItalicFormatter):
    clean_word: Word = Word("ocean")
    highlighted_word_1: Word = italic_formatter.highlight(clean_word)
    highlighted_word_2: Word = italic_formatter.highlight(highlighted_word_1)
    assert highlighted_word_1 == '<i class="cross-field-highlighter">ocean</i>'
    assert highlighted_word_2 == '<i class="cross-field-highlighter">ocean</i>'


def test_erase(italic_formatter: ItalicFormatter):
    highlighted_text: Text = Text('I see an <i class="cross-field-highlighter">ocean</i>.')
    clean_word: Text = italic_formatter.erase(highlighted_text)
    assert clean_word == "I see an ocean."


def test_erase_skip(italic_formatter: ItalicFormatter):
    highlighted_text: Text = Text('I <i class="cross-field-highlighter">see</i> an <i>ocean</i>.')
    clean_text: Text = italic_formatter.erase(highlighted_text)
    assert clean_text == 'I see an <i>ocean</i>.'
