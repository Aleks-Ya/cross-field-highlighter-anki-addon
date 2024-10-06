from abc import ABC, abstractmethod

from cross_field_highlighter.highlighter.highlighter_outcome import HighlighterOutcome
from cross_field_highlighter.highlighter.highlighter_params import HighlighterParams


class Highlighter(ABC):
    @abstractmethod
    def highlight(self, highlighter_params: HighlighterParams) -> HighlighterOutcome:
        pass

    @abstractmethod
    def erase(self, highlighter_params: HighlighterParams) -> HighlighterOutcome:
        pass
