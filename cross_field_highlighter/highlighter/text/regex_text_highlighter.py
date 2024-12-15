import logging
from logging import Logger

from ..token.find_and_replace_token_highlighter import FindAndReplaceTokenHighlighter
from ..token.start_with_token_highlighter import StartWithTokenHighlighter
from ...highlighter.formatter.formatter_facade import FormatterFacade
from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.text.text_highlighter import TextHighlighter
from ...highlighter.tokenizer.stop_words_tokenizer import StopWordsTokenizer
from ...highlighter.tokenizer.tokenizer import Tokenizer, Tokens, TokenType, Token
from ...highlighter.types import Text, Word, Words

log: Logger = logging.getLogger(__name__)


class RegexTextHighlighter(TextHighlighter):
    def __init__(self, start_with_token_highlighter: StartWithTokenHighlighter,
                 find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter, formatter_facade: FormatterFacade,
                 tokenizer: Tokenizer, stop_words_tokenizer: StopWordsTokenizer):
        self.__start_with_token_highlighter: StartWithTokenHighlighter = start_with_token_highlighter
        self.__find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter = find_and_replace_token_highlighter
        self.__formatter_facade: FormatterFacade = formatter_facade
        self.__tokenizer: Tokenizer = tokenizer
        self.__stop_words_tokenizer: StopWordsTokenizer = stop_words_tokenizer

    def highlight(self, collocation: Text, text: Text, stop_words: Text, space_delimited_language: bool,
                  highlight_format: HighlightFormat) -> Text:
        super().highlight(collocation, text, stop_words, space_delimited_language, highlight_format)
        if not collocation or collocation.strip() == "":
            return text
        collocation_tokens: Tokens = self.__tokenizer.tokenize_distinct(collocation)
        collocation_tokens.delete_by_token_type(TokenType.SPACE)
        collocation_tokens.delete_by_token_type(TokenType.PUNCTUATION)
        stop_words_tokenized: Tokens = self.__stop_words_tokenizer.tokenize(stop_words)
        for stop_token in stop_words_tokenized:
            collocation_tokens.delete_word(stop_token.word)
        collocation_token: Token = Token(Word(collocation), TokenType.WORD)
        collocation_tokens.insert(0, collocation_token)
        highlighted_words: Words = Words([])
        clean_text: Text = self.erase(text)
        special_tokens: Tokens = Tokens([collocation_token])
        text_tokens: Tokens = self.__tokenizer.tokenize(clean_text, special_tokens)
        for text_token in text_tokens:
            if space_delimited_language:
                highlighted_text_word: Word = self.__start_with_token_highlighter.highlight(
                    text_token, collocation_tokens, highlight_format)
            else:
                highlighted_text_word: Word = self.__find_and_replace_token_highlighter.highlight(
                    text_token, collocation_tokens, highlight_format)
            highlighted_words.append(highlighted_text_word)
        return Text("".join(highlighted_words))

    def erase(self, text: Text) -> Text:
        super().erase(text)
        return self.__formatter_facade.erase(text)
