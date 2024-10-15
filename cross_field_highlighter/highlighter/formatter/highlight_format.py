from enum import Enum


class HighlightFormatCode(Enum):
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    UNDERLINE = "UNDERLINE"
    MARK = "MARK"


class HighlightFormat:
    def __init__(self, name: str, code: HighlightFormatCode):
        self.name = name
        self.code = code
