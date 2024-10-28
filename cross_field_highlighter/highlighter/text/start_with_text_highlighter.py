import re
import logging
from logging import Logger
from re import RegexFlag

from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.highlighter.tokenizer.stop_words_tokenizer import StopWordsTokenizer
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokenizer
from cross_field_highlighter.highlighter.types import Text, Word, Words

log: Logger = logging.getLogger(__name__)


class StartWithTextHighlighter(TextHighlighter):
    __space: Word = Word(" ")

    def __init__(self, formatter_facade: FormatterFacade, tokenizer: Tokenizer,
                 stop_words_tokenizer: StopWordsTokenizer):
        self.__formatter_facade: FormatterFacade = formatter_facade
        self.__tokenizer: Tokenizer = tokenizer
        self.__stop_words_tokenizer: StopWordsTokenizer = stop_words_tokenizer

    def highlight(self, collocation: Text, text: Text, stop_words: Text,
                  highlight_format: HighlightFormat) -> Text:
        super().highlight(collocation, text, stop_words, highlight_format)
        collocation_words: Words = Words(self.__tokenizer.tokenize_distinct(collocation))
        if self.__space in collocation_words:
            collocation_words.remove(self.__space)
        stop_words_tokenized: Words = self.__stop_words_tokenizer.tokenize(stop_words)
        for stop_word in stop_words_tokenized:
            if stop_word in collocation_words:
                collocation_words.remove(stop_word)
        highlighted_words: Words = Words([])
        clean_text: Text = self.erase(text)
        text_words: Words = self.__tokenizer.tokenize(clean_text)
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
        super().erase(text)
        return self.__formatter_facade.erase(text)
