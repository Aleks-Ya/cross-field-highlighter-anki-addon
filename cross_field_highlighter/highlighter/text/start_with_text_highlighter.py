import re
import logging
from logging import Logger
from re import RegexFlag

from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.highlighter.types import Text, Word

log: Logger = logging.getLogger(__name__)


class StartWithTextHighlighter(TextHighlighter):
    def __init__(self, formatter_facade: FormatterFacade):
        self.__formatter_facade: FormatterFacade = formatter_facade

    def highlight(self, collocation: Text, text: Text, stop_words: set[Word],
                  highlight_format: HighlightFormat) -> Text:
        collocation_words: set[Word] = {Word(word) for word in collocation.split(" ")}
        highlighted_words: list[Word] = []
        for word in collocation_words:
            if word in stop_words:
                log.debug(f"Skip stop word: {word}")
                continue
            word_regexp: str = fr"{word[:len(word) - 1]}\w*" if len(word) > 2 else word
            text_words: list[Word] = [Word(word) for word in text.split(" ")]
            for text_word in text_words:
                if re.match(word_regexp, text_word, RegexFlag.IGNORECASE | RegexFlag.UNICODE):
                    highlighted_word: Word = self.__formatter_facade.format(text_word, highlight_format)
                    highlighted_words.append(highlighted_word)
                else:
                    highlighted_words.append(text_word)
        return Text(" ".join(highlighted_words))

    def erase(self, text: Text) -> Text:
        return self.__formatter_facade.erase(text)
