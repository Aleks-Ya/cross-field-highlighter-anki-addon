from cross_field_highlighter.highlighter.token.start_with_matcher import StartWithMatcher
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Token, TokenType
from cross_field_highlighter.highlighter.types import Word


def test_match():
    assert __match("Beautiful", "beautiful")
    assert __match("measure", "mesh")
    assert __match("drowning", "drown")
    assert __match("forgotten", "forget")


def __match(text_token_word: str, collocation_token_word: str, text_token_type: TokenType = TokenType.WORD,
            collocation_token_type: TokenType = TokenType.WORD) -> bool:
    return StartWithMatcher.match(Token(Word(text_token_word), text_token_type),
                                  Token(Word(collocation_token_word), collocation_token_type))
