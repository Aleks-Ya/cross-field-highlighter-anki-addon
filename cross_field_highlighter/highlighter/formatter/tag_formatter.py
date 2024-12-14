from re import Pattern, compile, escape, sub, IGNORECASE
import string

from ...highlighter.formatter.formatter import Formatter
from ...highlighter.types import Word, Text


class TagFormatter(Formatter):
    def __init__(self, tag: str):
        self.__highlight_prefix: str = f'<{tag} class="cross-field-highlighter">'
        self.__erase_prefix: str = f'<{tag}\\s+class="cross-field-highlighter">'
        self.__suffix: str = f'</{tag}>'
        self.__word_pattern: Pattern = compile(fr'{self.__erase_prefix}(\w*){self.__suffix}', flags=IGNORECASE)
        self.__punctuation_pattern: Pattern[str] = compile(
            fr"{self.__erase_prefix}([{escape(string.punctuation)}]){self.__suffix}", flags=IGNORECASE)
        self.__any_pattern: Pattern = compile(fr'{self.__erase_prefix}(.*){self.__suffix}', flags=IGNORECASE)

    def highlight(self, word: Word) -> Word:
        super().highlight(word)
        already_highlighted: bool = self.__highlight_prefix in word and self.__suffix in word
        return Word(f"{self.__highlight_prefix}{word}{self.__suffix}") if not already_highlighted else word

    def erase(self, text: Text) -> Text:
        super().erase(text)
        clean_text: Text = self.__erase_by_pattern(text, self.__word_pattern)
        clean_text = self.__erase_by_pattern(clean_text, self.__punctuation_pattern)
        clean_text = self.__erase_by_pattern(clean_text, self.__any_pattern)
        return clean_text

    @staticmethod
    def __erase_by_pattern(text: Text, pattern: Pattern) -> Text:
        unclear_text: str = text
        while True:
            clean_text: str = sub(pattern, r'\1', unclear_text)
            if clean_text == unclear_text:
                break
            unclear_text = clean_text
        return Text(clean_text)
