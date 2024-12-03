from abc import ABC, abstractmethod

from ..tokenizer.tokenizer import Token, Tokens
from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.types import Word


class TokenHighlighter(ABC):
    @abstractmethod
    def highlight(self, text_token: Token, collocation_tokens: Tokens, highlight_format: HighlightFormat) -> Word:
        ...

    @abstractmethod
    def erase(self, text_token: Token) -> Word:
        ...
