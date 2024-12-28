import logging
from logging import Logger
from re import match, escape, IGNORECASE, UNICODE, Match

from ..tokenizer.tokenizer import TokenType
from ...highlighter.tokenizer.tokenizer import Token
from ...highlighter.types import Word

log: Logger = logging.getLogger(__name__)


class StartWithMatcher:
    @staticmethod
    def match(text_token: Token, collocation_token: Token) -> bool:
        if collocation_token.token_type == TokenType.TAG:
            return False
        collocation_word: Word = escape(collocation_token.word)
        collocation_word_length: int = len(collocation_word)
        collocation_word_short: str = collocation_word[:collocation_word_length - 2]
        text_word_length: int = len(text_token.word)
        collocation_word_regexp: str = fr"{collocation_word_short}\w*" if collocation_word_length > 3 else collocation_word
        match_result: Match[str] = match(collocation_word_regexp, text_token.word, IGNORECASE | UNICODE)
        too_long: bool = text_word_length > collocation_word_length + 3
        matches: bool = match_result and not too_long
        return matches
