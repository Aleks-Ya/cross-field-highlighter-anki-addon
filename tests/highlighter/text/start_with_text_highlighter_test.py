from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
from cross_field_highlighter.highlighter.types import Word
from tests.data import Data


def test_cases(start_with_text_highlighter: StartWithTextHighlighter, td: Data, bold_format: HighlightFormat):
    for case in td.cases():
        print(f"Case: {case.name}")
        stop_words: set[Word] = td.stop_words()
        assert start_with_text_highlighter.highlight(case.phrase, case.original_text, stop_words,
                                                     bold_format) == case.highlighted_text
        assert start_with_text_highlighter.highlight(case.phrase, case.highlighted_text, stop_words,
                                                     bold_format) == case.highlighted_text
        assert case.original_text == start_with_text_highlighter.erase(case.highlighted_text)
