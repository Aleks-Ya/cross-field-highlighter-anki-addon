import re

from cross_field_highlighter.highlighter.formatter.formatter import Formatter
from cross_field_highlighter.highlighter.types import Word, Text


class ItalicFormatter(Formatter):
    __prefix: str = "<i>"
    __suffix: str = "</i>"

    def highlight(self, word: Word) -> Word:
        already_highlighted: bool = word.startswith(self.__prefix) and word.endswith(self.__suffix)
        return Word(f"{self.__prefix}{word}{self.__suffix}") if not already_highlighted else word

    def erase(self, text: Text) -> Text:
        out: str = text
        out = re.sub(self.__prefix, '', out, flags=re.IGNORECASE)
        out = re.sub(self.__suffix, '', out, flags=re.IGNORECASE)
        return Text(out)
