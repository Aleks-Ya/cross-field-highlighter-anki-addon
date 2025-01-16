from typing import Callable

import pytest

from cross_field_highlighter.highlighter.tokenizer.regex_tokenizer import RegExTokenizer
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Tokens, Token, TokenType
from cross_field_highlighter.highlighter.types import Text, Words, Word


@pytest.fixture
def tokenize(regex_tokenizer: RegExTokenizer) -> Callable[[str, list[Token]], Tokens]:
    return lambda text, special_tokens: regex_tokenizer.tokenize(Text(text), special_tokens)


def test_tokenize_by_space(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('Hello, beautiful world!', []) == Tokens([
        Token(Word('Hello'), TokenType.WORD),
        Token(Word(','), TokenType.PUNCTUATION),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('beautiful'), TokenType.WORD),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('world'), TokenType.WORD),
        Token(Word('!'), TokenType.PUNCTUATION)
    ])


def test_tokenize_by_line_break(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('Hello, beautiful\nworld!', []) == [
        Token(Word('Hello'), TokenType.WORD),
        Token(Word(','), TokenType.PUNCTUATION),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('beautiful'), TokenType.WORD),
        Token(Word('\n'), TokenType.SPACE),
        Token(Word('world'), TokenType.WORD),
        Token(Word('!'), TokenType.PUNCTUATION)
    ]


def test_tokenize_tag(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('Hello, <b>beautiful</b>\nworld!', []) == [
        Token(Word('Hello'), TokenType.WORD),
        Token(Word(','), TokenType.PUNCTUATION),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('<b>'), TokenType.TAG),
        Token(Word('beautiful'), TokenType.WORD),
        Token(Word('</b>'), TokenType.TAG),
        Token(Word('\n'), TokenType.SPACE),
        Token(Word('world'), TokenType.WORD),
        Token(Word('!'), TokenType.PUNCTUATION)
    ]


def test_tokenize_html_tags(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('<li>Hello, world!</li>', []) == [
        Token(Word('<li>'), TokenType.TAG),
        Token(Word('Hello'), TokenType.WORD),
        Token(Word(','), TokenType.PUNCTUATION),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('world'), TokenType.WORD),
        Token(Word('!'), TokenType.PUNCTUATION),
        Token(Word('</li>'), TokenType.TAG)
    ]


def test_tokenize_japanese(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('中にあるテキスト', []) == [Token(Word('中にあるテキスト'), TokenType.WORD)]
    assert tokenize('<li>中にあるテキスト</li>', []) == [
        Token(Word('<li>'), TokenType.TAG),
        Token(Word('中にあるテキスト'), TokenType.WORD),
        Token(Word('</li>'), TokenType.TAG)
    ]


def test_tokenize_slash(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('Hello, beautiful/nice world\\universe!', []) == Tokens([
        Token(Word('Hello'), TokenType.WORD),
        Token(Word(','), TokenType.PUNCTUATION),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('beautiful'), TokenType.WORD),
        Token(Word('/'), TokenType.PUNCTUATION),
        Token(Word('nice'), TokenType.WORD),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('world'), TokenType.WORD),
        Token(Word('\\'), TokenType.PUNCTUATION),
        Token(Word('universe'), TokenType.WORD),
        Token(Word('!'), TokenType.PUNCTUATION)
    ])


def test_tokenize_square_brackets(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('Hello, [beautiful][nice] world!', []) == Tokens([
        Token(Word('Hello'), TokenType.WORD),
        Token(Word(','), TokenType.PUNCTUATION),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('['), TokenType.PUNCTUATION),
        Token(Word('beautiful'), TokenType.WORD),
        Token(Word(']'), TokenType.PUNCTUATION),
        Token(Word('['), TokenType.PUNCTUATION),
        Token(Word('nice'), TokenType.WORD),
        Token(Word(']'), TokenType.PUNCTUATION),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('world'), TokenType.WORD),
        Token(Word('!'), TokenType.PUNCTUATION)
    ])


def test_tokenize_by_special_token(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('Resistant to intrusions.', [Token(Word("intrusion"), TokenType.WORD)]) == Tokens([
        Token(Word('Resistant'), TokenType.WORD),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('to'), TokenType.WORD),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('intrusion'), TokenType.WORD),
        Token(Word('s'), TokenType.WORD),
        Token(Word('.'), TokenType.PUNCTUATION)
    ])


def test_tokenize_curly_quotes(tokenize: Callable[[str, list[Token]], Words]):
    assert tokenize('Beautiful “world.”', []) == Tokens([
        Token(Word('Beautiful'), TokenType.WORD),
        Token(Word(' '), TokenType.SPACE),
        Token(Word('“'), TokenType.PUNCTUATION),
        Token(Word('world'), TokenType.WORD),
        Token(Word('.'), TokenType.PUNCTUATION),
        Token(Word('”'), TokenType.PUNCTUATION),
    ])
