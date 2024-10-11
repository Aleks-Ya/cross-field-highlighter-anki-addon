from cross_field_highlighter.highlighter.formatter.italic_formatter import ItalicFormatter
from cross_field_highlighter.highlighter.types import Word


def test_highlight(italic_formatter: ItalicFormatter):
    clean_word: Word = Word("ocean")
    highlighted_word: Word = italic_formatter.highlight(clean_word)
    assert highlighted_word == "<i>ocean</i>"


def test_highlight_twice(italic_formatter: ItalicFormatter):
    clean_word: Word = Word("ocean")
    highlighted_word_1: Word = italic_formatter.highlight(clean_word)
    highlighted_word_2: Word = italic_formatter.highlight(highlighted_word_1)
    assert highlighted_word_1 == "<i>ocean</i>"
    assert highlighted_word_2 == "<i>ocean</i>"


def test_erase(italic_formatter: ItalicFormatter):
    highlighted_word: Word = Word("<i>ocean</i>")
    clean_word: Word = italic_formatter.erase(highlighted_word)
    assert clean_word == "ocean"
