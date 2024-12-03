from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter
from cross_field_highlighter.highlighter.types import Text
from tests.data import Data


def test_cases(start_with_text_highlighter: StartWithTextHighlighter, td: Data, bold_format: HighlightFormat):
    for case in td.cases():
        print(f"Case: {case.name}")
        stop_words: Text = td.stop_words()
        highlighted_text_1: Text = start_with_text_highlighter.highlight(
            case.phrase, case.original_text, stop_words, bold_format)
        highlighted_text_2: Text = start_with_text_highlighter.highlight(
            case.phrase, case.highlighted_text, stop_words, bold_format)
        erased_text: Text = start_with_text_highlighter.erase(case.highlighted_text)
        assert highlighted_text_1 == case.highlighted_text
        assert highlighted_text_2 == case.highlighted_text
        assert erased_text == case.original_text
