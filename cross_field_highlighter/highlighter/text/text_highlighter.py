from abc import ABC, abstractmethod


class TextHighlighter(ABC):
    @abstractmethod
    def highlight(self, collocation: str, text: str, stop_words: set[str]) -> str:
        pass

    @abstractmethod
    def erase(self, text: str) -> str:
        pass
