import re

from cross_field_highlighter.highlighter.formatter.formatter import Formatter
from cross_field_highlighter.highlighter.types import Word, Text


class TagFormatter(Formatter):
    def __init__(self, prefix: str, suffix: str):
        self.__prefix: str = prefix
        self.__suffix: str = suffix

    def highlight(self, word: Word) -> Word:
        already_highlighted: bool = self.__prefix in word and self.__suffix in word
        return Word(f"{self.__prefix}{word}{self.__suffix}") if not already_highlighted else word

    def erase(self, text: Text) -> Text:
        clean_text: str = re.sub(fr'{self.__prefix}(\w*){self.__suffix}', r'\1', text, flags=re.IGNORECASE)
        return Text(clean_text)
