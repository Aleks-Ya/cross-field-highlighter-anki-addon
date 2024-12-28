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
        text_word: Word = escape(text_token.word)
        return (StartWithMatcher.__match_full(text_word, collocation_word) or
                StartWithMatcher.__match_short(text_word, collocation_word))

    @staticmethod
    def __match_full(text_word: Word, collocation_word: Word) -> bool:
        collocation_word_regexp: str = fr"{collocation_word}\w*"
        match_result: Match[str] = match(collocation_word_regexp, text_word, IGNORECASE | UNICODE)
        too_long: bool = len(text_word) > len(collocation_word) + 3
        return match_result and not too_long

    @staticmethod
    def __match_short(text_word: Word, collocation_word: Word) -> bool:
        collocation_word_length: int = len(collocation_word)
        if collocation_word_length <= 3:
            return False
        collocation_word_max_length: int = collocation_word_length - int(collocation_word_length * 0.4)
        collocation_word_short: str = collocation_word[:collocation_word_max_length]
        collocation_word_regexp: str = fr"{collocation_word_short}\w*"
        match_result: Match[str] = match(collocation_word_regexp, text_word, IGNORECASE | UNICODE)
        too_long: bool = len(text_word) > collocation_word_length + 4
        return match_result and not too_long
