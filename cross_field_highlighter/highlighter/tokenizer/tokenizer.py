from abc import ABC, abstractmethod

from ...highlighter.types import Text, Words


class Tokenizer(ABC):

    @abstractmethod
    def tokenize(self, text: Text) -> Words:
        ...

    def tokenize_distinct(self, text: Text) -> Words:
        return Words(list(set(self.tokenize(text))))
