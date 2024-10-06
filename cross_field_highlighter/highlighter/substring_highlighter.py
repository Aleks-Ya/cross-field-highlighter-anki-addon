from cross_field_highlighter.highlighter.highlighter import Highlighter
from cross_field_highlighter.highlighter.highlighter_outcome import HighlighterOutcome
from cross_field_highlighter.highlighter.highlighter_params import HighlighterParams


class SubstringHighlighter(Highlighter):
    def highlight(self, highlighter_params: HighlighterParams) -> HighlighterOutcome:
        pass

    def erase(self, highlighter_params: HighlighterParams) -> HighlighterOutcome:
        pass
