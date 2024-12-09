from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.token.find_and_replace_token_highlighter import FindAndReplaceTokenHighlighter
from cross_field_highlighter.highlighter.tokenizer.tokenizer import Token, TokenType, Tokens
from cross_field_highlighter.highlighter.types import Word


def test_highlight_case_insensitive(find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter,
                                    bold_format: HighlightFormat):
    text_token: Token = Token(Word("Hello, Beautiful world!"), TokenType.WORD)
    collocation_tokens: Tokens = Tokens([Token(Word("beautiful"), TokenType.WORD)])
    highlighted_word: Word = find_and_replace_token_highlighter.highlight(text_token, collocation_tokens, bold_format)
    assert highlighted_word == Word('Hello, <b class="cross-field-highlighter">Beautiful</b> world!')


def test_highlight_japanese(find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter,
                            bold_format: HighlightFormat):
    text_token: Token = Token(Word("これは大きな日本語のテキストです。中にあるテキストをラップします。中にあるテキスト"),
                              TokenType.WORD)
    collocation_tokens: Tokens = Tokens([Token(Word("中にあるテキスト"), TokenType.WORD)])
    highlighted_word: Word = find_and_replace_token_highlighter.highlight(text_token, collocation_tokens, bold_format)
    assert highlighted_word == Word(
        'これは大きな日本語のテキストです。'
        '<b class="cross-field-highlighter">中にあるテキスト</b>をラップします。'
        '<b class="cross-field-highlighter">中にあるテキスト</b>')


def test_highlight_2nd_collocation_matches(find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter,
                                           bold_format: HighlightFormat):
    text_token: Token = Token(Word("beautiful"), TokenType.WORD)
    collocation_tokens: Tokens = Tokens([
        Token(Word("beautiful"), TokenType.WORD),
        Token(Word("</b>"), TokenType.TAG)
    ])
    highlighted_word: Word = find_and_replace_token_highlighter.highlight(text_token, collocation_tokens, bold_format)
    assert highlighted_word == Word('<b class="cross-field-highlighter">beautiful</b>')
