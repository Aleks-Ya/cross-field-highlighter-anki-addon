import re
import logging
from logging import Logger
from re import RegexFlag

from ...highlighter.formatter.formatter_facade import FormatterFacade
from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.text.text_highlighter import TextHighlighter
from ...highlighter.tokenizer.stop_words_tokenizer import StopWordsTokenizer
from ...highlighter.tokenizer.tokenizer import Tokenizer, Tokens, Token
from ...highlighter.types import Text, Word, Words

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
        collocation_tokens: Tokens = self.__tokenizer.tokenize_distinct(collocation)
        collocation_tokens.delete_word(self.__space)
        stop_words_tokenized: Tokens = self.__stop_words_tokenizer.tokenize(stop_words)
        for stop_token in stop_words_tokenized:
            collocation_tokens.delete_word(stop_token.word)
        highlighted_words: Words = Words([])
        clean_text: Text = self.erase(text)
        text_tokens: Tokens = self.__tokenizer.tokenize(clean_text)
        for text_token in text_tokens:
            highlighted_text_word: Word = self.__highlight_token(collocation_tokens, text_token, highlight_format)
            highlighted_words.append(highlighted_text_word)
        return Text("".join(highlighted_words))

    def erase(self, text: Text) -> Text:
        super().erase(text)
        return self.__formatter_facade.erase(text)

    def __highlight_token(self, collocation_tokens: Tokens, text_token: Token,
                          highlight_format: HighlightFormat) -> Word:
        highlighted_text_word: Word = text_token.word
        for collocation_token in collocation_tokens:
            collocation_word: Word = collocation_token.word
            collocation_word_length: int = len(collocation_word)
            word_regexp: str = fr"{collocation_word[:collocation_word_length - 1]}\w*" if collocation_word_length > 2 else collocation_word
            if re.match(word_regexp, text_token.word, RegexFlag.IGNORECASE | RegexFlag.UNICODE):
                highlighted_text_word = self.__formatter_facade.format(text_token.word, highlight_format)
                break
        return highlighted_text_word
