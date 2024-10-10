from cross_field_highlighter.highlighter.formatter.bold_formatter import BoldFormatter
from cross_field_highlighter.highlighter.types import Word, Text


def test_highlight(bold_formatter: BoldFormatter):
    clean_word: Word = Word("ocean")
    highlighted_word: Word = bold_formatter.highlight(clean_word)
    assert highlighted_word == "<b>ocean</b>"


def test_highlight_twice(bold_formatter: BoldFormatter):
    clean_word: Word = Word("ocean")
    highlighted_word_1: Word = bold_formatter.highlight(clean_word)
    highlighted_word_2: Word = bold_formatter.highlight(highlighted_word_1)
    assert highlighted_word_1 == "<b>ocean</b>"
    assert highlighted_word_2 == "<b>ocean</b>"


def test_erase(bold_formatter: BoldFormatter):
    highlighted_text: Text = Text("The <b>ocean</b> is calm.")
    clean_text: Text = bold_formatter.erase(highlighted_text)
    assert clean_text == "The ocean is calm."
