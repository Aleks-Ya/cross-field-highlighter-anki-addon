from .destination import Destination
from .highlight_format import HighlightFormat
from .source import Source


class HighlighterParams:
    def __init__(self, source: Source, destinations: Destination, highlight_format: HighlightFormat):
        self.source: Source = source
        self.destinations: Destination = destinations
        self.highlight_format: HighlightFormat = highlight_format


class BulkHighlighterParams:
    def __init__(self, params: list[HighlighterParams]):
        self.params: list[HighlighterParams] = params
