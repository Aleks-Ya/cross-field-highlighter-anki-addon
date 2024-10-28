from abc import ABC, abstractmethod

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import Text


class TextHighlighter(ABC):
    @abstractmethod
    def highlight(self, collocation: Text, text: Text, stop_words: Text, highlight_format: HighlightFormat) -> Text:
        ...

    @abstractmethod
    def erase(self, text: Text) -> Text:
        ...
