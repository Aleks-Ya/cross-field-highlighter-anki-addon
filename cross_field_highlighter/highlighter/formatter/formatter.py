from abc import abstractmethod, ABC

from ...highlighter.types import Word, Text


class Formatter(ABC):

    @abstractmethod
    def highlight(self, word: Word) -> Word:
        ...

    @abstractmethod
    def erase(self, text: Text) -> Text:
        ...
