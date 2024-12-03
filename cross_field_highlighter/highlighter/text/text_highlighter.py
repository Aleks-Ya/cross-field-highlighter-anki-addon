from abc import ABC, abstractmethod

from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.types import Text


class TextHighlighter(ABC):
    @abstractmethod
    def highlight(self, collocation: Text, text: Text, stop_words: Text, space_delimited_language: bool,
                  highlight_format: HighlightFormat) -> Text:
        ...

    @abstractmethod
    def erase(self, text: Text) -> Text:
        ...
