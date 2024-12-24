from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.token.start_with_token_highlighter import StartWithTokenHighlighter
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Token, TokenType, Tokens
from cross_field_highlighter.highlighter.types import Word


def test_highlight(start_with_token_highlighter: StartWithTokenHighlighter, bold_format: HighlightFormat):
    text_token: Token = Token(Word("Beautiful"), TokenType.WORD)
    collocation_tokens: Tokens = Tokens([Token(Word("beautiful"), TokenType.WORD)])
    highlighted_token: Word = start_with_token_highlighter.highlight(text_token, collocation_tokens, bold_format)
    assert highlighted_token == Word('<b class="cross-field-highlighter">Beautiful</b>')


def test_highlight_short_words(start_with_token_highlighter: StartWithTokenHighlighter, bold_format: HighlightFormat):
    text_token: Token = Token(Word("measure"), TokenType.WORD)
    collocation_tokens: Tokens = Tokens([Token(Word("mesh"), TokenType.WORD)])
    highlighted_token: Word = start_with_token_highlighter.highlight(text_token, collocation_tokens, bold_format)
    assert highlighted_token == Word('<b class="cross-field-highlighter">measure</b>')  # TODO fix it


def test_highlight_short_words_ing(start_with_token_highlighter: StartWithTokenHighlighter,
                                   bold_format: HighlightFormat):
    text_token: Token = Token(Word("drowning"), TokenType.WORD)
    collocation_tokens: Tokens = Tokens([Token(Word("drown"), TokenType.WORD)])
    highlighted_token: Word = start_with_token_highlighter.highlight(text_token, collocation_tokens, bold_format)
    assert highlighted_token == Word('<b class="cross-field-highlighter">drowning</b>')
