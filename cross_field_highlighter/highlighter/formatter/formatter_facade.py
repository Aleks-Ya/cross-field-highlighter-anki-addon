from cross_field_highlighter.highlighter.formatter.formatter import Formatter
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokenizer
from cross_field_highlighter.highlighter.types import Text, Word


class FormatterFacade:
    def __init__(self, tokenizer: Tokenizer):
        self.__tokenizer: Tokenizer = tokenizer
        bold_formatter: TagFormatter = TagFormatter("b")
        italic_formatter: TagFormatter = TagFormatter("i")
        underline_formatter: TagFormatter = TagFormatter("u")
        mark_formatter: TagFormatter = TagFormatter("mark")
        self.__formatters: list[Formatter] = [bold_formatter, italic_formatter, underline_formatter, mark_formatter]
        self.__formatter_dict: dict[HighlightFormat, Formatter] = {
            HighlightFormat.BOLD: bold_formatter,
            HighlightFormat.ITALIC: italic_formatter,
            HighlightFormat.UNDERLINE: underline_formatter,
            HighlightFormat.MARK: mark_formatter
        }

    def format(self, word: Word, highlight_format: HighlightFormat) -> Word:
        formatter: Formatter = self.get_formatter(highlight_format)
        return formatter.highlight(word)

    def get_formatter(self, highlight_format: HighlightFormat) -> Formatter:
        return self.__formatter_dict.get(highlight_format)

    def erase(self, text: Text) -> Text:
        clean_text: Text = text
        for formatter in self.__formatters:
            clean_text: Text = formatter.erase(clean_text)
        return clean_text

    def get_all_formats(self) -> list[HighlightFormat]:
        return list(self.__formatter_dict.keys())
