from abc import ABC, abstractmethod

from cross_field_highlighter.highlighter.types import Text, Words


class Tokenizer(ABC):

    @abstractmethod
    def tokenize(self, text: Text) -> Words:
        ...

    def tokenize_distinct(self, text: Text) -> Words:
        return Words(list(set(self.tokenize(text))))
