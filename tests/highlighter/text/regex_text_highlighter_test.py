from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.text.regex_text_highlighter import RegexTextHighlighter
from cross_field_highlighter.highlighter.types import Text
from tests.data import Data


def test_cases_space_delimited(regex_text_highlighter: RegexTextHighlighter, td: Data,
                               bold_format: HighlightFormat):
    space_delimited_language: bool = True
    __highlight_erase(bold_format, space_delimited_language, regex_text_highlighter, td)


def test_cases_non_space_delimited(regex_text_highlighter: RegexTextHighlighter, td: Data,
                                   bold_format: HighlightFormat):
    space_delimited_language: bool = False
    __highlight_erase(bold_format, space_delimited_language, regex_text_highlighter, td)


def __highlight_erase(bold_format: HighlightFormat, space_delimited_language: bool,
                      regex_text_highlighter: RegexTextHighlighter, td: Data):
    for case in td.cases():
        print(f"Case: {case.name}")
        stop_words: Text = td.stop_words()
        case_highlighted_text: Text = case.highlighted_text_space_delimited if space_delimited_language else case.highlighted_text_non_space_delimited
        highlighted_text_1: Text = regex_text_highlighter.highlight(
            case.collocation, case.original_text, stop_words, space_delimited_language, bold_format)
        highlighted_text_2: Text = regex_text_highlighter.highlight(
            case.collocation, case_highlighted_text, stop_words, space_delimited_language, bold_format)
        erased_text: Text = regex_text_highlighter.erase(case_highlighted_text)
        assert highlighted_text_1 == case_highlighted_text
        assert highlighted_text_2 == case_highlighted_text
        assert erased_text == case.original_text
