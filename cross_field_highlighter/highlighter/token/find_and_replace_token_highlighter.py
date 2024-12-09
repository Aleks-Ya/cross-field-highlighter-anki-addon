import logging
import re
from logging import Logger

from .token_highlighter import TokenHighlighter
from ..tokenizer.tokenizer import TokenType
from ...highlighter.formatter.formatter_facade import FormatterFacade
from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.tokenizer.tokenizer import Tokens, Token
from ...highlighter.types import Text, Word

log: Logger = logging.getLogger(__name__)


class FindAndReplaceTokenHighlighter(TokenHighlighter):
    def __init__(self, formatter_facade: FormatterFacade):
        self.__formatter_facade: FormatterFacade = formatter_facade

    def highlight(self, text_token: Token, collocation_tokens: Tokens, highlight_format: HighlightFormat) -> Word:
        if text_token.token_type == TokenType.TAG:
            return text_token.word
        for collocation_token in collocation_tokens:
            pattern: str = f"({re.escape(collocation_token.word)})"
            highlighted_collocation_word: Word = self.__formatter_facade.format(Word("\\1"), highlight_format)
            highlighted_text_word: Word = Word(re.sub(pattern, highlighted_collocation_word, text_token.word,
                                                      flags=re.IGNORECASE))
            if highlighted_text_word != text_token.word:
                return highlighted_text_word
        return text_token.word

    def erase(self, text_token: Token) -> Word:
        super().erase(text_token)
        return Word(self.__formatter_facade.erase(Text(text_token.word)))
