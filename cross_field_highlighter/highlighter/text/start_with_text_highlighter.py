import re
from typing import List

from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter


class StartWithTextHighlighter(TextHighlighter):

    def highlight(self, collocation: str, text: str) -> str:
        collocation = self.__remove_prefix(collocation)
        words: List[str] = collocation.split(" ")
        words_regexp: List[str] = [fr"{word[:len(word) - 1]}\w*" if len(word) > 2 else word for word in words]
        base_collocation: str = ' '.join(words_regexp)
        return re.sub(fr'((?<!<b>)(?<!<)(?<!</)\b{base_collocation}\b(?<!>)(?<!</b>))', r'<b>\1</b>', text,
                      flags=re.IGNORECASE)

    def erase(self, text: str) -> str:
        out: str = text
        out = re.sub('<b>', '', out, flags=re.IGNORECASE)
        out = re.sub('</b>', '', out, flags=re.IGNORECASE)
        return out

    @staticmethod
    def __remove_prefix(word: str) -> str:
        prefixes: List[str] = ["to ", "a ", "an "]
        for prefix in prefixes:
            word = word[len(prefix):] if word.startswith(prefix) else word
        return word
