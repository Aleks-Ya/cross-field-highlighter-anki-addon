from abc import ABC, abstractmethod

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import Text


class TextHighlighter(ABC):
    @abstractmethod
    def highlight(self, collocation: str, text: str, stop_words: set[str], highlight_format: HighlightFormat) -> str:
        pass

    @abstractmethod
    def erase(self, text: Text) -> Text:
        pass
