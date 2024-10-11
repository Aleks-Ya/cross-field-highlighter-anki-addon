from abc import ABC, abstractmethod

from cross_field_highlighter.highlighter.types import Word


class Formatter(ABC):

    @abstractmethod
    def highlight(self, word: Word) -> Word:
        pass

    @abstractmethod
    def erase(self, word: Word) -> Word:
        pass
