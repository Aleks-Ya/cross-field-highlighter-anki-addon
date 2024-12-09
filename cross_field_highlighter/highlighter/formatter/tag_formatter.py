import re

from ...highlighter.formatter.formatter import Formatter
from ...highlighter.types import Word, Text


class TagFormatter(Formatter):
    def __init__(self, tag: str):
        self.__prefix: str = f'<{tag} class="cross-field-highlighter">'
        self.__suffix: str = f'</{tag}>'

    def highlight(self, word: Word) -> Word:
        super().highlight(word)
        already_highlighted: bool = self.__prefix in word and self.__suffix in word
        return Word(f"{self.__prefix}{word}{self.__suffix}") if not already_highlighted else word

    def erase(self, text: Text) -> Text:
        super().erase(text)
        pattern: str = fr'{self.__prefix}(\w*){self.__suffix}'
        unclear_text: str = text
        while True:
            clean_text: str = re.sub(pattern, r'\1', unclear_text, flags=re.IGNORECASE)
            if clean_text == unclear_text:
                break
            unclear_text = clean_text
        return Text(clean_text)
