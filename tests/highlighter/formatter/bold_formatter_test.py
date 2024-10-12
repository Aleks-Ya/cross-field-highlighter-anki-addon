from cross_field_highlighter.highlighter.formatter.bold_formatter import BoldFormatter
from cross_field_highlighter.highlighter.types import Word, Text


def test_highlight(bold_formatter: BoldFormatter):
    clean_word: Word = Word('ocean')
    highlighted_word: Word = bold_formatter.highlight(clean_word)
    assert highlighted_word == '<b class="cross-field-highlighter">ocean</b>'


def test_highlight_twice(bold_formatter: BoldFormatter):
    clean_word: Word = Word('ocean')
    highlighted_word_1: Word = bold_formatter.highlight(clean_word)
    highlighted_word_2: Word = bold_formatter.highlight(highlighted_word_1)
    assert highlighted_word_1 == '<b class="cross-field-highlighter">ocean</b>'
    assert highlighted_word_2 == '<b class="cross-field-highlighter">ocean</b>'


def test_erase(bold_formatter: BoldFormatter):
    highlighted_text: Text = Text('I see an <b class="cross-field-highlighter">ocean</b>.')
    clean_word: Text = bold_formatter.erase(highlighted_text)
    assert clean_word == "I see an ocean."


def test_erase_skip(bold_formatter: BoldFormatter):
    highlighted_text: Text = Text('I <b class="cross-field-highlighter">see</b> an <b>ocean</b>.')
    clean_text: Text = bold_formatter.erase(highlighted_text)
    assert clean_text == 'I see an <b>ocean</b>.'
