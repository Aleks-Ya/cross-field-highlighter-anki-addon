from abc import ABC, abstractmethod

from cross_field_highlighter.highlighter.types import Word, Text


class Tokenizer(ABC):

    @abstractmethod
    def tokenize(self, text: Text) -> list[Word]:
        ...
