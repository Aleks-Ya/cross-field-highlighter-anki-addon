import timeit

import pytest

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.text.regex_text_highlighter import RegexTextHighlighter
from cross_field_highlighter.highlighter.types import Text
from tests.data import Data


def test_cases(regex_text_highlighter: RegexTextHighlighter, td: Data, bold_format: HighlightFormat):
    for case in td.cases():
        print(f"Case: {case.name}")
        stop_words: Text = td.stop_words()
        case_original_text: Text = case.original_text
        case_highlighted_text: Text = case.highlighted_text
        highlighted_text_1: Text = regex_text_highlighter.highlight(
            case.collocation, case_original_text, stop_words, bold_format)
        highlighted_text_2: Text = regex_text_highlighter.highlight(
            case.collocation, case_highlighted_text, stop_words, bold_format)
        erased_text_1: Text = regex_text_highlighter.erase(case_highlighted_text)
        erased_text_2: Text = regex_text_highlighter.erase(erased_text_1)
        assert highlighted_text_1 == case_highlighted_text
        assert highlighted_text_2 == case_highlighted_text
        assert erased_text_1 == case_original_text
        assert erased_text_2 == case_original_text


@pytest.mark.performance
def test_highlight_performance(regex_text_highlighter: RegexTextHighlighter, bold_format: HighlightFormat):
    stop_words: Text = Text("a an to")
    original_text: Text = Text("Downloading a movie takes forever.")
    collocation: Text = Text("take forever")
    execution_time: float = timeit.timeit(
        lambda: regex_text_highlighter.highlight(collocation, original_text, stop_words, bold_format), number=1000)
    print(f"Execution time: {execution_time}")
    assert execution_time <= 1
