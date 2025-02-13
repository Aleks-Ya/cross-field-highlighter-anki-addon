from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note.field_highlighter import FieldHighlightResult, \
    NoteFieldEraseResult
from cross_field_highlighter.highlighter.note.regex_field_highlighter import RegexFieldHighlighter
from cross_field_highlighter.highlighter.types import FieldContent, Text
from tests.data import Data, DefaultFields


def test_cases(regex_field_highlighter: RegexFieldHighlighter, td: Data, bold_format: HighlightFormat):
    for case in td.cases():
        print(f"Case: {case.name}")

        case_original_text: Text = case.original_text
        note: Note = td.create_basic_note_1(FieldContent(case.collocation), FieldContent(case_original_text))
        stop_words: Text = td.stop_words()
        case_highlighted_text: Text = case.highlighted_text
        exp_was_modified: bool = case_original_text != case_highlighted_text

        # Highlight 1st time
        highlight_result_1: FieldHighlightResult = regex_field_highlighter.highlight(
            note, DefaultFields.basic_front, DefaultFields.basic_back, stop_words, bold_format)
        note_act: Note = highlight_result_1.note
        assert note_act[DefaultFields.basic_back] == case_highlighted_text
        assert highlight_result_1.was_modified() == exp_was_modified

        # Highlight again
        highlight_result_2: FieldHighlightResult = regex_field_highlighter.highlight(
            note, DefaultFields.basic_front, DefaultFields.basic_back, stop_words, bold_format)
        note_act: Note = highlight_result_2.note
        assert note_act[DefaultFields.basic_back] == case_highlighted_text
        assert not highlight_result_2.was_modified()

        # Erase 1st time
        erase_result_1: NoteFieldEraseResult = regex_field_highlighter.erase(note, DefaultFields.basic_back)
        assert erase_result_1.note[DefaultFields.basic_back] == case_original_text
        assert erase_result_1.was_modified() == exp_was_modified

        # Erase again
        erase_result_2: NoteFieldEraseResult = regex_field_highlighter.erase(note, DefaultFields.basic_back)
        assert erase_result_2.note[DefaultFields.basic_back] == case_original_text
        assert not erase_result_2.was_modified()
