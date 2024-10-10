from cross_field_highlighter.highlighter.formatter.italic_formatter import ItalicFormatter
from cross_field_highlighter.highlighter.types import Word, Text


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
    highlighted_text: Text = Text("The <i>ocean</i> is calm.")
    clean_text: Text = italic_formatter.erase(highlighted_text)
    assert clean_text == "The ocean is calm."
