import re
import string

from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokenizer
from cross_field_highlighter.highlighter.types import Word, Text


class RegExTokenizer(Tokenizer):
    __punctuation = string.punctuation.replace("/", "").replace("<", "").replace(">", "")
    __punctuation_pattern: re.Pattern[str] = re.compile(f"([{re.escape(__punctuation)}])")

    def tokenize(self, text: Text) -> list[Word]:
        words: list[Word] = [Word(word) for word in re.split(r'(\s)', text)]
        words_list: list[list[Word]] = [re.split(self.__punctuation_pattern, word) for word in words]
        words2: list[Word] = [item for sublist in words_list for item in sublist]
        return words2
