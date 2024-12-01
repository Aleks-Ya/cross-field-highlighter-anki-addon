from re import Pattern, split, compile, escape
import string

from ...highlighter.tokenizer.tokenizer import Tokenizer
from ...highlighter.types import Text, Words, Word


class RegExTokenizer(Tokenizer):
    def __init__(self):
        self.__punctuation_pattern: Pattern[str] = self.__create_punctuation_pattern()

    def tokenize(self, text: Text) -> Words:
        super().tokenize(text)
        words: Words = Words([Word(text)])
        by_space: Words = self.__split_by_spaces(words)
        by_tags: Words = self.__split_by_tags(by_space)
        by_punctuation: Words = self.__split_by_punctuation(by_tags)
        non_empty: Words = self.__remove_empty_words(by_punctuation)
        return non_empty

    @staticmethod
    def __create_punctuation_pattern() -> Pattern[str]:
        punctuation: str = string.punctuation.replace("/", "").replace("<", "").replace(">", "")
        punctuation_escaped: str = escape(punctuation)
        punctuation_pattern: Pattern[str] = compile(f"([{punctuation_escaped}])")
        return punctuation_pattern

    @staticmethod
    def __remove_empty_words(words: Words):
        return Words([word for word in words if word != ''])

    def __split_by_punctuation(self, words: Words) -> Words:
        words: list[Words] = [Words(split(self.__punctuation_pattern, word)) for word in words]
        return self.__flatten(words)

    def __split_by_tags(self, words: Words) -> Words:
        pattern: Pattern[str] = compile(f"(<[^>]+>)")
        words: list[Words] = [Words(split(pattern, word)) for word in words]
        return self.__flatten(words)

    def __split_by_spaces(self, words: Words) -> Words:
        words: list[Words] = [Words(split(r'(\s)', word)) for word in words]
        return self.__flatten(words)

    @staticmethod
    def __flatten(words_list: list[Words]) -> Words:
        return Words([item for sublist in words_list for item in sublist])
