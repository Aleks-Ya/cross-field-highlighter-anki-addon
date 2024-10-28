import logging
from logging import Logger

from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokenizer
from cross_field_highlighter.highlighter.types import Words, Word, Text

log: Logger = logging.getLogger(__name__)


class StopWordsTokenizer(Tokenizer):
    def __init__(self):
        self.__cache: dict[Text, Words] = {}
        log.debug(f"{self.__class__.__name__} was instantiated")

    def tokenize(self, text: Text) -> Words:
        if text not in self.__cache:
            stop_words: Words = Words([Word(word) for word in text.split(" ")]) if text else Words([])
            self.__cache[text] = Words(list(dict.fromkeys(stop_words)))
        return self.__cache[text]
