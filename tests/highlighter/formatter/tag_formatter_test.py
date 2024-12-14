import pytest

from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter
from cross_field_highlighter.highlighter.types import Word, Text


@pytest.fixture
def tag_formatter() -> TagFormatter:
    return TagFormatter("b")


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


def test_erase_skip_alien_formatting(tag_formatter: TagFormatter):
    highlighted_text: Text = Text('I <b class="cross-field-highlighter">see</b> an <b>ocean</b>.')
    clean_text: Text = tag_formatter.erase(highlighted_text)
    assert clean_text == 'I see an <b>ocean</b>.'


def test_erase_double_highlighted(tag_formatter: TagFormatter):
    highlighted_text: Text = Text(
        'I see an <b class="cross-field-highlighter"><b class="cross-field-highlighter">ocean</b></b>.')
    clean_word: Text = tag_formatter.erase(highlighted_text)
    assert clean_word == "I see an ocean."


def test_erase_square_brackets(tag_formatter: TagFormatter):
    highlighted_text: Text = Text(
        'I see an <b class="cross-field-highlighter">[</b>ocean<b class="cross-field-highlighter">]</b>.')
    clean_word: Text = tag_formatter.erase(highlighted_text)
    assert clean_word == "I see an [ocean]."


def test_erase_slash(tag_formatter: TagFormatter):
    highlighted_text: Text = Text('I see an <b class="cross-field-highlighter">ocean/sea</b>.')
    clean_word: Text = tag_formatter.erase(highlighted_text)
    assert clean_word == "I see an ocean/sea."


def test_different_separators_within_tag(tag_formatter: TagFormatter):
    assert tag_formatter.erase(Text('<b class="cross-field-highlighter">space</b>')) == 'space'
    assert tag_formatter.erase(Text('<b\nclass="cross-field-highlighter">linebreak</b>')) == 'linebreak'
    assert tag_formatter.erase(Text('<b\tclass="cross-field-highlighter">tab</b>')) == 'tab'
    assert tag_formatter.erase(Text('<b \n\tclass="cross-field-highlighter">several</b>')) == 'several'


def test_erase_several_tags(tag_formatter: TagFormatter):
    highlighted_text: Text = Text(
        'Immediately <b class="cross-field-highlighter">hang up</b>. Before you <b class="cross-field-highlighter">hang up</b>.')
    clean_word: Text = tag_formatter.erase(highlighted_text)
    assert clean_word == 'Immediately hang up. Before you hang up.'
