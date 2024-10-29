import logging
from logging import Logger

from cross_field_highlighter.highlighter.formatter.formatter import Formatter
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat, HighlightFormatCode
from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter
from cross_field_highlighter.highlighter.types import Text, Word

log: Logger = logging.getLogger(__name__)


class FormatterFacade:
    def __init__(self):
        bold_formatter: TagFormatter = TagFormatter("b")
        italic_formatter: TagFormatter = TagFormatter("i")
        underline_formatter: TagFormatter = TagFormatter("u")
        mark_formatter: TagFormatter = TagFormatter("mark")
        self.__formatters: list[Formatter] = [bold_formatter, italic_formatter, underline_formatter, mark_formatter]
        self.__format_dict: dict[HighlightFormatCode, HighlightFormat] = {
            HighlightFormatCode.BOLD: HighlightFormat("Bold", HighlightFormatCode.BOLD),
            HighlightFormatCode.ITALIC: HighlightFormat("Italic", HighlightFormatCode.ITALIC),
            HighlightFormatCode.UNDERLINE: HighlightFormat("Underline", HighlightFormatCode.UNDERLINE),
            HighlightFormatCode.MARK: HighlightFormat("Yellow background", HighlightFormatCode.MARK)
        }
        self.__formatter_dict: dict[HighlightFormat, Formatter] = {
            self.__format_dict[HighlightFormatCode.BOLD]: bold_formatter,
            self.__format_dict[HighlightFormatCode.ITALIC]: italic_formatter,
            self.__format_dict[HighlightFormatCode.UNDERLINE]: underline_formatter,
            self.__format_dict[HighlightFormatCode.MARK]: mark_formatter
        }
        log.debug(f"{self.__class__.__name__} was instantiated")

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

    def get_format_by_code(self, highlight_format_code: HighlightFormatCode) -> HighlightFormat:
        return self.__format_dict[highlight_format_code]

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
