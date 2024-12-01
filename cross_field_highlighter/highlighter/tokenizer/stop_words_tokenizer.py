import logging
from logging import Logger

from ...highlighter.tokenizer.tokenizer import Tokenizer, Tokens, TokenType, Token
from ...highlighter.types import Word, Text

log: Logger = logging.getLogger(__name__)


class StopWordsTokenizer(Tokenizer):
    def __init__(self):
        self.__cache: dict[Text, Tokens] = {}
        log.debug(f"{self.__class__.__name__} was instantiated")

    def tokenize(self, text: Text) -> Tokens:
        if text not in self.__cache:
            stop_words: Tokens = Tokens(
                [Token(Word(word), TokenType.WORD) for word in text.split(" ")]) if text else Tokens([])
            self.__cache[text] = Tokens(list(dict.fromkeys(stop_words)))
        return self.__cache[text]
