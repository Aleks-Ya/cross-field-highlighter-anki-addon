from abc import ABC


class HighlightFormat(ABC):
    pass


class BoldHighlightFormat(HighlightFormat):
    pass


class ItalicHighlightFormat(HighlightFormat):
    pass


class UnderscoreHighlightFormat(HighlightFormat):
    pass
