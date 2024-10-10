from cross_field_highlighter.highlighter.formatter.bold_formatter import BoldFormatter
from cross_field_highlighter.highlighter.formatter.formatter import Formatter
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.formatter.italic_formatter import ItalicFormatter
from cross_field_highlighter.highlighter.types import Text, Word


class FormatterFacade:
    def __init__(self, bold_formatter: BoldFormatter, italic_formatter: ItalicFormatter):
        self.__bold_formatter: BoldFormatter = bold_formatter
        self.__italic_formatter: ItalicFormatter = italic_formatter
        self.__formatters: list[Formatter] = [self.__bold_formatter, self.__italic_formatter]
        self.__formatter_dict: dict[HighlightFormat, Formatter] = {
            HighlightFormat.BOLD: self.__bold_formatter,
            HighlightFormat.ITALIC: self.__italic_formatter
        }

    def format(self, word: Word, highlight_format: HighlightFormat) -> Word:
        formatter: Formatter = self.get_formatter(highlight_format)
        return formatter.highlight(word)

    def get_formatter(self, highlight_format: HighlightFormat) -> Formatter:
        return self.__formatter_dict.get(highlight_format)

    def erase(self, text: Text) -> Text:
        clean_text: Text = text
        for formatter in self.__formatters:
            clean_text = formatter.erase(clean_text)
        return clean_text
