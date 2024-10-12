import re
import logging
from logging import Logger
from re import RegexFlag

from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokenizer
from cross_field_highlighter.highlighter.types import Text, Word

log: Logger = logging.getLogger(__name__)


class StartWithTextHighlighter(TextHighlighter):
    def __init__(self, formatter_facade: FormatterFacade, tokenizer: Tokenizer):
        self.__formatter_facade: FormatterFacade = formatter_facade
        self.__tokenizer: Tokenizer = tokenizer

    def highlight(self, collocation: Text, text: Text, stop_words: set[Word],
                  highlight_format: HighlightFormat) -> Text:
        collocation_words: set[Word] = set(self.__tokenizer.tokenize(collocation))
        collocation_words.discard(Word(" "))
        for stop_word in stop_words:
            collocation_words.discard(stop_word)
        highlighted_words: list[Word] = []
        text_words: list[Word] = self.__tokenizer.tokenize(text)
        for text_word in text_words:
            highlighted_word: Word = text_word
            for word in collocation_words:
                word_regexp: str = fr"{word[:len(word) - 1]}\w*" if len(word) > 2 else word
                if re.match(word_regexp, text_word, RegexFlag.IGNORECASE | RegexFlag.UNICODE):
                    highlighted_word: Word = self.__formatter_facade.format(text_word, highlight_format)
                    break
            highlighted_words.append(highlighted_word)
        return Text("".join(highlighted_words))

    def erase(self, text: Text) -> Text:
        return self.__formatter_facade.erase(text)
