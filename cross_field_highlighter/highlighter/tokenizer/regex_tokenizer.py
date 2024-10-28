import re
import string

from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokenizer
from cross_field_highlighter.highlighter.types import Word, Text, Words


class RegExTokenizer(Tokenizer):
    __punctuation = string.punctuation.replace("/", "").replace("<", "").replace(">", "")
    __punctuation_pattern: re.Pattern[str] = re.compile(f"([{re.escape(__punctuation)}])")

    def tokenize(self, text: Text) -> Words:
        super().tokenize(text)
        words: Words = Words([Word(word) for word in re.split(r'(\s)', text)])
        words_list: list[Words] = [Words(re.split(self.__punctuation_pattern, word)) for word in words]
        words2: Words = Words([item for sublist in words_list for item in sublist])
        non_empty_words: Words = Words([word for word in words2 if word != ''])
        return non_empty_words
