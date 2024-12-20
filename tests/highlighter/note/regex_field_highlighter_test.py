from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note.field_highlighter import FieldHighlightResult, \
    NoteFieldEraseResult
from cross_field_highlighter.highlighter.note.regex_field_highlighter import RegexFieldHighlighter
from cross_field_highlighter.highlighter.types import FieldContent, Text
from tests.data import Data, DefaultFields


def test_cases_space_delimited(regex_field_highlighter: RegexFieldHighlighter, td: Data,
                               bold_format: HighlightFormat):
    space_delimited_language: bool = True
    __highlight_erase(bold_format, space_delimited_language, regex_field_highlighter, td)


def test_cases_non_space_delimited(regex_field_highlighter: RegexFieldHighlighter, td: Data,
                                   bold_format: HighlightFormat):
    space_delimited_language: bool = False
    __highlight_erase(bold_format, space_delimited_language, regex_field_highlighter, td)


def __highlight_erase(bold_format: HighlightFormat, space_delimited_language: bool,
                      regex_field_highlighter: RegexFieldHighlighter, td: Data):
    for case in td.cases():
        print(f"Case: {case.name}")

        note: Note = td.create_basic_note_1(FieldContent(case.collocation), FieldContent(case.original_text))
        stop_words: Text = td.stop_words()
        case_highlighted_text: Text = case.highlighted_text_space_delimited if space_delimited_language else case.highlighted_text_non_space_delimited

        # Highlight 1st time
        highlight_result_1: FieldHighlightResult = regex_field_highlighter.highlight(
            note, DefaultFields.basic_front, DefaultFields.basic_back, stop_words, space_delimited_language,
            bold_format)
        note_act: Note = highlight_result_1.note
        assert note_act[DefaultFields.basic_back] == case_highlighted_text

        # Highlight again
        highlight_result_2: FieldHighlightResult = regex_field_highlighter.highlight(
            note, DefaultFields.basic_front, DefaultFields.basic_back, stop_words, space_delimited_language,
            bold_format)
        note_act: Note = highlight_result_2.note
        assert note_act[DefaultFields.basic_back] == case_highlighted_text

        # Erase
        erase_result: NoteFieldEraseResult = regex_field_highlighter.erase(note, DefaultFields.basic_back)
        assert erase_result.note[DefaultFields.basic_back] == case.original_text
