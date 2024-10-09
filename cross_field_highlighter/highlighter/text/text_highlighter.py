from abc import ABC, abstractmethod


class TextHighlighter(ABC):
    @abstractmethod
    def highlight(self, collocation: str, text: str) -> str:
        pass

    @abstractmethod
    def erase(self, text: str) -> str:
        pass
