import logging
from logging import Logger
from re import match, escape, IGNORECASE, UNICODE, Match

from .token_highlighter import TokenHighlighter
from ..tokenizer.tokenizer import TokenType
from ...highlighter.formatter.formatter_facade import FormatterFacade
from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.tokenizer.tokenizer import Tokens, Token
from ...highlighter.types import Text, Word

log: Logger = logging.getLogger(__name__)


class StartWithTokenHighlighter(TokenHighlighter):
    def __init__(self, formatter_facade: FormatterFacade):
        self.__formatter_facade: FormatterFacade = formatter_facade

    def highlight(self, text_token: Token, collocation_tokens: Tokens, highlight_format: HighlightFormat) -> Word:
        highlighted_text_word: Word = text_token.word
        for collocation_token in collocation_tokens:
            if collocation_token.token_type == TokenType.TAG:
                continue
            collocation_word: Word = escape(collocation_token.word)
            collocation_word_length: int = len(collocation_word)
            text_word_length: int = len(text_token.word)
            collocation_word_regexp: str = fr"{collocation_word[:collocation_word_length - 2]}\w*" \
                if collocation_word_length > 3 else collocation_word
            match_result: Match[str] = match(collocation_word_regexp, text_token.word, IGNORECASE | UNICODE)
            too_long: bool = text_word_length > collocation_word_length + 3
            if match_result and not too_long:
                highlighted_text_word = self.__formatter_facade.format(text_token.word, highlight_format)
                break
        return highlighted_text_word

    def erase(self, text_token: Token) -> Word:
        super().erase(text_token)
        return Word(self.__formatter_facade.erase(Text(text_token.word)))
