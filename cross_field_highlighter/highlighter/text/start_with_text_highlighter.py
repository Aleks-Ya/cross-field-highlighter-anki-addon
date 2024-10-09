import re

from cross_field_highlighter.highlighter.text.text_highlighter import TextHighlighter


class StartWithTextHighlighter(TextHighlighter):

    def highlight(self, collocation: str, text: str, stop_words: set[str]) -> str:
        all_words: list[str] = collocation.split(" ")
        words: list[str] = self.__remove_stop_words(all_words, stop_words)
        words_regexp: list[str] = [fr"{word[:len(word) - 1]}\w*" if len(word) > 2 else word for word in words]
        base_collocation: str = ' '.join(words_regexp)
        return re.sub(fr'((?<!<b>)(?<!<)(?<!</)\b{base_collocation}\b(?<!>)(?<!</b>))', r'<b>\1</b>', text,
                      flags=re.IGNORECASE)

    def erase(self, text: str) -> str:
        out: str = text
        out = re.sub('<b>', '', out, flags=re.IGNORECASE)
        out = re.sub('</b>', '', out, flags=re.IGNORECASE)
        return out

    @staticmethod
    def __remove_stop_words(words: list[str], stop_words: set[str]) -> list[str]:
        return [word for word in words if word not in stop_words]
