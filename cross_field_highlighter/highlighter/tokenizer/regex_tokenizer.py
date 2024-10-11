import re

from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokenizer
from cross_field_highlighter.highlighter.types import Word, Text


class RegExTokenizer(Tokenizer):

    def tokenize(self, text: Text) -> list[Word]:
        return [Word(word) for word in re.split(r'\s', text)]
