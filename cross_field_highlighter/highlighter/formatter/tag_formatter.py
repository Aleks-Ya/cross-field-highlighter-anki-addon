from cross_field_highlighter.highlighter.formatter.formatter import Formatter
from cross_field_highlighter.highlighter.types import Word


class TagFormatter(Formatter):
    def __init__(self, prefix: str, suffix: str):
        self.__prefix: str = prefix
        self.__suffix: str = suffix

    def highlight(self, word: Word) -> Word:
        already_highlighted: bool = word.startswith(self.__prefix) and word.endswith(self.__suffix)
        return Word(f"{self.__prefix}{word}{self.__suffix}") if not already_highlighted else word

    def erase(self, word: Word) -> Word:
        if self.__prefix in word and self.__suffix in word:
            clean_word = Word(word.replace(self.__prefix, "").replace(self.__suffix, ""))
        else:
            clean_word: Word = word
        return clean_word
