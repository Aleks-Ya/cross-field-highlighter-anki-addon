from cross_field_highlighter.highlighter.token.start_with_matcher import StartWithMatcher
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Token, TokenType
from cross_field_highlighter.highlighter.types import Word


def test_match():
    assert __match("beautiful", "Beautiful")
    assert not __match("mesh", "measure")
    assert __match("drown", "drowning")
    assert __match("forget", "forgotten")
    assert __match("forget", "forgetting")


def __match(collocation_token_word: str, text_token_word: str, collocation_token_type: TokenType = TokenType.WORD,
            text_token_type: TokenType = TokenType.WORD) -> bool:
    return StartWithMatcher.match(Token(Word(text_token_word), text_token_type),
                                  Token(Word(collocation_token_word), collocation_token_type))
