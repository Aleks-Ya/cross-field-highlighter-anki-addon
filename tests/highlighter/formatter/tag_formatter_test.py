import pytest

from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter
from cross_field_highlighter.highlighter.types import Word, Text


@pytest.fixture
def tag_formatter() -> TagFormatter:
    return TagFormatter(f'<b class="{TagFormatter.css_class}">', "</b>")


def test_highlight(tag_formatter: TagFormatter):
    clean_word: Word = Word('ocean')
    highlighted_word: Word = tag_formatter.highlight(clean_word)
    assert highlighted_word == '<b class="cross-field-highlighter">ocean</b>'


def test_highlight_twice(tag_formatter: TagFormatter):
    clean_word: Word = Word('ocean')
    highlighted_word_1: Word = tag_formatter.highlight(clean_word)
    highlighted_word_2: Word = tag_formatter.highlight(highlighted_word_1)
    assert highlighted_word_1 == '<b class="cross-field-highlighter">ocean</b>'
    assert highlighted_word_2 == '<b class="cross-field-highlighter">ocean</b>'


def test_erase(tag_formatter: TagFormatter):
    highlighted_text: Text = Text('I see an <b class="cross-field-highlighter">ocean</b>.')
    clean_word: Text = tag_formatter.erase(highlighted_text)
    assert clean_word == "I see an ocean."


def test_erase_skip(tag_formatter: TagFormatter):
    highlighted_text: Text = Text('I <b class="cross-field-highlighter">see</b> an <b>ocean</b>.')
    clean_text: Text = tag_formatter.erase(highlighted_text)
    assert clean_text == 'I see an <b>ocean</b>.'
