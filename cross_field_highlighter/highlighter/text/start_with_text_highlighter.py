import re

from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter
from cross_field_highlighter.highlighter.types import Text, Word


class StartWithTextHighlighter(TextHighlighter):
    def __init__(self, formatter_facade: FormatterFacade):
        self.__formatter_facade: FormatterFacade = formatter_facade

    def highlight(self, collocation: str, text: str, stop_words: set[Word], highlight_format: HighlightFormat) -> Text:
        all_words: list[str] = collocation.split(" ")
        words: list[str] = self.__remove_stop_words(all_words, stop_words)
        words_regexp: list[str] = [fr"{word[:len(word) - 1]}\w*" if len(word) > 2 else word for word in words]
        base_collocation: str = ' '.join(words_regexp)
        return Text(re.sub(fr'((?<!<b>)(?<!<)(?<!</)\b{base_collocation}\b(?<!>)(?<!</b>))', r'<b>\1</b>',
                           text, flags=re.IGNORECASE))

    def erase(self, text: Text) -> Text:
        return self.__formatter_facade.erase(text)

    @staticmethod
    def __remove_stop_words(words: list[str], stop_words: set[Word]) -> list[str]:
        return [word for word in words if word not in stop_words]
