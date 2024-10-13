from cross_field_highlighter.highlighter.formatter.mark_formatter import MarkFormatter
from cross_field_highlighter.highlighter.types import Word, Text


def test_highlight(mark_formatter: MarkFormatter):
    clean_word: Word = Word('ocean')
    highlighted_word: Word = mark_formatter.highlight(clean_word)
    assert highlighted_word == '<mark class="cross-field-highlighter">ocean</mark>'


def test_highlight_twice(mark_formatter: MarkFormatter):
    clean_word: Word = Word('ocean')
    highlighted_word_1: Word = mark_formatter.highlight(clean_word)
    highlighted_word_2: Word = mark_formatter.highlight(highlighted_word_1)
    assert highlighted_word_1 == '<mark class="cross-field-highlighter">ocean</mark>'
    assert highlighted_word_2 == '<mark class="cross-field-highlighter">ocean</mark>'


def test_erase(mark_formatter: MarkFormatter):
    highlighted_text: Text = Text('I see an <mark class="cross-field-highlighter">ocean</mark>.')
    clean_word: Text = mark_formatter.erase(highlighted_text)
    assert clean_word == "I see an ocean."


def test_erase_skip(mark_formatter: MarkFormatter):
    highlighted_text: Text = Text('I <mark class="cross-field-highlighter">see</mark> an <mark>ocean</mark>.')
    clean_text: Text = mark_formatter.erase(highlighted_text)
    assert clean_text == 'I see an <mark>ocean</mark>.'
