from enum import Enum
from typing import NewType


class HighlightFormatCode(Enum):
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    UNDERLINE = "UNDERLINE"
    MARK = "MARK"


class HighlightFormat:
    def __init__(self, name: str, code: HighlightFormatCode):
        self.name = name
        self.code = code

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, {self.code.value})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, __value):
        return self.name == __value.name and self.code == __value.code \
            if isinstance(__value, HighlightFormat) else False

    def __hash__(self):
        return hash((self.name, self.code))


HighlightFormats = NewType("HighlightFormats", list[HighlightFormat])
