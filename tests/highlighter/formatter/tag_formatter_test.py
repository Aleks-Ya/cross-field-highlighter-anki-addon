import pytest

from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter
from cross_field_highlighter.highlighter.types import Word, Text


@pytest.fixture
def tag_formatter() -> TagFormatter:
    return TagFormatter("<b>", "</b>")


def test_highlight(tag_formatter: TagFormatter):
    clean_word: Word = Word("ocean")
    highlighted_word: Word = tag_formatter.highlight(clean_word)
    assert highlighted_word == "<b>ocean</b>"


def test_highlight_twice(tag_formatter: TagFormatter):
    clean_word: Word = Word("ocean")
    highlighted_word_1: Word = tag_formatter.highlight(clean_word)
    highlighted_word_2: Word = tag_formatter.highlight(highlighted_word_1)
    assert highlighted_word_1 == "<b>ocean</b>"
    assert highlighted_word_2 == "<b>ocean</b>"


def test_erase(tag_formatter: TagFormatter):
    highlighted_text: Text = Text("The <b>ocean</b> is calm.")
    clean_text: Text = tag_formatter.erase(highlighted_text)
    assert clean_text == "The ocean is calm."
